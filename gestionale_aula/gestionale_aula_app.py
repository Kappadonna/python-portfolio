import streamlit as st

# ── Classe Professore (invariata) ─────────────────────────────────────────────

class Professore:
    def __init__(self, nome: str, cognome: str, materie=None, classi=None):
        self.__nome = nome
        self.__cognome = cognome
        self.__materie = materie if materie is not None else []
        self.__classi = classi if classi is not None else []

    @property
    def nome(self): return self.__nome
    @nome.setter
    def nome(self, v): self.__nome = v

    @property
    def cognome(self): return self.__cognome
    @cognome.setter
    def cognome(self, v): self.__cognome = v

    @property
    def materie(self): return self.__materie

    def aggiungi_materia(self, m):
        if m.lower() not in self.__materie:
            self.__materie.append(m.lower())

    def rimuovi_materia(self, m):
        if m.lower() in self.__materie:
            self.__materie.remove(m.lower())

    @property
    def classi(self): return self.__classi

    def aggiungi_classe(self, c):
        if c.lower() not in self.__classi:
            self.__classi.append(c.lower())

    def rimuovi_classe(self, c):
        if c.lower() in self.__classi:
            self.__classi.remove(c.lower())


# ── Session state init ────────────────────────────────────────────────────────

def init_state():
    if "prof" not in st.session_state:
        st.session_state.prof = None
    if "classi_studenti" not in st.session_state:
        # { nome_classe: {"materia": str, "studenti": [str]} }
        st.session_state.classi_studenti = {}

init_state()

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(page_title="Gestionale Aula", page_icon="🏫", layout="centered")
st.title("🏫 Gestionale Aula")

# ── Step 1: Login professore ──────────────────────────────────────────────────

if st.session_state.prof is None:
    st.subheader("Benvenuto! Inserisci i tuoi dati per iniziare.")
    with st.form("form_prof"):
        nome    = st.text_input("Nome")
        cognome = st.text_input("Cognome")
        submitted = st.form_submit_button("Accedi")
    if submitted:
        if nome.strip() and cognome.strip():
            st.session_state.prof = Professore(
                nome.strip().title(),
                cognome.strip().title()
            )
            st.rerun()
        else:
            st.error("Inserisci nome e cognome per continuare.")
    st.stop()

# ── Header professore ─────────────────────────────────────────────────────────

prof            = st.session_state.prof
classi_studenti = st.session_state.classi_studenti

col_title, col_btn = st.columns([4, 1])
with col_title:
    st.markdown(f"### 👨‍🏫 Prof. {prof.nome} {prof.cognome}")
with col_btn:
    if st.button("🔄 Esci"):
        st.session_state.prof = None
        st.session_state.classi_studenti = {}
        st.rerun()

st.divider()

# ── Tab principali ────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs(["📚 Materie", "🏛️ Classi", "👨‍🎓 Studenti", "📄 Registro"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — MATERIE
# ════════════════════════════════════════════════════════════════════════════════

with tab1:
    st.subheader("Gestione Materie")

    col1, col2 = st.columns(2)

    with col1:
        nuova_materia = st.text_input("Nuova materia", key="nuova_materia")
        if st.button("➕ Aggiungi materia"):
            if nuova_materia.strip():
                prof.aggiungi_materia(nuova_materia.strip())
                st.success(f"Materia '{nuova_materia.lower()}' aggiunta!")
                st.rerun()
            else:
                st.error("Inserisci il nome della materia.")

    with col2:
        if prof.materie:
            da_rimuovere = st.selectbox("Materia da rimuovere", prof.materie, key="rm_materia")
            if st.button("🗑️ Rimuovi materia"):
                prof.rimuovi_materia(da_rimuovere)
                st.success(f"Materia '{da_rimuovere}' rimossa.")
                st.rerun()
        else:
            st.info("Nessuna materia da rimuovere.")

    st.divider()

    if prof.materie:
        st.markdown("**Materie attuali:**")
        for m in prof.materie:
            st.markdown(f"- {m.capitalize()}")
    else:
        st.info("Nessuna materia ancora aggiunta.")

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — CLASSI
# ════════════════════════════════════════════════════════════════════════════════

