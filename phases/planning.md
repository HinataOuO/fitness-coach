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

**Come includere nel file HTML:**
```javascript
{ id: uid(), name: 'Tuck planche hold', prescribed: '5×5-8s @RPE9', type: 'time', rest: '3-4min', restLabel: '3–4 min' }
```

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
Includi il campo `duration` nell'HTML `initDefaults()` per ogni sessione.

---

## APP LOG HTML

### Regola critica
**Il file HTML è l'unico formato di log accettabile.** Mai consegnare il log come testo inline, markdown, JSON, o formato testo in chat.

### Quando fornirla
Dopo aver presentato il piano completo in chat, chiedi sempre:
> "Vuoi che generi anche l'app di log personalizzata per il telefono? È un file HTML offline con le tue sessioni già caricate, le pause indicate per ogni esercizio e la durata stimata. Ogni domenica genera il report e lo incolli qui."

Se sì → genera e consegna. Se no → non generare. Offri di nuovo solo se il piano viene rivisto significativamente.
Fornisci anche su richiesta se l'utente chiede come tracciare le sessioni.

### Come consegnarla
> "Ecco la tua app di log personalizzata — salvala sul telefono (Safari: Condividi → Aggiungi a schermata Home / Chrome: Menu → Aggiungi a schermata). Funziona offline, trovi già le tue sessioni caricate. Ogni domenica genera il report e incollalo qui."

### Come generarla — step by step
1. Leggi `assets/fitness-coach-log.html` dalla directory della skill
2. Copia il contenuto completo del file
3. Sostituisci ONLY la funzione `initDefaults()` con il piano dell'utente
4. Sostituisci `USER_NAME` con il nome dell'utente e `USER_GOAL` con l'obiettivo
5. Presenta il file all'utente

### Struttura initDefaults()
```javascript
function initDefaults() {
  if (sessions.length) return;
  sessions = [
    {
      id: uid(), name: 'SESSION_NAME', day: 'DAY_LABEL',
      exercises: [
        { id: uid(), name: 'Exercise name', prescribed: 'sets×reps @RPE', type: 'reps', rest: '90sec', restLabel: '90 sec' },
        { id: uid(), name: 'Exercise name', prescribed: 'sets×Xs @RPE', type: 'time', rest: '3-4min', restLabel: '3–4 min' },
        { id: uid(), name: 'Exercise name', prescribed: '2×45s', type: 'mobility' },
      ]
    },
    // repeat for each session
  ];
  config.weekNum = 1;
  config.userName = 'USER_NAME';
  config.userGoal = 'USER_GOAL';
  save();
}
```

### Regole campi

**day:** usa i giorni reali dell'utente.
- Italiano breve: `LUN`, `MAR`, `MER`, `GIO`, `VEN`, `SAB`, `DOM`
- Giorni flessibili/rotanti: `G1`, `G2`, `G3`
- Mai lasciare vuoto — appare nel tab sessione e nel report settimanale

**type:**
- `'reps'` → contati in rep, serie o carico
- `'time'` → isometrici, hold, serie temporizzate (secondi)
- `'dist'` → corsa, canottaggio, distanza
- `'mobility'` → cool-down/mobilità — solo checkbox + note

**prescribed per esercizi palestra — CRITICO:**
Includi sempre il carico specifico. L'utente lo legge durante l'allenamento come riferimento peso. Mai scrivere prescribed senza i kg reali.

- ✅ `'4×5 @80kg @RPE8'`
- ✅ `'4×8 @60kg @RPE7'`
- ✅ `'3×10 @40kg @RPE7'`
- ❌ `'4×5 @RPE8'` — manca il carico
- ❌ `'4×5-6 heavy @RPE8'` — vago
- BW: `'4×8 BW @RPE8'` | BW+carico: `'4×6 +20kg @RPE8'` | tempo: `'4×10s @RPE9'` | mobilità: `'2×45s'`

Il carico nel `prescribed` è il **target** per quella settimana. L'utente compila `done_val` con quello che ha effettivamente sollevato.

**Quando il piano viene rivisto:** rigenera e riconsegna il file HTML aggiornato.
