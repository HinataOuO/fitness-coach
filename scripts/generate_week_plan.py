#!/usr/bin/env python3
"""Validate a weekly plan, optionally embedding it in standalone HTML."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "assets" / "week-plan.schema.json"
TEMPLATE_PATH = ROOT / "assets" / "fitness-coach-log.html"
MARKER = "__WEEK_PLAN_JSON__"


class GenerationError(Exception):
    """Expected input or output error suitable for CLI display."""


def read_json(path: Path, label: str) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise GenerationError(f"lettura {label} fallita: {path}: {exc}") from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise GenerationError(
            f"JSON {label} non valido: {path}:{exc.lineno}:{exc.colno}: {exc.msg}"
        ) from exc


def matches_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise GenerationError(f"schema non supportato: type={expected!r}")


def validate(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    expected = schema.get("type")
    if expected is not None and not matches_type(value, expected):
        raise GenerationError(f"violazione schema in {path}: atteso {expected}")

    if "const" in schema and value != schema["const"]:
        raise GenerationError(f"violazione schema in {path}: valore incompatibile")
    if "enum" in schema and value not in schema["enum"]:
        choices = ", ".join(repr(item) for item in schema["enum"])
        raise GenerationError(f"violazione schema in {path}: valore non ammesso ({choices})")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in value:
                raise GenerationError(f"violazione schema in {path}: campo richiesto {name!r}")
        if schema.get("additionalProperties") is False:
            extra = value.keys() - properties.keys()
            if extra:
                name = sorted(extra)[0]
                raise GenerationError(f"violazione schema in {path}.{name}: proprietà non ammessa")
        for name, item in value.items():
            if name in properties:
                validate(item, properties[name], f"{path}.{name}")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise GenerationError(f"violazione schema in {path}: troppo pochi elementi")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise GenerationError(f"violazione schema in {path}: troppi elementi")
        if "items" in schema:
            for index, item in enumerate(value):
                validate(item, schema["items"], f"{path}[{index}]")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise GenerationError(f"violazione schema in {path}: stringa troppo corta")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            raise GenerationError(f"violazione schema in {path}: stringa troppo lunga")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise GenerationError(f"violazione schema in {path}: valore sotto il minimo")
        if "maximum" in schema and value > schema["maximum"]:
            raise GenerationError(f"violazione schema in {path}: valore sopra il massimo")


def validate_unique_ids(plan: dict[str, Any]) -> None:
    session_ids: set[str] = set()
    for session_index, session in enumerate(plan["sessions"]):
        session_id = session["id"]
        if session_id in session_ids:
            raise GenerationError(
                f"violazione applicativa in $.sessions[{session_index}].id: ID sessione duplicato {session_id!r}"
            )
        session_ids.add(session_id)

        exercise_ids: set[str] = set()
        for exercise_index, exercise in enumerate(session["exercises"]):
            exercise_id = exercise["id"]
            if exercise_id in exercise_ids:
                raise GenerationError(
                    "violazione applicativa in "
                    f"$.sessions[{session_index}].exercises[{exercise_index}].id: "
                    f"ID esercizio duplicato {exercise_id!r}"
                )
            exercise_ids.add(exercise_id)


def render(plan: Any, schema: Any, template: str) -> str:
    if not isinstance(schema, dict):
        raise GenerationError("schema non valido: radice non object")
    expected_version = schema.get("properties", {}).get("schemaVersion", {}).get("const")
    if isinstance(plan, dict) and "schemaVersion" in plan and plan["schemaVersion"] != expected_version:
        raise GenerationError(
            f"versione schema incompatibile in $.schemaVersion: attesa {expected_version!r}"
        )
    validate(plan, schema)
    validate_unique_ids(plan)

    marker_count = template.count(MARKER)
    if marker_count != 1:
        detail = "assente" if marker_count == 0 else f"duplicato ({marker_count} occorrenze)"
        raise GenerationError(f"marker {MARKER!r} {detail} nel template")

    payload = json.dumps(plan, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return template.replace(MARKER, payload)


def write_atomic(path: Path, content: str) -> None:
    if not path.parent.is_dir():
        raise GenerationError(f"scrittura output fallita: directory inesistente: {path.parent}")

    temporary: Path | None = None
    try:
        descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
        temporary = Path(name)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
        temporary = None
    except (OSError, UnicodeError) as exc:
        raise GenerationError(f"scrittura output fallita: {path}: {exc}") from exc
    finally:
        if temporary is not None:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass


def generate(plan_path: Path, output_path: Path | None = None) -> None:
    plan = read_json(plan_path, "piano")
    schema = read_json(SCHEMA_PATH, "schema")
    if not isinstance(schema, dict):
        raise GenerationError("schema non valido: radice non object")
    expected_version = schema.get("properties", {}).get("schemaVersion", {}).get("const")
    if isinstance(plan, dict) and "schemaVersion" in plan and plan["schemaVersion"] != expected_version:
        raise GenerationError(
            f"versione schema incompatibile in $.schemaVersion: attesa {expected_version!r}"
        )
    validate(plan, schema)
    validate_unique_ids(plan)
    if output_path is None:
        return
    try:
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise GenerationError(f"lettura template fallita: {TEMPLATE_PATH}: {exc}") from exc
    write_atomic(output_path, render(plan, schema, template))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Valida un piano settimanale JSON.")
    parser.add_argument("plan", type=Path, help="piano JSON UTF-8")
    parser.add_argument("--output", type=Path, help="genera anche un file HTML standalone")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        generate(args.plan, args.output)
    except GenerationError as exc:
        print(f"errore: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
