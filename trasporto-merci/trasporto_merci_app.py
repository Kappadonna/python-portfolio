from abc import ABC, abstractmethod
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────
#  MODELLO (invariato rispetto all'originale)
# ─────────────────────────────────────────────

class VeicoloTrasporto(ABC):
    def __init__(self, targa, peso_massimo, carico_attuale=0):
        self._targa = targa
        self._peso_massimo = peso_massimo
        self._carico_attuale = carico_attuale

    def carica(self, peso):
        if self._carico_attuale + peso <= self._peso_massimo:
            self._carico_attuale += peso
            return True, f"✅ Caricati {peso} kg sul veicolo {self._targa}."
        return False, "⚠️ Carico superiore al limite massimo."

    def scarica(self, peso):
        if self._carico_attuale >= peso:
            self._carico_attuale -= peso
            return True, f"✅ Scaricati {peso} kg dal veicolo {self._targa}."
        return False, "⚠️ Peso da scaricare superiore al carico attuale."

    @abstractmethod
    def costo_manutenzione(self): pass

    def get_targa(self):          return self._targa
    def get_peso_massimo(self):   return self._peso_massimo
    def get_carico_attuale(self): return self._carico_attuale
    def set_carico_attuale(self, v):
        if 0 <= v <= self._peso_massimo:
            self._carico_attuale = v


class Camion(VeicoloTrasporto):
    ICON = "🚛"
    def __init__(self, targa, peso_massimo, carico_attuale, numero_assi):
        super().__init__(targa, peso_massimo, carico_attuale)
        self._numero_assi = numero_assi
    def costo_manutenzione(self):
        return self._numero_assi * 100 + self._peso_massimo
    def get_numero_assi(self): return self._numero_assi
    def tipo(self): return "Camion"
    def extra(self): return f"{self._numero_assi} assi"


class Furgone(VeicoloTrasporto):
    ICON = "🚐"
    def __init__(self, targa, peso_massimo, carico_attuale, alimentazione):
        super().__init__(targa, peso_massimo, carico_attuale)
        self._alimentazione = alimentazione
    def costo_manutenzione(self):
        return 200 if self._alimentazione == "elettrico" else 150
    def get_alimentazione(self): return self._alimentazione
    def tipo(self): return "Furgone"
    def extra(self): return self._alimentazione.capitalize()


class Motocarro(VeicoloTrasporto):
    ICON = "🛺"
    def __init__(self, targa, peso_massimo, carico_attuale, anni_servizio):
        super().__init__(targa, peso_massimo, carico_attuale)
        self._anni_servizio = anni_servizio
    def costo_manutenzione(self):
        return self._anni_servizio * 50
    def get_anni_servizio(self): return self._anni_servizio
    def tipo(self): return "Motocarro"
    def extra(self): return f"{self._anni_servizio} anni serv."


class GestoreFlotta:
    def __init__(self):
        self._veicoli = []

    def aggiungi_veicolo(self, v: VeicoloTrasporto):
        self._veicoli.append(v)

    def rimuovi_veicolo(self, targa):
        before = len(self._veicoli)
        self._veicoli = [v for v in self._veicoli if v.get_targa() != targa]
        return len(self._veicoli) < before

    def costo_totale(self):
        return sum(v.costo_manutenzione() for v in self._veicoli)

    def get_veicoli(self):
        return self._veicoli

    def trova(self, targa):
        for v in self._veicoli:
            if v.get_targa() == targa:
                return v
        return None

    def targa_esistente(self, targa):
        return any(v.get_targa() == targa for v in self._veicoli)


# ─────────────────────────────────────────────
#  CONFIGURAZIONE PAGINA
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Fleet Manager",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS CUSTOM
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&family=DM+Mono:wght@400;500&display=swap');

/* Sfondo principale */
[data-testid="stAppViewContainer"] {
    background: #0d0f14;
    color: #e8e4dc;
    font-family: 'DM Mono', monospace;
}
[data-testid="stSidebar"] {
    background: #13161e;
    border-right: 1px solid #2a2e3d;
}
[data-testid="stSidebar"] * {
    color: #e8e4dc !important;
}

/* Titolo hero */
.hero-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 3.2rem;
    font-weight: 700;
    letter-spacing: .04em;
    color: #f5f0e8;
    line-height: 1;
    margin-bottom: .25rem;
}
.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: .78rem;
    color: #e55c00;
    letter-spacing: .18em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* Card metrica custom */