with tab2:
    st.subheader("Gestione Classi")

    if not prof.materie:
        st.warning("⚠️ Aggiungi almeno una materia prima di creare una classe.")
    else:
        with st.expander("➕ Crea nuova classe", expanded=not bool(prof.classi)):
            nome_classe    = st.text_input("Nome classe (es. 4A)", key="nome_classe")
            materia_classe = st.selectbox("Materia", prof.materie, key="materia_classe")
            n_studenti     = st.number_input(
                "Numero iniziale di studenti", min_value=0, max_value=50, value=0, key="n_studenti"
            )

            studenti_inputs = []
            for i in range(int(n_studenti)):
                s = st.text_input(f"Studente {i + 1}", key=f"stud_init_{i}")
                studenti_inputs.append(s)

            if st.button("✅ Crea classe"):
                nome_classe_clean = nome_classe.strip().upper()
                if not nome_classe_clean:
                    st.error("Inserisci un nome per la classe.")
                elif nome_classe_clean.lower() in prof.classi:
                    st.error("Esiste già una classe con questo nome.")
                elif any(not s.strip() for s in studenti_inputs):
                    st.error("Compila tutti i campi degli studenti.")
                else:
                    studenti = [s.strip().title() for s in studenti_inputs]
                    prof.aggiungi_classe(nome_classe_clean.lower())
                    classi_studenti[nome_classe_clean.lower()] = {
                        "materia": materia_classe,
                        "studenti": studenti,
                    }
                    st.success(f"Classe '{nome_classe_clean}' creata con successo!")
                    st.rerun()

    st.divider()

    if prof.classi:
        st.markdown("**Classi registrate:**")
        for c in prof.classi:
            info    = classi_studenti.get(c, {})
            materia = info.get("materia", "N/D")
            n       = len(info.get("studenti", []))
            col_a, col_b = st.columns([5, 1])
            with col_a:
                st.markdown(
                    f"📋 **{c.upper()}** &nbsp;—&nbsp; {materia.capitalize()} "
                    f"&nbsp;—&nbsp; {n} studenti"
                )
            with col_b:
                if st.button("🗑️", key=f"rm_classe_{c}", help=f"Rimuovi classe {c.upper()}"):
                    prof.rimuovi_classe(c)
                    classi_studenti.pop(c, None)
                    st.rerun()
    else:
        st.info("Nessuna classe ancora creata.")

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — STUDENTI
# ════════════════════════════════════════════════════════════════════════════════

with tab3:
    st.subheader("Gestione Studenti")

    if not prof.classi:
        st.info("Crea prima almeno una classe per gestire gli studenti.")
    else:
        classe_sel = st.selectbox(
            "Seleziona la classe", prof.classi,
            format_func=lambda c: c.upper(), key="classe_studenti"
        )

        info     = classi_studenti.get(classe_sel, {"materia": "", "studenti": []})
        studenti = info["studenti"]

        st.markdown(
            f"**Materia:** {info.get('materia','').capitalize()} &nbsp;|&nbsp; "
            f"**Studenti iscritti:** {len(studenti)}"
        )
        st.divider()

        # Aggiungi studente
        nuovo_stud = st.text_input("Nome e cognome da aggiungere", key="nuovo_stud")
        if st.button("➕ Aggiungi studente"):
            if nuovo_stud.strip():
                nome_stud = nuovo_stud.strip().title()
                if nome_stud not in studenti:
                    studenti.append(nome_stud)
                    st.success(f"'{nome_stud}' aggiunto alla classe {classe_sel.upper()}!")
                    st.rerun()
                else:
                    st.warning("Studente già presente in questa classe.")
            else:
                st.error("Inserisci nome e cognome.")

        st.divider()

        # Elenco studenti
        if studenti:
            st.markdown("**Elenco studenti:**")
            for i, s in enumerate(studenti):
                col_s, col_btn = st.columns([5, 1])
                with col_s:
                    st.markdown(f"{i + 1}. {s}")
                with col_btn:
                    if st.button("🗑️", key=f"rm_stud_{classe_sel}_{i}", help=f"Rimuovi {s}"):
                        studenti.pop(i)
                        st.rerun()
        else:
            st.info("Nessuno studente ancora in questa classe.")

# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — REGISTRO (anteprima file .txt)
# ════════════════════════════════════════════════════════════════════════════════

with tab4:
    st.subheader("Registro classi")

    if not prof.classi:
        st.info("Nessuna classe ancora creata. Crea una classe per visualizzarne il registro.")
    else:
        classe_reg = st.selectbox(
            "Seleziona la classe da visualizzare",
            prof.classi,
            format_func=lambda c: c.upper(),
            key="classe_registro"
        )

        info     = classi_studenti.get(classe_reg, {"materia": "", "studenti": []})
        materia  = info.get("materia", "N/D")
        studenti = info.get("studenti", [])

        # Costruisce il contenuto esattamente come sarebbe nel file .txt
        righe = [
            f"Classe: {classe_reg.upper()}",
            f"Materia: {materia.capitalize()}",
            f"Professore: {prof.nome} {prof.cognome}",
            "",
            "Studenti:",
        ]
        for s in studenti:
            righe.append(f"  - {s}")
        if not studenti:
            righe.append("  (nessuno studente)")

        contenuto_txt = "\n".join(righe)

        st.code(contenuto_txt, language=None)

        st.caption(f"📁 Nome file corrispondente: Aula_{classe_reg.upper()}_{prof.cognome}.txt")