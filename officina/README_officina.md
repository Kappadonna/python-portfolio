# 🔧 Officina Masamune — Gestione Riparazioni

Sistema di gestione dei ticket di riparazione per un'officina di elettrodomestici, sviluppato in Python con paradigma **orientato agli oggetti (OOP)**.

---

## 📌 Descrizione

Il programma modella il flusso di lavoro di un'officina tecnica che gestisce riparazioni di tre categorie di elettrodomestici — **Frigorifero**, **Lavatrice** e **Forno** — permettendo di:

- Aprire ticket di riparazione con descrizione del guasto
- Calcolare un preventivo di costo base con extra opzionali (commissioni e IVA)
- Chiudere ticket a riparazione completata
- Aggiungere note tecniche ai ticket
- Visualizzare statistiche per tipo di elettrodomestico

La struttura è costruita attorno a una classe astratta `Elettrodomestico` con un metodo `stima_costo_base()` overridato in ciascuna sottoclasse secondo logiche specifiche. La classe `TicketRiparazione` incapsula ogni intervento, e `Officina` coordina l'insieme.

---

## 📂 File

| File | Contenuto |
|---|---|
| `Officina_Masamune.py` | Programma originale con interfaccia testuale (terminale) |
| `officina_app.py` | Versione con interfaccia grafica su Streamlit |
| `requirements.txt` | Dipendenze Python necessarie |

---

## 🏗️ Struttura OOP

```
Elettrodomestico  (classe astratta)
├── Frigorifero   → costo base su litri e presenza freezer
├── Lavatrice     → costo base su capacità kg
└── Forno         → costo base su alimentazione e ventilazione

TicketRiparazione → incapsula elettrodomestico, stato e preventivo
Officina          → gestisce la lista ticket e le statistiche
```

---


## ▶️ Come eseguire

**Versione terminale:**
```bash
python Officina_Masamune.py
```

**Versione Streamlit:**
```bash
pip install -r requirements.txt
streamlit run officina_app.py
```

---

## 🎨 Interfaccia Streamlit

La versione grafica include:
- **Hero banner** con contatore ticket aperti in tempo reale
- **4 metriche** — ticket totali, aperti, chiusi, valore totale con IVA
- **Lista ticket** con filtro per stato (tutti / aperti / chiusi), badge colorati e note tecniche inline
- **Tabella dettaglio** con evidenziazione stato
- **Preventivo interattivo** — seleziona un ticket e attiva/disattiva commissioni e IVA con aggiornamento immediato della voce di costo
- **Grafico a barre** per tipo di elettrodomestico (Lavatrice / Frigorifero / Forno)

---

## 🤖 Nota sull'uso di AI

Il programma originale (`Officina_Masamune.py`) — inclusi la struttura OOP, la gerarchia di classi, il calcolo del preventivo e il menu interattivo da terminale — è stato sviluppato **interamente in autonomia**.

La versione Streamlit (`officina_app.py`) è stata realizzata con il supporto di **Claude (Anthropic)**. A partire dal codice originale, Claude ha contribuito a:
- Identificare e correggere i bug presenti nell'originale
- Convertire l'interfaccia testuale in un'app web con Streamlit
- Progettare il tema industriale/meccanico (palette acciaio/arancione, font Bebas Neue + IBM Plex Mono)
- Implementare il preventivo interattivo con calcolo dinamico di commissioni e IVA
- Gestire lo stato della sessione con `st.session_state`
- Scrivere il CSS custom per lo stile dell'interfaccia

Questa distinzione riflette un uso trasparente e consapevole degli strumenti AI come supporto allo sviluppo, non come sostituto delle competenze personali.
