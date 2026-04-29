from abc import ABC, abstractmethod
import datetime
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────
#  MODELLO — con bug fix rispetto all'originale
# ─────────────────────────────────────────────

anno_corrente = datetime.date.today().year


class Elettrodomestico(ABC):

    def __init__(self, marca: str, modello: str, anno_acquisto: int, guasto: str):
        self.__marca = marca
        self.__modello = modello
        self.__anno_acquisto = anno_acquisto
        self.__guasto = guasto

    def descrizione(self):
        return (
            f"Marca: {self.get_marca()} | Modello: {self.get_modello()} | "
            f"Anno: {self.get_anno_acquisto()} | Guasto: {self.get_guasto()}"
        )

    def stima_costo_base(self):
        return 50

    def get_marca(self):
        return self.__marca
    
    def get_modello(self):
        return self.__modello
    
    def get_anno_acquisto(self):
        return self.__anno_acquisto
    
    def get_guasto(self):
        return self.__guasto

    def set_marca(self, marca):
        self.__marca = marca
        
    def set_modello(self, modello):
        self.__modello = modello
        
    def set_guasto(self, guasto):
        self.__guasto = guasto

    def set_anno_acquisto(self, anno):
        if anno <= anno_corrente:
            self.__anno_acquisto = anno
        else:
            raise ValueError("L'anno di acquisto non può essere nel futuro.")


class Forno(Elettrodomestico):

    ICON = "🔥"

    def __init__(self, marca, modello, anno_acquisto, guasto,
                 tipo_alimentazione: str, ha_ventilato: bool):
        super().__init__(marca, modello, anno_acquisto, guasto)
        self.tipo_alimentazione = tipo_alimentazione
        self.ha_ventilato = ha_ventilato

    def stima_costo_base(self):
        base = super().stima_costo_base()
        if self.tipo_alimentazione == "elettrico":
            return base + (25 if self.ha_ventilato else 15)
        else:
            return base + (20 if self.ha_ventilato else 10)

    def descrizione(self):
        return (
            super().descrizione() +
            f" | Alim.: {self.tipo_alimentazione} | Ventilato: {'Sì' if self.ha_ventilato else 'No'}"
        )

    def tipo(self): return "Forno"


class Frigorifero(Elettrodomestico):

    ICON = "🧊"

    def __init__(self, marca, modello, anno_acquisto, guasto,
                 litri: int, ha_freezer: bool):
        super().__init__(marca, modello, anno_acquisto, guasto)
        self.litri = litri
        self.ha_freezer = ha_freezer

    def stima_costo_base(self):
        base = super().stima_costo_base()
        freezer_extra = 30 if self.ha_freezer else 0
        if self.litri > 50:
            return base + 30 + freezer_extra
        elif self.litri > 25:
            return base + 10 + freezer_extra
        else:
            return base + freezer_extra

    def descrizione(self):
        return (
            super().descrizione() +
            f" | Capacità: {self.litri}L | Freezer: {'Sì' if self.ha_freezer else 'No'}"
        )

    def tipo(self):
        return "Frigorifero"


class Lavatrice(Elettrodomestico):

    ICON = "🌀"
    soglia_capacita_alta = 8

    def __init__(self, marca, modello, anno_acquisto, guasto,
                 capacita_kg: int, giri_centrifuga: int):
        super().__init__(marca, modello, anno_acquisto, guasto)
        self.capacita_kg = capacita_kg
        self.giri_centrifuga = giri_centrifuga

    def stima_costo_base(self):
        costo = super().stima_costo_base()
        if self.capacita_kg > self.soglia_capacita_alta:
            costo += 20
        return costo

    def descrizione(self):
        return (
            super().descrizione() +
            f" | Capacità: {self.capacita_kg} kg | Centrifuga: {self.giri_centrifuga} giri/min"
        )

    def tipo(self):
        return "Lavatrice"


