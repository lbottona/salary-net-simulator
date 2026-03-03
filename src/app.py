import inspect

import streamlit as st
from tax_calculator import calcola_netto

HAS_MENSILITA_PARAM = "mensilita" in inspect.signature(calcola_netto).parameters

st.set_page_config(page_title="Calcolatore Netto da RAL", page_icon="💰", layout="wide")


def format_currency(value: float) -> str:
    return f"{value:,.0f}".replace(",", ".")


def format_percent(value: float) -> str:
    safe_value = value or 0
    return f"{safe_value * 100:.1f}%"


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
            html, body, [data-testid="stAppViewContainer"], .stApp {
                background: linear-gradient(135deg, #e6ecda 0%, #fdfdf8 60%) !important;
                color: #10130e !important;
                font-family: 'Space Grotesk', sans-serif !important;
            }
            .main .block-container {
                padding: 2.4rem 3.5rem 3.5rem;
                color: #0c0f0b !important;
            }
            .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label {
                color: #0c0f0b !important;
            }
            .page-eyebrow {
                text-transform: uppercase;
                letter-spacing: 0.25em;
                font-size: 12px;
                color: #4a4f38;
                margin-bottom: 6px;
            }
            .page-title {
                font-size: 46px;
                font-weight: 600;
                margin: 0 0 18px;
                color: #050805;
            }
            .jet-card {
                background: #ffffff;
                border-radius: 36px;
                border: 1px solid #c3caa6;
                padding: 32px 34px 24px;
                box-shadow: 0 30px 60px rgba(8, 12, 6, 0.08);
            }
            .jet-divider {
                border: none;
                border-bottom: 1px solid #c5caa9;
                margin: 20px 0;
            }
            .input-label {
                font-weight: 600;
                margin-bottom: 6px;
                color: #20231f;
            }
            .stNumberInput input, .stTextInput input {
                border-radius: 16px !important;
                border: 1px solid #a3ad86 !important;
                background: #ffffff !important;
                color: #050805 !important;
                font-size: 18px !important;
                height: 50px;
            }
            .stSelectbox div[data-baseweb="select"] > div {
                border-radius: 16px !important;
                border: 1px solid #a3ad86 !important;
                background: #ffffff !important;
                color: #050805 !important;
            }
            .stRadio label {
                font-weight: 600;
                color: #151a12 !important;
            }
            button[kind="primary"], .stButton > button {
                background: linear-gradient(120deg, #11150d, #1f2914) !important;
                color: #ffffff !important;
                border-radius: 18px !important;
                font-weight: 700 !important;
                height: 54px;
                border: 0 !important;
                box-shadow: 0 12px 25px rgba(4, 6, 3, 0.25);
                letter-spacing: 0.03em;
            }
            .stButton > button *, button[kind="primary"] * {
                color: #ffffff !important;
            }
            .chip {
                border: 1px solid #9eb178;
                background: #eaf3cd;
                border-radius: 999px;
                padding: 4px 12px;
                font-size: 12px;
                color: #233015;
            }
            .result-box {
                border: 2px solid #b0c08a;
                border-radius: 24px;
                padding: 22px 26px;
                background: #ffffff;
            }
            .result-box h3 {
                margin: 0;
                font-size: 28px;
                font-weight: 600;
                color: #0c120a;
            }
            .result-value {
                font-size: 64px;
                font-weight: 600;
                margin: 8px 0 0;
                color: #020402;
            }
            .result-subtext {
                margin: 6px 0 0;
                color: #2d311f;
            }
            .result-section {
                margin-top: 32px;
            }
            .subtle-link {
                color: #0b3c7a;
                text-decoration: underline;
                font-weight: 500;
            }
            .cta-card {
                border: 1px solid #a8b588;
                border-radius: 28px;
                padding: 20px 24px;
                background: #ffffff;
                margin-top: 26px;
                display: flex;
                align-items: center;
                gap: 18px;
            }
            .cta-card button {
                border-radius: 999px !important;
                border: 1px solid #10130e !important;
                color: #10130e !important;
                background: transparent !important;
                font-weight: 600;
            }
            .stToggle {
                display: inline-flex !important;
                align-items: center;
                gap: 12px;
                padding: 6px 14px;
                border: 1px solid #b7c28f;
                border-radius: 999px;
                background: #f8fbe9;
            }
            .stToggle > label {
                font-weight: 600;
                color: #151a12;
                margin: 0;
            }
            .stToggle div[data-baseweb="toggle"] {
                width: 48px !important;
                height: 24px !important;
                border-radius: 999px !important;
                border: 2px solid #4f5c2b !important;
                background: #dfe7bf !important;
                box-shadow: inset 0 0 0 1px rgba(0,0,0,0.08);
            }
            .stToggle div[data-baseweb="toggle"] > div {
                background: #ffffff !important;
                width: 20px !important;
                height: 20px !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.25);
            }
            .stToggle input:checked + div div[data-baseweb="toggle"] {
                background: #11150d !important;
                border-color: #11150d !important;
                box-shadow: none;
            }
            .detail-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 14px;
                margin-top: 24px;
            }
            .detail-card {
                border: 1px solid #cdd8a9;
                border-radius: 20px;
                padding: 14px 16px;
                background: #f9fbf1;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5);
            }
            .detail-label {
                font-size: 12px;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #748059;
                margin: 0;
            }
            .detail-value {
                margin: 6px 0 0;
                font-size: 20px;
                font-weight: 600;
                color: #040704;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_styles()

st.markdown('<p class="page-eyebrow">simulatore Leo hr</p>', unsafe_allow_html=True)
st.markdown('<h1 class="page-title">Calcola lo stipendio netto</h1>', unsafe_allow_html=True)


col_inputs, col_results = st.columns([1.05, 0.95], gap="large")

with col_inputs:
    st.markdown("#### Stipendio (RAL)")
    ral = st.number_input(
        "Inserisci RAL (in €)",
        min_value=0.0,
        step=500.0,
        format="%.0f",
        key="ral",
    )
    contract_type = st.selectbox(
        "Contratto",
        ["Tempo indeterminato"],
        index=0,
    )
    mensilita = st.selectbox("Mensilità", options=[12, 13, 14], index=1)

   


    st.button("Calcola", use_container_width=True)

if ral > 0:
    if HAS_MENSILITA_PARAM:
        result = calcola_netto(ral, mensilita)
    else:
        result = calcola_netto(ral)
        st.warning("Aggiorna tax_calculator.py per supportare il numero di mensilita personalizzato.", icon="⚠️")
else:
    result = {
        "ral": 0,
        "imponibile": 0,
        "netto_annuale": 0,
        "netto_mensile": 0,
        "totale_tasse": 0,
        "irpef": 0,
        "inps": 0,
        "add_regionale": 0,
        "add_comunale": 0,
        "irpef_lorda": 0,
        "detrazione_lavoro_dipendente": 0,
        "aliquota_effettiva": 0,
        "aliquota_marginale": 0,
    }

with col_results:
    st.markdown("#### Risultato")
    view_mensile = st.toggle("Vedi mensile", value=True, key="view_mode")
    primary_value = result["netto_mensile"] if view_mensile else result["netto_annuale"]
    primary_label = "Stipendio netto" if view_mensile else "Stipendio netto annuale"
    secondary_label = "vedi mensile" if not view_mensile else "vedi annuale"

    st.markdown(
        f"""
        <div class="result-box">
            <div class="chip">{secondary_label}</div>
            <h3>{primary_label}</h3>
            <p class="result-value">{format_currency(primary_value)} €</p>
            <p class="result-subtext">Mensilità considerata: {mensilita}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown('<hr class="jet-divider">', unsafe_allow_html=True)
    net_share = (result["netto_annuale"] / result["ral"] * 100) if result["ral"] else 0
    st.markdown(
        f"""
        <p><strong>IRPEF</strong>: € {result['irpef']:,.2f}<br>
        <strong>INPS</strong>: € {result['inps']:,.2f}<br>
        <strong>Addizionali</strong>: € {(result['add_regionale'] + result['add_comunale']):,.2f}</p>
        <p style="color:#5a5e4c;">Tasse totali €{format_currency(result['totale_tasse'])} · Netto {net_share:.1f}% della RAL se inserita.</p>
        """,
        unsafe_allow_html=True,
    )

detail_values = [
    ("RAL lordo", f"€ {format_currency(result['ral'])}"),
    ("Imponibile fiscale", f"€ {format_currency(result['imponibile'])}"),
    ("Contributi INPS", f"€ {format_currency(result['inps'])}"),
    ("IRPEF lorda", f"€ {format_currency(result['irpef_lorda'])}"),
    ("Detrazione lavoro dip.", f"€ {format_currency(result['detrazione_lavoro_dipendente'])}"),
    ("IRPEF netta", f"€ {format_currency(result['irpef'])}"),
    ("Addizionale regionale", f"€ {format_currency(result['add_regionale'])}"),
    ("Addizionale comunale", f"€ {format_currency(result['add_comunale'])}"),
    ("Tasse totali", f"€ {format_currency(result['totale_tasse'])}"),
    ("Netto annuale", f"€ {format_currency(result['netto_annuale'])}"),
    ("Netto mensile", f"€ {format_currency(result['netto_mensile'])}"),
    ("Aliquota effettiva", format_percent(result['aliquota_effettiva'])),
    ("Aliquota marginale", format_percent(result['aliquota_marginale'])),
]

cards_html = "".join(
    f"<div class='detail-card'><p class='detail-label'>{label}</p><p class='detail-value'>{value}</p></div>"
    for label, value in detail_values
)

if result["ral"] > 0:
    st.markdown("<div style='margin-top:40px;'>", unsafe_allow_html=True)
    st.markdown("### Dettaglio completo", unsafe_allow_html=True)
    st.markdown(f"<div class='detail-grid'>{cards_html}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

   

st.markdown("</div>", unsafe_allow_html=True)