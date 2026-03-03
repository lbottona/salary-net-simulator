# Salary Net Simulator

Applicazione Streamlit che consente di stimare in pochi secondi lo stipendio netto annuale e mensile partendo dalla RAL. Il calcolo e le visualizzazioni sono pensati per chi deve spiegare rapidamente le simulazioni ai candidati o confrontare offerte economiche interne.

## Demo GIF

![Demo animata](media/screen.gif)

## Funzionalita principali

- Inserimento della RAL e del numero di mensilita (12/13/14) con UI responsive.
- Report immediato su netto annuale, netto per mensilita e incidenza percentuale delle imposte.
- Dettaglio delle componenti fiscali: INPS, IRPEF lorda/netta, detrazioni, addizionali regionale e comunale, aliquote effettive e marginali.
- Styling personalizzato per un look book destinato al team HR.

## Come funziona il motore di calcolo

| Step | Descrizione                      | Formula/Dettaglio                                                                 |
| ---- | -------------------------------- | --------------------------------------------------------------------------------- |
| 1    | **Contributi INPS**              | `inps = ral * 9.19%`                                                              |
| 2    | **Imponibile fiscale**           | `imponibile = ral - inps`                                                         |
| 3    | **IRPEF lorda**                  | Scaglioni 2025: 23% (0-28k), 35% (28k-50k), 43% (>50k)                            |
| 4    | **Detrazione lavoro dipendente** | Art. 13 TUIR con le tre fasce 0-15k, 15k-28k, 28k-50k                             |
| 5    | **Addizionali**                  | Regione Lombardia (aliquote progressive 2026) + comunale flat 0.8%                |
| 6    | **Netto**                        | `netto = ral - (inps + irpef + addizionali)`; divisione per mensilita selezionate |

La logica e implementata in `src/tax_calculator.py`, mentre la UI si trova in `src/app.py`.

## Avvio rapido

1. Installare Python 3.11 o superiore.
2. Creare un ambiente virtuale e attivarlo:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. Installare le dipendenze minime:
   ```bash
   pip install streamlit
   ```
4. Avviare l app:
   ```bash
   streamlit run src/app.py
   ```

## Struttura del progetto

```
src/
├── app.py            # UI Streamlit e presentazione dei risultati
└── tax_calculator.py # Funzioni fiscali e logiche di calcolo
```

## Riferimenti ufficiali

1. **[IRPEF 2025](https://www.agenziaentrate.gov.it/portale/imposta-sul-reddito-delle-persone-fisiche-irpef-/aliquote-e-calcolo-dell-irpef)** – Legge 30 dicembre 2023, n. 213 (Legge di Bilancio 2024), art. 1 commi 52-54. Dettaglio scaglioni pubblicato dal MEF nel dossier “Riforma IRPEF 2025”.
2. **Detrazioni per lavoro dipendente** – Testo Unico delle Imposte sui Redditi, art. 13; guida Agenzia delle Entrate “Le detrazioni 2025 per i redditi di lavoro dipendente”.
3. **Contributi INPS lavoratori dipendenti settore privato** – Circolare INPS n. 11 del 16 gennaio 2024, tabella aliquote IVS (quota dipendente 9.19%).
4. **Addizionale regionale Lombardia 2026** – Deliberazione Consiglio Regionale Lombardia n. XI/9669 del 30 dicembre 2024 (codice regione 10) e prospetto ufficiale sul portale [MEF](https://www1.finanze.gov.it/finanze2/dipartimentopolitichefiscali/fiscalitalocale/addregirpef/addregirpef.php?reg=10).
5. **Addizionale comunale Milano 0.8%** – Delibera del Consiglio Comunale di Milano n. 18 del 25 marzo 2024, pubblicata sul portale istituzionale “Milano Partecipa”.
6. **Streamlit docs** – https://docs.streamlit.io/ per le best practice sull UX e il deployment.