class TicketRiparazione:

    #ID_TICKET = 0

    def __init__(self, elettrodomestico: Elettrodomestico, stato=None, note=None):
        #TicketRiparazione.ID_TICKET += 1
        #self.__id_ticket = TicketRiparazione.ID_TICKET
        st.session_state.ticket_counter += 1
        self.__id_ticket = st.session_state.ticket_counter
        self.__elettrodomestico = elettrodomestico
        self.__stato = stato if stato is not None else "aperto"
        self.__note = note if note is not None else ["-"]

    def calcola_preventivo(self, commissioni=False, iva=False):
        costo = self.__elettrodomestico.stima_costo_base()
        if commissioni:
            costo += 10
        if iva:
            costo *= 1.22
        return round(costo, 2)

    def get_id(self):
        return self.__id_ticket
    def get_elettrodomestico(self):
        return self.__elettrodomestico
    def get_stato(self):
        return self.__stato
    def get_note(self):
        return self.__note

    def set_stato(self, stato):
        self.__stato = stato

    def aggiungi_nota(self, nota: str):
        self.__note.append(nota)


class Officina:

    def __init__(self, nome):
        self.nome = nome
        self.tickets = []

    def aggiungi_ticket(self, ticket: TicketRiparazione):
        self.tickets.append(ticket)

    def chiudi_ticket(self, id_ticket):
        for t in self.tickets:
            if t.get_id() == id_ticket:
                t.set_stato("chiuso")
                return True
        return False

    def get_tickets_aperti(self):
        return [t for t in self.tickets if t.get_stato() == "aperto"]

    def get_tickets_chiusi(self):
        return [t for t in self.tickets if t.get_stato() == "chiuso"]

    def totale_preventivi(self, commissioni=False, iva=False):
        return round(sum(t.calcola_preventivo(commissioni, iva) for t in self.tickets), 2)

    def statistiche_per_tipo(self):
        return {
            "Lavatrice":    sum(1 for t in self.tickets if isinstance(t.get_elettrodomestico(), Lavatrice)),
            "Frigorifero":  sum(1 for t in self.tickets if isinstance(t.get_elettrodomestico(), Frigorifero)),
            "Forno":        sum(1 for t in self.tickets if isinstance(t.get_elettrodomestico(), Forno)),
        }


# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Officina Masamune",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS — TEMA INDUSTRIALE/MECCANICO
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@300;400;500;600&display=swap');

:root {
    --bg:        #111214;
    --steel:     #1c1f23;
    --steel2:    #252a30;
    --plate:     #2e3338;
    --border:    #3a4048;
    --border2:   #505860;
    --orange:    #f07000;
    --orange2:   #ff8c1a;
    --yellow:    #f5c518;
    --red:       #c0392b;
    --green:     #27ae60;
    --cream:     #e8e0d4;
    --muted:     #7a8290;
    --font-disp: 'Bebas Neue', Impact, sans-serif;
    --font-mono: 'IBM Plex Mono', 'Courier New', monospace;
}

/* ── BASE ── */
[data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--cream);
    font-family: var(--font-mono);
}
/* Diagonal stripe texture on background */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: repeating-linear-gradient(
        45deg,
        transparent,
        transparent 40px,
        rgba(255,255,255,.012) 40px,
        rgba(255,255,255,.012) 41px
    );
    pointer-events: none;
    z-index: 0;
}
[data-testid="stSidebar"] {
    background: var(--steel);
    border-right: 2px solid var(--orange);
}
[data-testid="stSidebar"] * { color: var(--cream) !important; }

/* ── HERO ── */
.hero {
    background: var(--steel);
    border: 1px solid var(--border);
    border-left: 5px solid var(--orange);
    border-radius: 4px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '⚙';
    position: absolute;
    right: 1.5rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: .06;
    line-height: 1;
}
.hero-tag {
    font-family: var(--font-mono);
    font-size: .65rem;
    letter-spacing: .25em;
    text-transform: uppercase;
    color: var(--orange);
    margin-bottom: .3rem;
}
.hero-title {
    font-family: var(--font-disp);
    font-size: 3.2rem;
    letter-spacing: .08em;
    color: var(--cream);
    line-height: 1;
}
.hero-sub {
    font-size: .72rem;
    color: var(--muted);
    letter-spacing: .1em;
    margin-top: .3rem;
}
.hero-badge {
    background: var(--orange);
    color: #fff;
    font-family: var(--font-disp);
    font-size: 1.4rem;
    letter-spacing: .1em;
    padding: .4rem 1rem;
    border-radius: 3px;
    white-space: nowrap;
}

