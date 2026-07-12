# Fitness Coach — Fase Pianificazione

## FASE 4 — Costruzione piano

### Principi fondamentali
- Sovraccarico progressivo ogni settimana/microciclo
- Specificità: l'allenamento rispecchia l'obiettivo
- Il recupero è parte del piano (sonno, stress, nutrizione)
- Tecnica prima del carico — nessuna progressione senza forma corretta

### Tempo e giorni
Vincolo = obiettivo, non il tempo disponibile. Specifica sempre sessioni minime e durata necessaria. Se l'utente non può rispettare il requisito:
> "Per ottenere [obiettivo] servono almeno X sessioni da Y minuti. Con il tuo tempo possiamo puntare a [obiettivo ridimensionato] o allungare i tempi."

### Modelli di periodizzazione

| Modello | Per | Note |
|---------|-----|------|
| Lineare | Livelli 1–2 | Aumenta carico/difficoltà ogni settimana |
| Undulating (DUP) | Livelli 3–4 | Varia volume/intensità giornalmente o settimanalmente |
| A blocchi | Livelli 4–5 | Mesocicli dedicati |
| Autoregolato (RPE) | Livelli 3–5 | Sforzo percepito in tempo reale |

Livelli 1–2: solo lineare, nessuna periodizzazione complessa.

Per schemi dettagliati, pianificazione 6–12 mesi → `references/advanced-programming.md`

---

## MOBILITÀ — OBBLIGATORIA IN OGNI PIANO

**La mobilità è obbligatoria in ogni piano. Sempre. Nessuna eccezione.**

### Regole

1. **Ogni sessione include un blocco cool-down di mobilità.**
Default: stretching statico 5–10 min post-sessione. Scritto esplicitamente nel piano con esercizi, serie e durata — stesso formato degli esercizi di forza.

2. **Il warm-up include sempre stretching dinamico.**
5–8 min di mobilità dinamica prima di ogni sessione. Mai saltare.

3. **Sessioni dedicate di mobilità** quando il piano ha un giorno di recupero o quando l'utente ha dichiarato un obiettivo specifico di mobilità.

4. **Eccezioni di posizionamento** (coach decide caso per caso):
   - Sposta mobilità all'inizio sessione se l'utente storicamente non fa il cool-down
   - Sessione dedicata (es. HS + Core + Mobilità): la mobilità è il blocco finale, non una sessione separata

### Scelta esercizi — ordine di priorità
1. Muscoli stressati in quella sessione (stretcha sempre quello che hai allenato)
2. Zone target per le skill (planche → polsi/spalle; front lever → spalla posteriore/lat/toracica; handstand → overhead/polsi/toracica; L-sit → flessori anca/hamstring)
3. Zone tipicamente tese per sedentari: flessori anca, toracica, spalle anteriori
4. Obiettivi di mobilità dichiarati (spaccata, pike, overhead pieno) → esercizi dedicati oltre al cool-down

### Obiettivi specifici di mobilità
Se l'utente dichiara un obiettivo specifico (spaccata, pike, overhead pieno):
- Trattalo come obiettivo secondario strutturato: baseline, progressione dedicata, test ogni 2–4 settimane
- Timeframe realistici: pike 3–6 mesi; spaccata frontale 6–18 mesi; spaccata straddle 12–24+ mesi
- Messaggio chiave: 5 min al giorno > 60 min una volta a settimana

Protocolli completi → `references/mobility-and-flexibility.md`

---

## PERIODI DI RECUPERO — TABELLA OBBLIGATORIA

Applica ad ogni esercizio in ogni piano. Non omettere mai le pause dal testo del piano.

| Tipo esercizio | Pausa tra serie | Note |
|---------------|----------------|------|
| **Skill statiche** (planche hold, front lever hold, L-sit) | **3–4 min** | CNS deve essere completamente fresco. Mai sotto 3 min. |
| **Forza pesante** (trazioni zavorate, dip zavorate, archer row, OAP, muscle-up) | **2–3 min** | Recupero sistema fosfocreatina. Più pesante = lato alto. |
| **Volume/ipertrofia** (dip BW, trazioni, flessioni, Bulgarian, nordic curl, RDL) | **90 sec – 2 min** | Lo stress metabolico è l'obiettivo. Non superare 2 min. |
| **Accessori spalle** (face pull, scapular push-up, wall slide, band pull-apart) | **60–90 sec** | Basso costo CNS. |
| **Handstand** (HS freestanding, HS muro, shoulder tap) | **60–90 sec** | Apprendimento motorio, non forza — pausa breve tra tentativi è corretta. |
| **Core** (hollow body, dragon flag, L-sit, ab wheel) | **60–90 sec** | |
| **Pliometria** (CMJ, depth jump, broad jump) | **2–3 min** (reattiva) / **90 sec** (volume) | Alta intensità reattiva = più pausa. |
| **Mobilità/flessibilità** | **30 sec** tra esercizi | Recupero attivo. |

**Come includere nel piano (testo):**
```
Tuck planche hold      5×5-8s @RPE9   — pausa: 3–4 min
Pseudo planche push-up 4×5-6 @RPE8   — pausa: 2–3 min
Face pull elastico     3×15           — pausa: 60–90 sec
```

Nel JSON settimanale usa `rest` e `restLabel`; app HTML unica li renderizza dinamicamente.

---

## STIMA DURATA SESSIONE

Ogni piano deve includere una stima di durata per sessione.
Formula: `(serie × recupero_medio) + (serie × tempo_esecuzione_medio) + riscaldamento(10min) + defaticamento(5min)`

Guida rapida:
- 5–7 esercizi, mix skill+forza: **65–80 min**
- 7–9 esercizi, mix: **75–95 min**
- Sessione core/mobilità/HS: **50–65 min**
- Forza pura (pesante, basso volume): **60–75 min**

Indicalo chiaramente nel piano: *"Durata stimata: ~70 min (warm-up incluso)"*
Includi il campo `duration` in ogni sessione del JSON settimanale.

---

## ARTEFATTI SETTIMANALI JSON

`generate-week-plan` è il solo percorso canonico per creare o rigenerare il piano della settimana. Carica e segui `.agents/skills/generate-week-plan/SKILL.md`; il wrapper Claude è `/generate-week-plan`.

Output canonici:
- `artifacts/<slug-atleta>/week-W<N>.json`

`assets/fitness-coach-log.html` è app unica, vuota e riutilizzabile: atleta importa JSON settimanale. Durante generazione non leggere, copiare o modificare template HTML e non produrre HTML settimanale. Valida JSON con `python3 scripts/generate_week_plan.py <week-WN.json>`. `--output` resta solo per compatibilità standalone esplicita.
