# 🏫 Gestionale Aula — Gestione Classi e Studenti

Sistema di gestione di classi scolastiche e studenti per professori, sviluppato in Python con paradigma **orientato agli oggetti (OOP)**.

---

## 📌 Descrizione

Il programma modella il flusso di lavoro di un professore che gestisce le proprie classi, permettendo di:

- Registrare un professore con le proprie materie di insegnamento
- Creare classi scolastiche associate a una materia
- Aggiungere e rimuovere studenti da ciascuna classe
- Consultare il registro della classe in formato testuale
- Gestire l'intero stato della sessione senza necessità di file su disco

La struttura è costruita attorno alla classe `Professore`, che incapsula nome, cognome, materie e classi attraverso proprietà con getter/setter e metodi di aggiunta/rimozione. Lo stato globale (classi e studenti) viene gestito tramite `st.session_state` nella versione Streamlit.

---

## 📂 File

| File | Contenuto |
|---|---|
| `Creazione_aula.py` | Programma originale con interfaccia testuale (terminale) |
| `gestionale_aula_app.py` | Versione con interfaccia grafica su Streamlit |

---

## 🏗️ Struttura OOP

```
Professore
├── nome, cognome          → proprietà con getter/setter
├── materie                → lista con aggiungi/rimuovi
└── classi                 → lista con aggiungi/rimuovi

Stato globale (session_state)
└── classi_studenti        → { nome_classe: { materia, studenti[] } }
```

---

## ▶️ Come eseguire

**Versione terminale:**
```bash
python Creazione_aula.py
```

**Versione Streamlit:**
```bash
pip install streamlit
streamlit run gestionale_aula_app.py
```

---

## 🎨 Interfaccia Streamlit

La versione grafica include:

- **Schermata di login** — inserimento nome e cognome del professore per avviare la sessione
- **4 tab** principali per separare le funzionalità:
  - 📚 **Materie** — aggiunta e rimozione materie con selectbox
  - 🏛️ **Classi** — creazione classe con studenti iniziali, rimozione con un click
  - 👨‍🎓 **Studenti** — aggiunta e rimozione studenti per classe selezionata
  - 📄 **Registro** — anteprima inline del contenuto che corrisponderebbe al file `.txt`, con indicazione del nome file

---

## 🤖 Nota sull'uso di AI

Il programma originale (`Creazione_aula.py`) — inclusi la struttura OOP, la classe `Professore` con proprietà e metodi, la logica di gestione dei file `.txt` e il menu interattivo da terminale — è stato sviluppato **interamente in autonomia**.

La versione Streamlit (`gestionale_aula_app.py`) è stata realizzata con il supporto di **Claude (Anthropic)**. A partire dal codice originale, Claude ha contribuito a:
- Convertire l'interfaccia testuale in un'app web con Streamlit
- Sostituire la scrittura su file con la gestione dello stato tramite `st.session_state`
- Progettare la struttura a tab e i form interattivi
- Implementare il tab Registro per la visualizzazione inline del contenuto testuale
- Mantenere invariata la classe `Professore` originale senza modifiche alla logica OOP

Questa distinzione riflette un uso trasparente e consapevole degli strumenti AI come supporto allo sviluppo, non come sostituto delle competenze personali.
