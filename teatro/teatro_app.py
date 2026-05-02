import streamlit as st

# ─────────────────────────────────────────────
#  MODELLO (invariato rispetto all'originale)
# ─────────────────────────────────────────────

class Posto:
    def __init__(self, numero: int, fila: str, occupato=False):
        self._numero = numero
        self._fila = fila
        self._occupato = occupato

    def prenota(self):
        if self._occupato:
            return False, f"Il posto {self._numero} {self._fila} è già occupato."
        self._occupato = True
        return True, f"Posto {self._numero} fila {self._fila} prenotato con successo."

    def libera(self):
        if not self._occupato:
            return False, f"Il posto {self._numero} {self._fila} è già libero."
        self._occupato = False
        return True, f"Posto {self._numero} fila {self._fila} liberato."

    def get_numero(self):   return self._numero
    def get_fila(self):     return self._fila
    def get_occupato(self): return self._occupato
    def set_numero(self, v): self._numero = v
    def set_fila(self, v):   self._fila = v


class PostoVIP(Posto):
    def __init__(self, numero, fila, occupato=False, servizi_extra=None):
        super().__init__(numero, fila, occupato)
        self.servizi_extra = servizi_extra if servizi_extra is not None else []

    def prenota(self, servizi_selezionati=None):
        ok, msg = super().prenota()
        if ok and servizi_selezionati:
            self.servizi_extra = servizi_selezionati
        return ok, msg

    def get_servizi_extra(self): return self.servizi_extra
    def tipo(self): return "VIP"


class PostoStandard(Posto):
    def __init__(self, numero, fila, costo, occupato=False):
        super().__init__(numero, fila, occupato)
        self.costo = costo

    def prenota(self):
        ok, msg = super().prenota()
        if ok:
            msg += f" Costo: €{self.costo:.2f}"
        return ok, msg

    def get_costo(self): return self.costo
    def set_costo(self, v): self.costo = v
    def tipo(self): return "Standard"


class Teatro:
    def __init__(self):
        self._posti = []

    def aggiungi_posto(self, posto: Posto):
        self._posti.append(posto)

    def trova_posto(self, numero, fila):
        for p in self._posti:
            if p.get_numero() == numero and p.get_fila().upper() == fila.upper():
                return p
        return None

    def esiste_posto(self, numero, fila):
        return self.trova_posto(numero, fila) is not None

    def libera_posto(self, numero, fila):
        p = self.trova_posto(numero, fila)
        if p:
            return p.libera()
        return False, f"Il posto {numero} fila {fila} non esiste."

    def get_posti(self): return self._posti

    def statistiche(self):
        tot = len(self._posti)
        occupati = sum(1 for p in self._posti if p.get_occupato())
        incasso = sum(
            p.get_costo() for p in self._posti
            if isinstance(p, PostoStandard) and p.get_occupato()
        )
        vip_count = sum(1 for p in self._posti if isinstance(p, PostoVIP))
        std_count = sum(1 for p in self._posti if isinstance(p, PostoStandard))
        return {
            "totale": tot,
            "occupati": occupati,
            "liberi": tot - occupati,
            "incasso": incasso,
            "vip": vip_count,
            "standard": std_count,
        }


# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Teatro — Prenotazioni",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS — TEMA TEATRALE ART DÉCO
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap');

/* ── ROOT VARS ── */
:root {
    --bg:        #080408;
    --surface:   #12080c;
    --surface2:  #1c0e13;
    --border:    #3a1c22;
    --border2:   #5a2c34;
    --crimson:   #b91c3a;
    --crimson2:  #e02548;
    --gold:      #c9963a;
    --gold2:     #e8b84b;
    --cream:     #f0e6d4;
    --muted:     #7a6058;
    --vip-bg:    #1e0e16;
    --vip-glow:  #c9963a44;
}

/* ── BASE ── */
[data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--cream);
    font-family: 'Cormorant Garamond', Georgia, serif;
}
[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--cream) !important; }

