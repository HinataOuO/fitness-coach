---
name: generate-week-plan
description: Genera o rigenera per un atleta esplicito il JSON validato della settimana e, solo su richiesta esplicita, l'HTML standalone. Usare con `$generate-week-plan ATLETA WN`, quando l'utente chiede week-WN o qualsiasi scheda, piano o settimana in HTML.
---

## purpose
Generare dal profilo persistito `artifacts/<slug-atleta>/week-W<N>.json` come fonte canonica. Generare anche `week-W<N>.html` esclusivamente su richiesta esplicita, sempre dal medesimo JSON tramite il generatore Python.

## load
- `core/KERNEL.md` e `core/CONVENTIONS.md`.
- Solo `<atleta>/profile-core.md`, `<atleta>/profile-plan-current.md` e sezione finale pertinente di `<atleta>/profile-log-history.md`.
- `phases/planning.md`, `references/goal-compatibility.md` e soli riferimenti richiesti da profilo, obiettivi, livello, dolore, recupero e piano.
- `assets/week-plan.schema.json`.

## scope
- Atleta e settimana espliciti sono obbligatori; settimana deve esistere nel piano e ultimo report deve essere disponibile.
- JSON conforme allo schema, con ID deterministici e stabili tra rigenerazioni equivalenti.
- Output predefinito solo JSON. HTML standalone solo quando richiesto esplicitamente.
- Rigenerare la stessa settimana in modalità JSON-only sostituisce il JSON ed elimina l'eventuale HTML obsoleto; in modalità HTML sostituisce entrambi.

## deny
- Non creare file finché input obbligatori non sono presenti e coerenti.
- Non inventare settimana, report, carichi, giorni o vincoli.
- Non modificare template HTML.
- Non scrivere o modificare HTML manualmente. Non pubblicare JSON non validato, HTML non generato dallo stesso JSON, né modificare profili, piano, schema o generatore.

## procedure
1. Risolvere nome verso una sola directory atleta top-level. Leggere solo file richiesti. Verificare settimana 1–53 dichiarata e ultimo report; altrimenti fermarsi senza scritture.
2. Derivare settimana dal piano, adattandola solo con report e vincoli. Applicare riferimenti pertinenti.
3. Creare slug con Unicode NFKD: minuscolo ASCII alfanumerico, sequenze non alfanumeriche come `-`, lettere non ASCII non traslitterabili scartate, trattini compressi/rimossi ai bordi. Rifiutare slug vuoto. Verificare con `Path.is_relative_to(artifacts.resolve())` che output resti sotto `artifacts/`.
4. Costruire documento conforme. ID = prefisso leggibile + primi 12 caratteri SHA-256 di chiave UTF-8 canonica normalizzata NFKC, spazi compressi, minuscolo: piano=`<slug>|<identità-piano>`; sessione=`<plan-id>|<giorno>|<nome-sessione>`; esercizio=`<session-id>|<posizione-zero-based>|<nome-esercizio>`.
5. Scrivere e `fsync` JSON in un temporaneo univoco nella directory atleta.
6. Se HTML non è richiesto, validare con `python3 scripts/generate_week_plan.py <temp-json>`. Solo su uscita zero pubblicare il JSON con `os.replace`, poi eliminare l'eventuale `week-W<N>.html` obsoleto. Su errore lasciare gli artefatti precedenti invariati.
7. Se HTML è richiesto, generarlo in un altro temporaneo della stessa directory con il comando obbligatorio `python3 scripts/generate_week_plan.py <temp-json> --output <temp-html>`. Solo su uscita zero pubblicare entrambi i temporanei con `os.replace`. Su errore di validazione o generazione lasciare entrambi gli artefatti precedenti invariati.
8. Eliminare sempre tutti i temporanei. Non pubblicare mai un artefatto parziale.

## done
- JSON canonico esiste e supera CLI di validazione; nessun temporaneo residuo, percorsi sotto `artifacts/`, ID stabili.
- Se HTML richiesto, esiste ed è stato generato dallo stesso JSON; altrimenti non esiste HTML canonico della settimana.