/* ── METRIC CARDS ── */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: .7rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: var(--steel);
    border: 1px solid var(--border);
    border-top: 3px solid var(--orange);
    border-radius: 3px;
    padding: .9rem 1.1rem;
    position: relative;
}
.metric-label {
    font-size: .62rem;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .35rem;
}
.metric-val {
    font-family: var(--font-disp);
    font-size: 2.2rem;
    letter-spacing: .04em;
    color: var(--cream);
    line-height: 1;
}
.metric-val.orange { color: var(--orange2); }
.metric-val.green  { color: var(--green); }
.metric-val.red    { color: var(--red); }
.metric-icon {
    position: absolute;
    right: .9rem; top: .8rem;
    font-size: 1.3rem;
    opacity: .3;
}

/* ── SECTION ── */
.sec-title {
    font-family: var(--font-disp);
    font-size: 1.3rem;
    letter-spacing: .12em;
    color: var(--cream);
    border-bottom: 2px solid var(--border);
    padding-bottom: .4rem;
    margin: 1.2rem 0 .8rem;
    display: flex;
    align-items: center;
    gap: .6rem;
}
.sec-title::before { content: '//'; color: var(--orange); font-size: 1rem; }

/* ── TICKET CARDS ── */
.ticket-card {
    background: var(--steel);
    border: 1px solid var(--border);
    border-left: 4px solid var(--orange);
    border-radius: 3px;
    padding: .85rem 1.1rem;
    margin-bottom: .55rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.ticket-card.chiuso {
    border-left-color: var(--border2);
    opacity: .55;
}
.ticket-id {
    font-family: var(--font-disp);
    font-size: 1.6rem;
    color: var(--orange);
    min-width: 2.5rem;
    text-align: center;
}
.ticket-id.chiuso { color: var(--muted); }
.ticket-info { flex: 1; }
.ticket-tipo {
    font-size: .72rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--muted);
}
.ticket-desc {
    font-size: .82rem;
    color: var(--cream);
    margin-top: .15rem;
    font-family: var(--font-mono);
}
.stato-badge {
    font-family: var(--font-disp);
    font-size: .85rem;
    letter-spacing: .1em;
    padding: .2rem .7rem;
    border-radius: 2px;
    text-transform: uppercase;
}
.stato-badge.aperto  { background: #1a3a1a; color: var(--green); border: 1px solid var(--green); }
.stato-badge.chiuso  { background: var(--plate); color: var(--muted); border: 1px solid var(--border); }

/* ── NOTIFICHE ── */
.notif-ok  { background:#0d2014; border:1px solid #1e5a30; border-left:3px solid var(--green); border-radius:3px; padding:.65rem 1rem; color:#4ade80; font-size:.82rem; margin:.5rem 0; font-family:var(--font-mono); }
.notif-err { background:#2a0d0a; border:1px solid #6b1e1e; border-left:3px solid var(--red); border-radius:3px; padding:.65rem 1rem; color:#f87171; font-size:.82rem; margin:.5rem 0; font-family:var(--font-mono); }
.notif-info{ background:#1a1200; border:1px solid #5a4000; border-left:3px solid var(--yellow); border-radius:3px; padding:.65rem 1rem; color:var(--yellow); font-size:.82rem; margin:.5rem 0; font-family:var(--font-mono); }

/* ── PREVENTIVO BOX ── */
.preventivo-box {
    background: var(--steel2);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 1.2rem 1.4rem;
}
.preventivo-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: .35rem 0;
    border-bottom: 1px dashed var(--border);
    font-size: .82rem;
}
.preventivo-row:last-child { border-bottom: none; }
.preventivo-row .label { color: var(--muted); letter-spacing: .08em; }
.preventivo-row .val   { font-family: var(--font-disp); font-size: 1.2rem; color: var(--orange2); }
.preventivo-total {
    font-family: var(--font-disp);
    font-size: 2rem;
    color: var(--orange);
    text-align: right;
    padding-top: .5rem;
    letter-spacing: .05em;
}

/* ── SIDEBAR OVERRIDES ── */
.sidebar-logo {
    font-family: var(--font-disp);
    font-size: 1.8rem;
    letter-spacing: .12em;
    color: var(--cream);
    line-height: 1;
}
.sidebar-sub {
    font-size: .62rem;
    letter-spacing: .2em;
    color: var(--orange);
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.stSelectbox label, .stNumberInput label,
.stTextInput label, .stRadio label,
.stTextArea label, .stCheckbox label {
    font-size: .68rem !important;
    letter-spacing: .15em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    font-family: var(--font-mono) !important;
}
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
textarea {
    background: var(--steel2) !important;
    border: 1px solid var(--border) !important;
    color: var(--cream) !important;
    border-radius: 2px !important;
    font-family: var(--font-mono) !important;
    font-size: .85rem !important;
}
.stButton > button {
    background: var(--orange) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: var(--font-disp) !important;
    font-size: 1rem !important;
    letter-spacing: .15em !important;
    padding: .5rem 1.2rem !important;
    width: 100%;
    transition: background .2s !important;
}
.stButton > button:hover { background: var(--orange2) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────

if "officina" not in st.session_state:
    st.session_state.officina = Officina("Masamune")
if "notifica" not in st.session_state:
    st.session_state.notifica = None
if "ticket_counter" not in st.session_state:
    st.session_state.ticket_counter = 0


officina: Officina = st.session_state.officina


def set_notif(tipo, msg):
    st.session_state.notifica = (tipo, msg)


def show_notif():
    if st.session_state.notifica:
        tipo, msg = st.session_state.notifica
        css = {"ok": "notif-ok", "err": "notif-err", "info": "notif-info"}.get(tipo, "notif-info")
        st.markdown(f'<div class="{css}">{msg}</div>', unsafe_allow_html=True)
        st.session_state.notifica = None


# ─────────────────────────────────────────────
#  SIDEBAR — AZIONI
# ─────────────────────────────────────────────

TIPO_MAP = {"Frigorifero 🧊": "Frigorifero", "Lavatrice 🌀": "Lavatrice", "Forno 🔥": "Forno"}

with st.sidebar:
    st.markdown('<div class="sidebar-logo">🔧 MASAMUNE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Officina di riparazione</div>', unsafe_allow_html=True)

    azione = st.selectbox("Azione", [
        "📋  Nuovo ticket",
        "✅  Chiudi ticket",
        "📝  Aggiungi nota",
    ])

    st.markdown("---")

    # ── NUOVO TICKET ─────────────────────────────
    if azione == "📋  Nuovo ticket":
        tipo_sel = st.selectbox("Tipo elettrodomestico", list(TIPO_MAP.keys()))
        tipo = TIPO_MAP[tipo_sel]

        marca    = st.text_input("Marca")
        modello  = st.text_input("Modello")
        anno_acq = st.number_input("Anno di acquisto", min_value=1950,
                                   max_value=anno_corrente, value=2020, step=1)
        guasto   = st.text_input("Descrizione guasto")

        # Campi specifici per tipo
        if tipo == "Frigorifero":
            litri      = st.number_input("Capacità (litri)", min_value=1, value=200, step=10)
            ha_freezer = st.checkbox("Ha il freezer")
        elif tipo == "Lavatrice":
            capacita   = st.number_input("Capacità (kg)", min_value=1, value=7, step=1)
            giri       = st.number_input("Giri centrifuga (giri/min)", min_value=400, value=1000, step=100)
        else:  # Forno
            alimentazione = st.selectbox("Alimentazione", ["elettrico", "gas"])
            ventilato     = st.checkbox("Forno ventilato")

        if st.button("Apri Ticket"):
            if not marca or not modello or not guasto:
                set_notif("err", "⚠ Compila tutti i campi obbligatori.")
            else:
                try:
                    if tipo == "Frigorifero":
                        el = Frigorifero(marca, modello, anno_acq, guasto, litri, ha_freezer)
                    elif tipo == "Lavatrice":
                        el = Lavatrice(marca, modello, anno_acq, guasto, capacita, giri)
                    else:
                        el = Forno(marca, modello, anno_acq, guasto, alimentazione, ventilato)
                    ticket = TicketRiparazione(el)
                    #officina.aggiungi_ticket(ticket)
                    st.session_state.officina.aggiungi_ticket(ticket)
                    set_notif("ok", f"✔ Ticket #{ticket.get_id()} aperto — {tipo} {marca} {modello}")
                    st.rerun()
                except ValueError as e:
                    set_notif("err", f"⚠ {e}")

    # ── CHIUDI TICKET ────────────────────────────
    elif azione == "✅  Chiudi ticket":
        aperti = officina.get_tickets_aperti()
        if not aperti:
            st.markdown('<div class="notif-info">Nessun ticket aperto.</div>', unsafe_allow_html=True)
        else:
            opzioni = {f"#{t.get_id()} — {t.get_elettrodomestico().tipo()} {t.get_elettrodomestico().get_marca()}": t.get_id()
                       for t in aperti}
            sel = st.selectbox("Seleziona ticket", list(opzioni.keys()))
            if st.button("Chiudi Ticket"):
                ok = officina.chiudi_ticket(opzioni[sel])
                set_notif("ok" if ok else "err",
                          f"✔ Ticket {sel} chiuso." if ok else "⚠ Ticket non trovato.")
                st.rerun()

    # ── AGGIUNGI NOTA ────────────────────────────
    else:
        tutti = officina.tickets
        if not tutti:
            st.markdown('<div class="notif-info">Nessun ticket presente.</div>', unsafe_allow_html=True)
        else:
            opzioni = {f"#{t.get_id()} — {t.get_elettrodomestico().tipo()}": t for t in tutti}
            sel = st.selectbox("Seleziona ticket", list(opzioni.keys()))
            nota = st.text_area("Nota", placeholder="Inserisci la nota tecnica...")
            if st.button("Aggiungi Nota"):
                if nota.strip():
                    opzioni[sel].aggiungi_nota(nota.strip())
                    set_notif("ok", f"✔ Nota aggiunta al ticket {sel}.")
                    st.rerun()
                else:
                    set_notif("err", "⚠ La nota non può essere vuota.")


# ─────────────────────────────────────────────
#  MAIN — DASHBOARD
# ─────────────────────────────────────────────

# ── HERO ─────────────────────────────────────
n_tot    = len(officina.tickets)
n_aperti = len(officina.get_tickets_aperti())
n_chiusi = len(officina.get_tickets_chiusi())

st.markdown(f"""
<div class="hero">
    <div>
        <div class="hero-tag">// Sistema Gestione Riparazioni</div>
        <div class="hero-title">OFFICINA MASAMUNE</div>
        <div class="hero-sub">Gestione ticket · Preventivi · Statistiche</div>
    </div>
    <div class="hero-badge">{n_aperti} APERTI</div>
</div>
""", unsafe_allow_html=True)

show_notif()

# ── METRICHE ─────────────────────────────────
tot_base  = officina.totale_preventivi()
tot_iva   = officina.totale_preventivi(commissioni=True, iva=True)
stats     = officina.statistiche_per_tipo()

st.markdown(f"""
<div class="metrics-row">
    <div class="metric-card">
        <div class="metric-label">Ticket totali</div>
        <div class="metric-val">{n_tot}</div>
        <div class="metric-icon">📋</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Ticket aperti</div>
        <div class="metric-val orange">{n_aperti}</div>
        <div class="metric-icon">🔧</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Ticket chiusi</div>
        <div class="metric-val green">{n_chiusi}</div>
        <div class="metric-icon">✅</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Valore flotta (IVA incl.)</div>
        <div class="metric-val orange">€{tot_iva:,.0f}</div>
        <div class="metric-icon">💶</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── LAYOUT ────────────────────────────────────
col_left, col_right = st.columns([3, 2], gap="large")

# ── TICKET LIST + FILTRI ─────────────────────
with col_left:
    st.markdown('<div class="sec-title">Ticket</div>', unsafe_allow_html=True)

    filtro = st.radio("Mostra:", ["Tutti", "Aperti", "Chiusi"],
                      horizontal=True, label_visibility="collapsed")

    if filtro == "Aperti":
        lista = officina.get_tickets_aperti()
    elif filtro == "Chiusi":
        lista = officina.get_tickets_chiusi()
    else:
        lista = officina.tickets

    if not lista:
        st.markdown('<div class="notif-info">Nessun ticket da mostrare. Usa la sidebar per aprirne uno.</div>',
                    unsafe_allow_html=True)
    else:
        for t in reversed(lista):
            el = t.get_elettrodomestico()
            stato = t.get_stato()
            card_cls = "ticket-card" + (" chiuso" if stato == "chiuso" else "")
            id_cls   = "ticket-id"  + (" chiuso" if stato == "chiuso" else "")
            badge_cls = f"stato-badge {stato}"
            note_html = ""
            if t.get_note():
                note_html = (
                    "<div style='margin-top:.4rem;font-size:.72rem;color:#7a8290;'>"
                    + " &nbsp;·&nbsp; ".join(t.get_note()) + "</div>"
                )
            st.markdown(f"""
            <div class="{card_cls}">
                <div class="{id_cls}">#{t.get_id()}</div>
                <div class="ticket-info">
                    <div class="ticket-tipo">{el.ICON} {el.tipo()}</div>
                    <div class="ticket-desc">{el.get_marca()} {el.get_modello()} · {el.get_guasto()}</div>
                    {note_html}
                </div>
                <div>
                    <span class="{badge_cls}">{stato}</span>
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;
                                color:#f07000;text-align:right;margin-top:.3rem;">
                        €{t.calcola_preventivo():,.0f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── TABELLA DETTAGLIO ─────────────────────
    if lista:
        st.markdown('<div class="sec-title">Tabella Dettaglio</div>', unsafe_allow_html=True)
        rows = []
        for t in lista:
            el = t.get_elettrodomestico()
            rows.append({
                "ID":       t.get_id(),
                "Tipo":     el.tipo(),
                "Marca":    el.get_marca(),
                "Modello":  el.get_modello(),
                "Anno":     el.get_anno_acquisto(),
                "Guasto":   el.get_guasto(),
                "Stato":    t.get_stato().capitalize(),
                "Base (€)": el.stima_costo_base(),
            })
        df = pd.DataFrame(rows)

        def color_stato(val):
            if val == "Aperto":
                return "color: #27ae60; font-weight:600"
            return "color: #7a8290"

        st.dataframe(
            df.style.applymap(color_stato, subset=["Stato"]),
            use_container_width=True,
            hide_index=True,
        )

# ── PREVENTIVO + GRAFICO ─────────────────────
with col_right:

    # Preventivo interattivo
    st.markdown('<div class="sec-title">Preventivo Interattivo</div>', unsafe_allow_html=True)

    if not officina.tickets:
        st.markdown('<div class="notif-info">Nessun ticket per calcolare il preventivo.</div>',
                    unsafe_allow_html=True)
    else:
        opz = {f"#{t.get_id()} — {t.get_elettrodomestico().tipo()} {t.get_elettrodomestico().get_marca()}": t
               for t in officina.tickets}
        sel_prev = st.selectbox("Ticket", list(opz.keys()), key="prev_sel")
        t_sel = opz[sel_prev]
        el_sel = t_sel.get_elettrodomestico()

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            commissioni = st.checkbox("Commissioni (+€10)")
        with col_c2:
            iva = st.checkbox("IVA 22%")

        costo_base  = el_sel.stima_costo_base()
        comm_val    = 10 if commissioni else 0
        imponibile  = costo_base + comm_val
        iva_val     = round(imponibile * 0.22, 2) if iva else 0
        totale      = round(imponibile + iva_val, 2)

        st.markdown(f"""
        <div class="preventivo-box">
            <div class="preventivo-row">
                <span class="label">COSTO BASE</span>
                <span class="val">€{costo_base:.2f}</span>
            </div>
            <div class="preventivo-row">
                <span class="label">COMMISSIONI</span>
                <span class="val">€{comm_val:.2f}</span>
            </div>
            <div class="preventivo-row">
                <span class="label">IVA 22%</span>
                <span class="val">€{iva_val:.2f}</span>
            </div>
            <div class="preventivo-total">TOTALE &nbsp; €{totale:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Grafico statistiche per tipo
    st.markdown('<div class="sec-title">Statistiche per Tipo</div>', unsafe_allow_html=True)

    if not officina.tickets:
        st.markdown('<div class="notif-info">Nessun dato disponibile.</div>', unsafe_allow_html=True)
    else:
        labels  = list(stats.keys())
        values  = list(stats.values())
        icons   = ["🌀", "🧊", "🔥"]
        colors  = ["#f07000", "#3a8fc0", "#c0392b"]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[f"{ic} {lb}" for ic, lb in zip(icons, labels)],
            y=values,
            marker=dict(color=colors, line=dict(width=0)),
            text=values,
            textposition="outside",
            textfont=dict(family="Bebas Neue", size=18, color="#e8e0d4"),
            hovertemplate="<b>%{x}</b><br>Ticket: %{y}<extra></extra>",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#1c1f23",
            font=dict(family="IBM Plex Mono", color="#7a8290", size=11),
            xaxis=dict(tickfont=dict(family="IBM Plex Mono", size=12, color="#e8e0d4"),
                       gridcolor="#2e3338", showgrid=False, linecolor="#3a4048"),
            yaxis=dict(tickfont=dict(size=11), gridcolor="#2e3338",
                       linecolor="#3a4048", dtick=1),
            margin=dict(l=10, r=10, t=20, b=10),
            height=260,
            showlegend=False,
            bargap=0.4,
        )
        st.plotly_chart(fig, use_container_width=True)