/* ── DECORATIVE BORDER TOP ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    display: block;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--gold), var(--crimson), var(--gold), transparent);
}

/* ── HERO ── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    position: relative;
}
.hero-ornament {
    color: var(--gold);
    font-size: 1.1rem;
    letter-spacing: .6em;
    margin-bottom: .5rem;
    opacity: .7;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 4rem;
    font-weight: 900;
    font-style: italic;
    color: var(--cream);
    line-height: 1;
    letter-spacing: .02em;
    text-shadow: 0 0 60px #b91c3a44;
}
.hero-sub {
    font-family: 'Cormorant Garamond', serif;
    font-size: .85rem;
    letter-spacing: .35em;
    text-transform: uppercase;
    color: var(--gold);
    margin-top: .5rem;
    font-weight: 300;
}
.hero-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: .8rem;
    margin: 1.2rem auto;
    max-width: 400px;
}
.hero-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold));
}
.hero-line.right {
    background: linear-gradient(90deg, var(--gold), transparent);
}
.hero-diamond { color: var(--gold); font-size: .7rem; }

/* ── STAT CARDS ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: .8rem;
    margin-bottom: 2rem;
}
.stat-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-top: 2px solid var(--gold);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.stat-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 20%; right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold)44, transparent);
}
.stat-label {
    font-size: .7rem;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .4rem;
    font-family: 'Cormorant Garamond', serif;
}
.stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--cream);
}
.stat-value.gold  { color: var(--gold2); }
.stat-value.red   { color: var(--crimson2); }
.stat-value.green { color: #6bcf8a; }

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-style: italic;
    color: var(--cream);
    letter-spacing: .04em;
    border-bottom: 1px solid var(--border);
    padding-bottom: .5rem;
    margin: 1.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: .6rem;
}
.section-title::before {
    content: '◆';
    color: var(--gold);
    font-size: .55rem;
    font-style: normal;
}

/* ── SEAT MAP ── */
.sala-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.palco {
    background: linear-gradient(135deg, var(--crimson) 0%, #7a0e20 100%);
    border-radius: 60px 60px 0 0;
    text-align: center;
    padding: .6rem 2rem;
    margin: 0 auto 2rem;
    max-width: 60%;
    font-family: 'Playfair Display', serif;
    font-size: .85rem;
    letter-spacing: .25em;
    text-transform: uppercase;
    color: var(--cream);
    box-shadow: 0 4px 30px #b91c3a55;
}
.fila-row {
    display: flex;
    align-items: center;
    gap: .4rem;
    margin-bottom: .45rem;
    justify-content: center;
}
.fila-label {
    font-family: 'Playfair Display', serif;
    font-size: .75rem;
    color: var(--gold);
    letter-spacing: .1em;
    width: 1.5rem;
    text-align: center;
    font-weight: 700;
}
.posto {
    width: 36px;
    height: 32px;
    border-radius: 5px 5px 2px 2px;
    border: 1px solid;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: .6rem;
    font-family: 'Cormorant Garamond', serif;
    font-weight: 600;
    cursor: default;
    transition: transform .15s;
    position: relative;
}
.posto:hover { transform: translateY(-2px); }
.posto.libero-std {
    background: #1e2818;
    border-color: #3a5028;
    color: #6bcf8a;
}
.posto.occupato-std {
    background: #2a0e14;
    border-color: var(--crimson);
    color: var(--crimson2);
}
.posto.libero-vip {
    background: var(--vip-bg);
    border-color: var(--gold);
    color: var(--gold2);
    box-shadow: 0 0 8px var(--vip-glow);
}
.posto.occupato-vip {
    background: #2a1a08;
    border-color: var(--gold2);
    color: var(--gold2);
    box-shadow: 0 0 12px var(--vip-glow);
    opacity: .6;
}
.seat-legend {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    margin-top: 1rem;
    flex-wrap: wrap;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: .4rem;
    font-size: .72rem;
    color: var(--muted);
    letter-spacing: .05em;
    font-family: 'Cormorant Garamond', serif;
}
.legend-dot {
    width: 12px; height: 12px;
    border-radius: 2px;
    border: 1px solid;
}

/* ── NOTIFICHE ── */
.notif-ok  { background:#0a1e10; border:1px solid #1e5a30; border-left: 3px solid #6bcf8a; border-radius:4px; padding:.7rem 1rem; color:#6bcf8a; font-size:.85rem; margin:.5rem 0; font-family:'Cormorant Garamond',serif; letter-spacing:.02em; }
.notif-err { background:#1e0a0e; border:1px solid #5a1e28; border-left: 3px solid var(--crimson2); border-radius:4px; padding:.7rem 1rem; color:var(--crimson2); font-size:.85rem; margin:.5rem 0; font-family:'Cormorant Garamond',serif; letter-spacing:.02em; }
.notif-info{ background:#1a140a; border:1px solid #5a420e; border-left: 3px solid var(--gold); border-radius:4px; padding:.7rem 1rem; color:var(--gold2); font-size:.85rem; margin:.5rem 0; font-family:'Cormorant Garamond',serif; letter-spacing:.02em; }

/* ── SIDEBAR OVERRIDES ── */
.sidebar-brand {
    text-align: center;
    padding: .5rem 0 1.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}
.sidebar-brand-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-style: italic;
    font-weight: 700;
    color: var(--cream) !important;
}
.sidebar-brand-sub {
    font-size: .65rem;
    letter-spacing: .22em;
    text-transform: uppercase;
    color: var(--gold) !important;
    font-family: 'Cormorant Garamond', serif;
}
.stSelectbox label, .stNumberInput label,
.stTextInput label, .stMultiSelect label {
    font-size: .72rem !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    font-family: 'Cormorant Garamond', serif !important;
}
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #1c0e13 !important;
    border: 1px solid var(--border2) !important;
    color: var(--cream) !important;
    border-radius: 3px !important;
    font-family: 'Cormorant Garamond', serif !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--crimson), #8a1228) !important;
    color: var(--cream) !important;
    border: 1px solid var(--crimson2) !important;
    border-radius: 3px !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: .9rem !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    padding: .5rem 1.2rem !important;
    width: 100%;
    transition: all .2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--crimson2), var(--crimson)) !important;
    box-shadow: 0 0 16px #b91c3a55 !important;
}
div[data-testid="stDataFrame"] {
    background: var(--surface2) !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────

if "teatro" not in st.session_state:
    st.session_state.teatro = Teatro()
if "notifica" not in st.session_state:
    st.session_state.notifica = None

teatro: Teatro = st.session_state.teatro

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

SERVIZI_OPZIONI = ["Accesso al Lounge", "Servizio in posto"]

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">🎭 Teatro</div>
        <div class="sidebar-brand-sub">Sistema di Prenotazione</div>
    </div>
    """, unsafe_allow_html=True)

    azione = st.selectbox("Azione", ["🎟️  Prenota posto", "🔓  Libera posto"])
    st.markdown("---")

    # ── PRENOTA ──────────────────────────────────
    if azione == "🎟️  Prenota posto":
        st.markdown('<div style="font-family:\'Playfair Display\',serif;font-style:italic;font-size:1rem;color:#f0e6d4;margin-bottom:.8rem;">Nuova Prenotazione</div>', unsafe_allow_html=True)

        tipo = st.selectbox("Tipo posto", ["Standard", "VIP ✦"])
        fila = st.text_input("Fila", placeholder="Es. A, B, C...").upper().strip()
        numero = st.number_input("Numero posto", min_value=1, max_value=99, value=1, step=1)

        if tipo == "Standard":
            costo = st.number_input("Costo (€)", min_value=0.0, value=25.0, step=5.0, format="%.2f")
        else:
            servizi_sel = st.multiselect(
                "Servizi extra (opzionale)",
                SERVIZI_OPZIONI,
                help="Seleziona uno o più servizi VIP"
            )

        if st.button("Conferma Prenotazione"):
            if not fila:
                set_notif("err", "⚠ Inserisci una fila valida.")
            else:
                posto_esistente = teatro.trova_posto(numero, fila)
                if posto_esistente:
                    ok, msg = posto_esistente.prenota()
                    set_notif("ok" if ok else "err", msg)
                else:
                    if tipo == "Standard":
                        nuovo = PostoStandard(numero, fila, costo)
                    else:
                        nuovo = PostoVIP(numero, fila)
                    teatro.aggiungi_posto(nuovo)
                    if tipo == "Standard":
                        ok, msg = nuovo.prenota()
                    else:
                        ok, msg = nuovo.prenota(servizi_selezionati=[s.lower() for s in servizi_sel])
                    set_notif("ok" if ok else "err", msg)
                st.rerun()

    # ── LIBERA ───────────────────────────────────
    else:
        st.markdown('<div style="font-family:\'Playfair Display\',serif;font-style:italic;font-size:1rem;color:#f0e6d4;margin-bottom:.8rem;">Libera un Posto</div>', unsafe_allow_html=True)

        posti = teatro.get_posti()
        occupati = [p for p in posti if p.get_occupato()]
        if not occupati:
            st.markdown('<div class="notif-info">Nessun posto attualmente occupato.</div>', unsafe_allow_html=True)
        else:
            opzioni = [f"{p.get_fila()}{p.get_numero()} — {p.tipo()}" for p in occupati]
            sel = st.selectbox("Seleziona posto", opzioni)
            idx = opzioni.index(sel)
            posto_sel = occupati[idx]

            if st.button("Libera Posto"):
                ok, msg = posto_sel.libera()
                set_notif("ok" if ok else "err", msg)
                st.rerun()

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

# ── HERO ─────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-ornament">✦ &nbsp;&nbsp; Benvenuti &nbsp;&nbsp; ✦</div>
    <div class="hero-title">Teatro Reale</div>
    <div class="hero-sub">Sistema di Gestione Prenotazioni</div>
    <div class="hero-divider">
        <div class="hero-line"></div>
        <div class="hero-diamond">◆</div>
        <div class="hero-line right"></div>
    </div>
</div>
""", unsafe_allow_html=True)

