---
name: generate-week-plan
description: Genera o rigenera per un atleta esplicito JSON validato e HTML standalone della settimana prevista dal piano corrente. Usare con `$generate-week-plan ATLETA WN` o quando l'utente chiede week-WN.
---

## purpose
Generare dal profilo persistito la coppia sincronizzata `artifacts/<slug-atleta>/week-W<N>.json` e `artifacts/<slug-atleta>/week-W<N>.html`, usando il template `assets/fitness-coach-log.html` tramite il generatore Python.

## load
- `core/KERNEL.md` e `core/CONVENTIONS.md`.
- Solo `<atleta>/profile-core.md`, `<atleta>/profile-plan-current.md` e sezione finale pertinente di `<atleta>/profile-log-history.md`.
- `phases/planning.md`, `references/goal-compatibility.md` e soli riferimenti richiesti da profilo, obiettivi, livello, dolore, recupero e piano.
- `assets/week-plan.schema.json`.

## scope
- Atleta e settimana espliciti sono obbligatori; settimana deve esistere nel piano e ultimo report deve essere disponibile.
- JSON conforme allo schema, con ID deterministici e stabili tra rigenerazioni equivalenti; HTML standalone generato dallo stesso JSON.
- Rigenerare stessa settimana sostituisce entrambi gli artefatti canonici.

## deny
- Non creare file finché input obbligatori non sono presenti e coerenti.
- Non inventare settimana, report, carichi, giorni o vincoli.
- Non modificare template HTML.
- Non pubblicare JSON non validato, HTML non generato dallo stesso JSON, né modificare profili, piano, schema o generatore.

## procedure
1. Risolvere nome verso una sola directory atleta top-level. Leggere solo file richiesti. Verificare settimana 1–53 dichiarata e ultimo report; altrimenti fermarsi senza scritture.
2. Derivare settimana dal piano, adattandola solo con report e vincoli. Applicare riferimenti pertinenti.
3. Creare slug con Unicode NFKD: minuscolo ASCII alfanumerico, sequenze non alfanumeriche come `-`, lettere non ASCII non traslitterabili scartate, trattini compressi/rimossi ai bordi. Rifiutare slug vuoto. Verificare con `Path.is_relative_to(artifacts.resolve())` che output resti sotto `artifacts/`.
4. Costruire documento conforme. ID = prefisso leggibile + primi 12 caratteri SHA-256 di chiave UTF-8 canonica normalizzata NFKC, spazi compressi, minuscolo: piano=`<slug>|<identità-piano>`; sessione=`<plan-id>|<giorno>|<nome-sessione>`; esercizio=`<session-id>|<posizione-zero-based>|<nome-esercizio>`.
5. Scrivere e `fsync` JSON in temporaneo univoco nella directory atleta. Generare HTML in altro temporaneo della stessa directory con `python3 scripts/generate_week_plan.py <temp-json> --output <temp-html>`.
6. Solo su uscita zero pubblicare con `os.replace` verso `week-W<N>.html` e `week-W<N>.json`. Su errore di validazione o generazione lasciare entrambi gli artefatti precedenti invariati. Eliminare sempre temporanei.

## done
- JSON canonico esiste e supera CLI di validazione; HTML canonico è stato generato dallo stesso JSON.
- Entrambi gli artefatti esistono, nessun temporaneo residuo, percorsi sotto `artifacts/`, ID stabili.
