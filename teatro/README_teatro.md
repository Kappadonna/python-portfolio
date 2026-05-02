# 🎭 Sistema di Prenotazione — Teatro

Sistema di gestione delle prenotazioni di un teatro, sviluppato in Python con paradigma **orientato agli oggetti (OOP)**.

---

## 📌 Descrizione

Il programma modella la sala di un teatro composta da due tipologie di posti — **Standard** e **VIP** — permettendo di:

- Prenotare e liberare posti, con controllo automatico sulla disponibilità
- Aggiungere servizi extra per i posti VIP (accesso al lounge, servizio in posto)
- Calcolare il costo associato a ciascun posto Standard
- Visualizzare lo stato aggiornato di tutti i posti occupati

La struttura è costruita attorno a una classe base (`Posto`) con override del metodo `prenota()` nelle sottoclassi, ognuna delle quali estende il comportamento in modo specifico. La classe `Teatro` coordina l'insieme dei posti e le operazioni di ricerca e gestione.

---

## 📂 File

| File | Contenuto |
|---|---|
| `Teatro_v3.py` | Programma originale con interfaccia testuale (terminale) |
| `teatro_app.py` | Versione con interfaccia grafica su Streamlit |
| `requirements.txt` | Dipendenze Python necessarie |

---

## 🏗️ Struttura OOP

```
Posto  (classe base)
├── PostoStandard   → override prenota() con stampa del costo
└── PostoVIP        → override prenota() con selezione servizi extra

Teatro              → gestisce la lista dei posti
```

---

## ▶️ Come eseguire

**Versione terminale:**
```bash
python Teatro_v3.py
```

**Versione Streamlit:**
```bash
pip install -r requirements.txt
streamlit run teatro_app.py
```

---

## 🎨 Interfaccia Streamlit

La versione grafica include:
- **Dashboard statistiche** — posti totali, occupati, disponibili e incasso stimato
- **Mappa visiva della sala** — griglia interattiva con colori distinti per tipo e stato del posto (Standard libero/occupato, VIP libero/occupato), organizzata per fila con il palco in evidenza
- **Tabella di dettaglio** — elenco completo dei posti con stato, costo e servizi VIP selezionati
- **Sidebar di prenotazione** — form per prenotare nuovi posti (con selezione servizi VIP opzionale) e liberare posti già occupati

---

## 🤖 Nota sull'uso di AI

Il programma originale (`Teatro_v3.py`) — inclusi la struttura OOP, la gerarchia di classi, il meccanismo di override di `prenota()` e il menu interattivo da terminale — è stato sviluppato **interamente in autonomia**.

La versione Streamlit (`teatro_app.py`) è stata realizzata con il supporto di **Claude (Anthropic)**. A partire dal codice originale, Claude ha contribuito a:
- Convertire l'interfaccia testuale in un'app web con Streamlit
- Progettare il tema teatrale art déco (palette borgogna/oro, tipografia Playfair Display)
- Implementare la mappa visiva della sala con griglia CSS dinamica
- Gestire lo stato della sessione con `st.session_state`
- Scrivere il CSS custom per lo stile dell'interfaccia

Questa distinzione riflette un uso trasparente e consapevole degli strumenti AI come supporto allo sviluppo, non come sostituto delle competenze personali.


# MODIFICARE LOGICA. 
# INSERIRE COSTO PER TUTTI I TIPI DI BIGLIETTO, A SECONDA DELLA FILA E DEL TIPO DI BIGLIETTO
# DARE UNA MAPPA INIZIALE