show_notif()

# ── STATISTICHE ──────────────────────────────
stats = teatro.statistiche()

st.markdown(f"""
<div class="stat-grid">
    <div class="stat-card">
        <div class="stat-label">Posti Totali</div>
        <div class="stat-value">{stats['totale']}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Occupati</div>
        <div class="stat-value red">{stats['occupati']}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Disponibili</div>
        <div class="stat-value green">{stats['liberi']}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Incasso stimato</div>
        <div class="stat-value gold">€{stats['incasso']:,.0f}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── LAYOUT PRINCIPALE ─────────────────────────
col_map, col_list = st.columns([3, 2], gap="large")

# ── MAPPA SALA ────────────────────────────────
with col_map:
    st.markdown('<div class="section-title">Mappa della Sala</div>', unsafe_allow_html=True)
    posti = teatro.get_posti()

    if not posti:
        st.markdown('<div class="notif-info">✦ &nbsp; Nessun posto ancora aggiunto. Usa la sidebar per iniziare le prenotazioni.</div>', unsafe_allow_html=True)
    else:
        # Organizza per fila
        from collections import defaultdict
        sale_map = defaultdict(list)
        for p in posti:
            sale_map[p.get_fila().upper()].append(p)

        # Ordina file alfabeticamente, posti per numero
        sale_map = {k: sorted(v, key=lambda x: x.get_numero()) for k, v in sorted(sale_map.items())}

        html_sala = '<div class="sala-wrap">'
        html_sala += '<div class="palco">◆ &nbsp; P A L C O &nbsp; ◆</div>'

        for fila, ps in sale_map.items():
            html_sala += f'<div class="fila-row"><span class="fila-label">{fila}</span>'
            for p in ps:
                is_vip = isinstance(p, PostoVIP)
                if p.get_occupato():
                    css = "occupato-vip" if is_vip else "occupato-std"
                    label = "✦" if is_vip else "✕"
                else:
                    css = "libero-vip" if is_vip else "libero-std"
                    label = "✦" if is_vip else str(p.get_numero())

                # Tooltip
                if is_vip and p.get_occupato() and p.get_servizi_extra():
                    servizi_str = ", ".join(p.get_servizi_extra())
                    title = f"VIP {p.get_numero()} — {servizi_str}"
                elif is_vip:
                    title = f"VIP — Posto {p.get_numero()}"
                else:
                    title = f"Std — Posto {p.get_numero()} — €{p.get_costo():.0f}"

                html_sala += f'<div class="posto {css}" title="{title}">{label}</div>'
            html_sala += '</div>'

        html_sala += """
        <div class="seat-legend">
            <div class="legend-item"><div class="legend-dot" style="background:#1e2818;border-color:#3a5028;"></div> Standard libero</div>
            <div class="legend-item"><div class="legend-dot" style="background:#2a0e14;border-color:#e02548;"></div> Standard occupato</div>
            <div class="legend-item"><div class="legend-dot" style="background:#1e0e16;border-color:#c9963a;box-shadow:0 0 6px #c9963a44;"></div> VIP libero</div>
            <div class="legend-item"><div class="legend-dot" style="background:#2a1a08;border-color:#e8b84b;opacity:.6;"></div> VIP occupato</div>
        </div>
        """
        html_sala += '</div>'
        st.markdown(html_sala, unsafe_allow_html=True)

# ── LISTA POSTI ───────────────────────────────
with col_list:
    st.markdown('<div class="section-title">Dettaglio Posti</div>', unsafe_allow_html=True)

    if not posti:
        st.markdown('<div class="notif-info">Nessun dato disponibile.</div>', unsafe_allow_html=True)
    else:
        import pandas as pd

        rows = []
        for p in sorted(posti, key=lambda x: (x.get_fila(), x.get_numero())):
            stato = "Occupato" if p.get_occupato() else "Libero"
            tipo = p.tipo()
            extra = ""
            costo_display = ""
            if isinstance(p, PostoVIP) and p.get_servizi_extra():
                extra = ", ".join(p.get_servizi_extra())
            if isinstance(p, PostoStandard):
                costo_display = f"€{p.get_costo():.2f}"
            rows.append({
                "Fila": p.get_fila(),
                "N°": p.get_numero(),
                "Tipo": tipo,
                "Stato": stato,
                "Costo": costo_display,
                "Servizi VIP": extra,
            })

        df = pd.DataFrame(rows)

        def style_row(row):
            if row["Stato"] == "Occupato" and row["Tipo"] == "VIP":
                return ["background-color: #1e1408; color: #e8b84b"] * len(row)
            elif row["Stato"] == "Occupato":
                return ["background-color: #1e0a0e; color: #e02548"] * len(row)
            elif row["Tipo"] == "VIP":
                return ["background-color: #1e0e16; color: #c9963a"] * len(row)
            return [""] * len(row)

        st.dataframe(
            df.style.apply(style_row, axis=1),
            use_container_width=True,
            hide_index=True,
            height=380,
        )
