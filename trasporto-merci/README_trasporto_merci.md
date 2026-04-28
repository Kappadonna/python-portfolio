# 🚛 Gestione Flotta — Trasporto Merci

Sistema di gestione di una flotta di veicoli per il trasporto merci, sviluppato in Python con paradigma **orientato agli oggetti (OOP)**.

---

## 📌 Descrizione

Il programma modella una flotta composta da tre tipologie di veicoli — **Camion**, **Furgone** e **Motocarro** — permettendo di:

- Aggiungere e rimuovere veicoli dalla flotta
- Caricare e scaricare merci, con controllo automatico dei limiti
- Calcolare il costo di manutenzione per ciascun veicolo e per l'intera flotta
- Visualizzare lo stato aggiornato di tutti i veicoli

La struttura è costruita attorno a una classe astratta base (`VeicoloTrasporto`) con metodi concreti condivisi e un metodo astratto (`costo_manutenzione`) implementato da ciascuna sottoclasse in modo specifico. La classe `GestoreFlotta` coordina l'insieme dei veicoli.

---

## 📂 File

| File | Contenuto |
|---|---|
| `Trasporto_merci.py` | Programma originale con interfaccia testuale (terminale) |
| `trasporto_merci_app.py` | Versione con interfaccia grafica su Streamlit |

---

## 🏗️ Struttura OOP

```
VeicoloTrasporto  (classe astratta)
├── Camion          → costo basato su numero assi e peso massimo
├── Furgone         → costo basato sul tipo di alimentazione
└── Motocarro       → costo basato sugli anni di servizio

GestoreFlotta       → gestisce la lista di veicoli
```

---

## ▶️ Come eseguire

**Versione terminale:**
```bash
python Trasporto_merci.py
```

**Versione Streamlit:**
```bash
pip install streamlit plotly pandas
streamlit run trasporto_merci_app.py
```

---

## 🤖 Nota sull'uso di AI

Il programma originale (`Trasporto_merci.py`) — inclusi la struttura OOP, la logica di business, i metodi e il menu interattivo da terminale — è stato sviluppato **interamente in autonomia**.

La versione Streamlit (`trasporto_merci_app.py`) è stata realizzata con il supporto di **Claude (Anthropic)**. A partire dal codice originale, Claude ha contribuito a:
- Convertire l'interfaccia testuale in un'app web con Streamlit
- Progettare il layout della dashboard (metriche, schede veicolo, tabella)
- Implementare il grafico interattivo con Plotly
- Gestire lo stato della sessione con `st.session_state`
- Scrivere il CSS custom per lo stile dell'interfaccia

Questa distinzione riflette un uso trasparente e consapevole degli strumenti AI come supporto allo sviluppo, non come sostituto delle competenze personali.