.metric-card {
    background: #181c25;
    border: 1px solid #252a38;
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: #e55c00;
}
.metric-label {
    font-size: .68rem;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: #7a7f94;
    margin-bottom: .35rem;
}
.metric-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #f5f0e8;
}
.metric-icon {
    font-size: 1.6rem;
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    opacity: .25;
}

/* Veicolo card */
.veicolo-card {
    background: #181c25;
    border: 1px solid #252a38;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: .6rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color .2s;
}
.veicolo-card:hover { border-color: #e55c00; }
.veicolo-icon { font-size: 2rem; }
.veicolo-info { flex: 1; }
.veicolo-targa {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #f5f0e8;
    letter-spacing: .08em;
}
.veicolo-detail {
    font-size: .72rem;
    color: #7a7f94;
    letter-spacing: .05em;
}
.badge {
    background: #e55c00;
    color: #fff;
    font-size: .65rem;
    font-weight: 600;
    padding: .15rem .5rem;
    border-radius: 20px;
    letter-spacing: .08em;
    text-transform: uppercase;
}

/* Progress bar */
.progress-wrap {
    background: #252a38;
    border-radius: 4px;
    height: 6px;
    margin-top: .4rem;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 4px;
    transition: width .4s;
}

/* Notification */
.notif-ok  { background:#0a2e1a; border:1px solid #1e6b3a; border-radius:8px; padding:.6rem 1rem; color:#4ade80; font-size:.82rem; margin:.5rem 0; }
.notif-err { background:#2e0a0a; border:1px solid #6b1e1e; border-radius:8px; padding:.6rem 1rem; color:#f87171; font-size:.82rem; margin:.5rem 0; }
.notif-info{ background:#0d1a2e; border:1px solid #1e3f6b; border-radius:8px; padding:.6rem 1rem; color:#60a5fa; font-size:.82rem; margin:.5rem 0; }

/* Section title */
.section-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #f5f0e8;
    letter-spacing: .06em;
    text-transform: uppercase;
    border-bottom: 1px solid #252a38;
    padding-bottom: .4rem;
    margin: 1.2rem 0 .8rem;
}

/* Streamlit widget overrides */
.stSelectbox label, .stNumberInput label, .stTextInput label {
    font-size: .72rem !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    color: #7a7f94 !important;
}
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #181c25 !important;
    border: 1px solid #252a38 !important;
    color: #e8e4dc !important;
    border-radius: 6px !important;
}
.stButton > button {
    background: #e55c00 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: .82rem !important;
    font-weight: 500 !important;
    padding: .5rem 1.2rem !important;
    transition: opacity .2s !important;
    width: 100%;
}
.stButton > button:hover { opacity: .85 !important; }
div[data-testid="stDataFrame"] {
    background: #181c25 !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────

if "flotta" not in st.session_state:
    st.session_state.flotta = GestoreFlotta()
if "notifica" not in st.session_state:
    st.session_state.notifica = None   # (tipo, messaggio)

flotta: GestoreFlotta = st.session_state.flotta


# ─────────────────────────────────────────────
#  HELPER NOTIFICHE
# ─────────────────────────────────────────────

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

with st.sidebar:
    st.markdown('<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:1.6rem;font-weight:700;color:#f5f0e8;letter-spacing:.05em;margin-bottom:.1rem;">🚛 FLEET</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.65rem;color:#e55c00;letter-spacing:.2em;text-transform:uppercase;margin-bottom:1.5rem;">Sistema di Gestione</div>', unsafe_allow_html=True)

    azione = st.selectbox("Azione", ["➕  Aggiungi veicolo", "📦  Carica / Scarica", "🗑️  Rimuovi veicolo"])

    st.markdown("---")

    # ── AGGIUNGI ─────────────────────────────
    if azione == "➕  Aggiungi veicolo":
        st.markdown('<div class="section-title">Nuovo veicolo</div>', unsafe_allow_html=True)
        tipo = st.selectbox("Tipo", ["Camion 🚛", "Furgone 🚐", "Motocarro 🛺"])
        targa = st.text_input("Targa", placeholder="AB123CD").upper().strip()
        peso_max = st.number_input("Peso massimo (kg)", min_value=1, value=5000, step=100)
        carico_att = st.number_input("Carico attuale (kg)", min_value=0, value=0, step=50)

        if tipo == "Camion 🚛":
            numero_assi = st.number_input("Numero di assi", min_value=2, max_value=10, value=4)
        elif tipo == "Furgone 🚐":
            alimentazione = st.selectbox("Alimentazione", ["elettrico", "diesel"])
        else:
            anni_servizio = st.number_input("Anni di servizio", min_value=0, value=3)

        if st.button("Aggiungi alla flotta"):
            if not targa:
                set_notif("err", "⚠️ Inserisci una targa valida.")
            elif flotta.targa_esistente(targa):
                set_notif("err", f"⚠️ La targa **{targa}** è già presente in flotta.")
            elif carico_att > peso_max:
                set_notif("err", "⚠️ Il carico attuale non può superare il peso massimo.")
            else:
                if tipo == "Camion 🚛":
                    veicolo = Camion(targa, peso_max, carico_att, numero_assi)
                elif tipo == "Furgone 🚐":
                    veicolo = Furgone(targa, peso_max, carico_att, alimentazione)
                else:
                    veicolo = Motocarro(targa, peso_max, carico_att, anni_servizio)
                flotta.aggiungi_veicolo(veicolo)
                set_notif("ok", f"✅ {veicolo.tipo()} **{targa}** aggiunto alla flotta.")
                st.rerun()

    # ── CARICA / SCARICA ──────────────────────
    elif azione == "📦  Carica / Scarica":
        st.markdown('<div class="section-title">Gestione carico</div>', unsafe_allow_html=True)
        veicoli = flotta.get_veicoli()
        if not veicoli:
            st.markdown('<div class="notif-info">Nessun veicolo in flotta.</div>', unsafe_allow_html=True)
        else:
            targhe = [v.get_targa() for v in veicoli]
            targa_sel = st.selectbox("Seleziona veicolo", targhe)
            operazione = st.selectbox("Operazione", ["Carica", "Scarica"])
            kg = st.number_input("Quantità (kg)", min_value=1, value=100, step=10)

            if st.button(f"{operazione} veicolo"):
                v = flotta.trova(targa_sel)
                if v:
                    ok, msg = v.carica(kg) if operazione == "Carica" else v.scarica(kg)
                    set_notif("ok" if ok else "err", msg)
                    st.rerun()

    # ── RIMUOVI ───────────────────────────────
    else:
        st.markdown('<div class="section-title">Rimuovi veicolo</div>', unsafe_allow_html=True)
        veicoli = flotta.get_veicoli()
        if not veicoli:
            st.markdown('<div class="notif-info">Nessun veicolo in flotta.</div>', unsafe_allow_html=True)
        else:
            targhe = [v.get_targa() for v in veicoli]
            targa_rm = st.selectbox("Seleziona targa", targhe)
            if st.button("🗑️ Rimuovi dalla flotta"):
                flotta.rimuovi_veicolo(targa_rm)
                set_notif("info", f"🗑️ Veicolo **{targa_rm}** rimosso dalla flotta.")
                st.rerun()


# ─────────────────────────────────────────────
#  MAIN — DASHBOARD
# ─────────────────────────────────────────────

st.markdown('<div class="hero-title">GESTIONE FLOTTA</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Sistema di trasporto merci</div>', unsafe_allow_html=True)

show_notif()

veicoli = flotta.get_veicoli()
n_veicoli   = len(veicoli)
costo_tot   = flotta.costo_totale()
carico_tot  = sum(v.get_carico_attuale() for v in veicoli)
cap_tot     = sum(v.get_peso_massimo() for v in veicoli)
perc_carico = round(carico_tot / cap_tot * 100, 1) if cap_tot > 0 else 0

# ── METRICHE ───────────────────────────────

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Veicoli in flotta</div>
        <div class="metric-value">{n_veicoli}</div>
        <div class="metric-icon">🚛</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Costo manutenzione</div>
        <div class="metric-value">€{costo_tot:,.0f}</div>
        <div class="metric-icon">🔧</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Carico totale</div>
        <div class="metric-value">{carico_tot:,} kg</div>
        <div class="metric-icon">📦</div>
    </div>""", unsafe_allow_html=True)

with c4:
    color = "#e55c00" if perc_carico > 80 else "#4ade80"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Saturazione flotta</div>
        <div class="metric-value" style="color:{color}">{perc_carico}%</div>
        <div class="metric-icon">📊</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── LAYOUT: veicoli + grafico ───────────────

col_left, col_right = st.columns([1, 1], gap="large")

# ── VEICOLI ────────────────────────────────
with col_left:
    st.markdown('<div class="section-title">Veicoli in flotta</div>', unsafe_allow_html=True)
    if not veicoli:
        st.markdown('<div class="notif-info">Nessun veicolo ancora aggiunto. Usa la sidebar per iniziare.</div>', unsafe_allow_html=True)
    else:
        for v in veicoli:
            perc = v.get_carico_attuale() / v.get_peso_massimo() * 100 if v.get_peso_massimo() > 0 else 0
            bar_color = "#e55c00" if perc > 80 else "#f5a623" if perc > 50 else "#4ade80"
            st.markdown(f"""
            <div class="veicolo-card">
                <div class="veicolo-icon">{v.ICON}</div>
                <div class="veicolo-info">
                    <div class="veicolo-targa">{v.get_targa()}</div>
                    <div class="veicolo-detail">{v.extra()} &nbsp;·&nbsp; max {v.get_peso_massimo():,} kg &nbsp;·&nbsp; costo €{v.costo_manutenzione():,}</div>
                    <div class="progress-wrap">
                        <div class="progress-fill" style="width:{perc:.1f}%; background:{bar_color};"></div>
                    </div>
                    <div class="veicolo-detail" style="margin-top:.25rem;">{v.get_carico_attuale():,} / {v.get_peso_massimo():,} kg &nbsp;<span style="color:{bar_color}">({perc:.1f}%)</span></div>
                </div>
                <span class="badge">{v.tipo()}</span>
            </div>
            """, unsafe_allow_html=True)

# ── GRAFICO ────────────────────────────────
with col_right:
    st.markdown('<div class="section-title">Costi di manutenzione</div>', unsafe_allow_html=True)
    if not veicoli:
        st.markdown('<div class="notif-info">Nessun dato da visualizzare.</div>', unsafe_allow_html=True)
    else:
        labels = [v.get_targa() for v in veicoli]
        costs  = [v.costo_manutenzione() for v in veicoli]
        icons_map = {"Camion": "#e55c00", "Furgone": "#f5a623", "Motocarro": "#60a5fa"}
        colors = [icons_map.get(v.tipo(), "#e55c00") for v in veicoli]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=labels,
            y=costs,
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"€{c:,}" for c in costs],
            textposition="outside",
            textfont=dict(family="DM Mono", size=11, color="#e8e4dc"),
            hovertemplate="<b>%{x}</b><br>Costo: €%{y:,}<extra></extra>",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#181c25",
            font=dict(family="DM Mono", color="#7a7f94"),
            xaxis=dict(
                tickfont=dict(family="Barlow Condensed", size=13, color="#e8e4dc"),
                gridcolor="#252a38", showgrid=False,
                linecolor="#252a38",
            ),
            yaxis=dict(
                tickprefix="€", tickfont=dict(size=11),
                gridcolor="#252a38", linecolor="#252a38",
            ),
            margin=dict(l=10, r=10, t=30, b=10),
            height=320,
            showlegend=False,
            bargap=0.35,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Legenda colori
    if veicoli:
        st.markdown("""
        <div style="display:flex;gap:1.2rem;margin-top:.5rem;">
            <span style="font-size:.7rem;color:#7a7f94;">
                <span style="color:#e55c00;">■</span> Camion &nbsp;
                <span style="color:#f5a623;">■</span> Furgone &nbsp;
                <span style="color:#60a5fa;">■</span> Motocarro
            </span>
        </div>
        """, unsafe_allow_html=True)

# ── TABELLA INTERATTIVA ─────────────────────
st.markdown('<div class="section-title">Tabella veicoli</div>', unsafe_allow_html=True)
if not veicoli:
    st.markdown('<div class="notif-info">Nessun dato disponibile.</div>', unsafe_allow_html=True)
else:
    rows = []
    for v in veicoli:
        perc = round(v.get_carico_attuale() / v.get_peso_massimo() * 100, 1) if v.get_peso_massimo() > 0 else 0
        rows.append({
            "Tipo":              v.tipo(),
            "Targa":             v.get_targa(),
            "Peso max (kg)":     v.get_peso_massimo(),
            "Carico (kg)":       v.get_carico_attuale(),
            "Saturazione (%)":   perc,
            "Costo maint. (€)":  v.costo_manutenzione(),
            "Dettaglio":         v.extra(),
        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df.style
          .format({"Saturazione (%)": "{:.1f}%", "Costo maint. (€)": "€{:,.0f}", "Peso max (kg)": "{:,}", "Carico (kg)": "{:,}"})
          .background_gradient(subset=["Saturazione (%)"], cmap="RdYlGn_r", vmin=0, vmax=100)
          .background_gradient(subset=["Costo maint. (€)"], cmap="Oranges", vmin=0),
        use_container_width=True,
        hide_index=True,
    )
