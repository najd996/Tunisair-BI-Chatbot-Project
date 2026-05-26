import streamlit as st
import pandas as pd
import time
import base64
import altair as alt

from streamlit_local_storage import LocalStorage
local_storage = LocalStorage()

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_image("plane.png")

# ─────────────────────────────────────────────────────────────────────────────
#  CONFIG & THEME
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tunisair ChatBot",
    page_icon="Tunisair_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

TUNISAIR_RED = "#E30613"
PURE_WHITE = "#FFFFFF"
NEUTRAL_LIGHT = "#F8F9FA"
TEXT_BLACK = "#000000"
BORDER_GREY = "#EEEEEE"

# ─────────────────────────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(f"""
<style>
            
    .stHtmlHeader a, 
    .st-emotion-cache-15zrgzn, 
    [data-testid="stHeaderActionElements"] {{
        display: none !important;
    }}

    /* Additional layer to catch the hover effect link */
    header a {{
        visibility: hidden !important;
    }}
            
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .stApp {{ background-color: {PURE_WHITE}; }}
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; color: {TEXT_BLACK}; }}

    .app-header {{
        background-color: {PURE_WHITE};
        border-bottom: 4px solid {TUNISAIR_RED};
        padding: 15px 0px;
        margin-bottom: 25px;
    }}

    [data-testid="stSidebar"] {{
        background-color: {NEUTRAL_LIGHT} !important;
        border-right: 1px solid {BORDER_GREY};
    }}

    .msg-user .bubble {{
        background: {TUNISAIR_RED};
        color: white;
        border-radius: 12px 12px 0px 12px;
        padding: 10px;
        margin-bottom: 5px;
    }}
    .msg-bot .bubble {{
        background: #F1F3F5;
        border: 1px solid #E9ECEF;
        color: {TEXT_BLACK};
        border-radius: 12px 12px 12px 0px;
        padding: 10px;
        margin-bottom: 5px;
    }}

    .section-title {{
        color: {TUNISAIR_RED};
        font-weight: 800;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 2px;
        margin: 20px 0 10px 0;
    }}

    .stButton button {{
        background-color: {TUNISAIR_RED} !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        width: 100%;
    }}
    .stButton button:hover {{ background-color: #B2050F !important; }}

    [data-testid="stTable"] {{ background-color: white; }}
    
    
    footer {{visibility: hidden;}}
    [data-testid="InputInstructions"] {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  FAKE API (lpartie ili bch tbadalha bel API mteena)
# ─────────────────────────────────────────────────────────────────────────────
def fake_api(question: str) -> dict:
    q = question.lower()
    
    if "prix" in q:
        return {
            "intent": "EVOLUTION_DES_PRIX",
            "reponse": "L'analyse montre une stabilité relative des prix entre 2021 et 2023, avec une légère baisse en 2022 avant une remontée. Cela impacte directement la marge brute sur les vols long-courriers.",
            "resultat": {
                "prix": [["2023", 2.74694491757679], ["2022", 2.743470128561861], ["2021", 2.7533909880658762]]
            },
            "chart_type": "line"
        }
    
    elif "taxe" in q:
        return {
            "intent": "EVOLUTION_DES_TAXES",
            "reponse": "Les taxes ont connu une fluctuation significative, atteignant un pic en 2021. La gestion fiscale actuelle a permis de réduire ce coût de 12% en 2022.",
            "resultat": {
                "taxes": [["2023", 1.4317488950718193], ["2022", 1.2732039131173662], ["2021", 1.5502226768644607]]
            },
            "chart_type": "line"
        }
        
    elif "fournisseur" in q:
        return {
            "intent": "DEPENSES_PAR_FOURNISSEUR",
            "reponse": "Air Total International reste le partenaire majeur. Une diversification vers PETROL OFISI pourrait être envisagée pour optimiser les coûts de ravitaillement en zone Est.",
            "resultat": {
                "dépenses": [["2019", "PETROL OFISI A.S.", 6069.51], ["2020", "AIR TOTAL INTERNATIONAL S.A", 6011043.757], ["2020", "TAMOIL ITALIA S.P.A.", 622150.365]]
            },
            "chart_type": "table"
        }

    elif "vols" in q or "consommateurs" in q:
        return {
            "intent": "VOLS_LES_PLUS_CONSOMMATEURS",
            "reponse": "La ligne Paris (ORY) - Tunis (TUN) est la plus énergivore en raison de la fréquence élevée des vols et de l'utilisation d'appareils plus anciens sur ce trajet.",
            "resultat": {
                "vols": [[2024, "ORY", "TUN", 9, 128163.6, 1], [2024, "TUN", "ORY", 8, 88329.7, 2], [2024, "TUN", "IST", 3, 75000.0, 3]]
            },
            "chart_type": "bar"
        }
    
    return {
        "intent": "GENERAL_INFO", 
        "reponse": "Tunisair utilise principalement du Jet A-1. Pour optimiser la consommation, il est conseillé de surveiller le 'Tankering' sur les escales où le prix est plus bas.", 
        "resultat": None
    }

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE & LOGIC
# ─────────────────────────────────────────────────────────────────────────────

saved_msgs = local_storage.getItem("chat_history")
saved_res = local_storage.getItem("last_result")

if "messages" not in st.session_state:
    st.session_state.messages = saved_msgs if saved_msgs else []

if "last_result" not in st.session_state:
    if saved_res == "null" or saved_res is None:
        st.session_state.last_result = None
    else:
        st.session_state.last_result = saved_res
def process_question(question: str):
    if not question.strip(): return
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.spinner("Analyse..."):
        time.sleep(0.4)
        result = fake_api(question)
        result["timestamp"] = time.time() 
        
        bot_text = result.get("reponse", result.get("response", "Analyse terminée."))
        
        st.session_state.messages.append({"role": "bot", "content": bot_text})
        st.session_state.last_result = result
        
    st.session_state.needs_save = True

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR: HISTORY
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.image("Tunisair_logo.png", use_container_width=True) 
    st.markdown(f"<h2 style='color:{TUNISAIR_RED}; font-size:1.2rem;'>Historique</h2>", unsafe_allow_html=True)
    st.divider()
    if not st.session_state.messages:
        st.write("Aucun historique.")
    for msg in st.session_state.messages:
        label = "👤" if msg["role"] == "user" else "✈️"
        st.markdown(f"<div style='font-size:0.85rem; margin-bottom:10px;'><b>{label}</b> {msg['content']}</div>", unsafe_allow_html=True)
    
    if st.button("🗑️ Effacer"):
        st.session_state.messages = []
        st.session_state.last_result = None
        st.session_state.needs_save = False
        
        local_storage.setItem("chat_history", [], key="manual_clear_history")
        local_storage.setItem("last_result", None, key="manual_clear_res")
        
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN INTERFACE
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 20px; padding: 10px 0;">
        <img src="data:image/png;base64,{img_base64}" style="height: 60px; width: auto;">
        <h1 style="margin: 0; font-weight: 900; font-size: 2.5rem; white-space: nowrap;">
            TUNISAIR <span style="color:{TUNISAIR_RED};">ChatBot</span>
        </h1>
    </div>
    <div style="border-bottom: 4px solid {TUNISAIR_RED}; margin-bottom: 25px;"></div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown(f"""
        <p style="color: #666666; font-style: italic; font-size: 1.1rem; margin-bottom: 25px;">
            Bienvenue. Je suis votre assistant BI dédié à l’analyse des coûts et performances du carburant aviation. Je vous fournis des indicateurs clés, des tendances et des prévisions pour soutenir vos décisions stratégiques.
        </p>
    """, unsafe_allow_html=True)

# ── Result ──
if st.session_state.last_result and len(st.session_state.messages) > 0:
    res = st.session_state.last_result
    st.markdown('<div class="section-title">Analyse & Visualisation</div>', unsafe_allow_html=True)
    
    if res.get("resultat"):
        chart_box = st.container()
        with chart_box:
            st.markdown("""
                <style>
                    [data-testid="stVerticalBlock"] > div:has(div.stChart) {
                        border: none !important;
                        background: transparent !important;
                    }
                </style>
            """, unsafe_allow_html=True)

            if res["intent"] in ["EVOLUTION_DES_PRIX", "EVOLUTION_DES_TAXES"]:
                raw_data = list(res["resultat"].values())[0]
                df = pd.DataFrame(raw_data, columns=["Année", "Valeur"]).sort_values("Année")
                
                y_limit = df["Valeur"].max() * 1.2 
                
                chart = alt.Chart(df).mark_line(color=TUNISAIR_RED).encode(
                    x=alt.X('Année:N', title='Année'),
                    y=alt.Y('Valeur:Q', scale=alt.Scale(domain=[df["Valeur"].min() * 0.8, y_limit]), title='Valeur (USD)')
                ).properties(height=300)
                
                st.altair_chart(chart, use_container_width=True)
            
            elif res["intent"] == "DEPENSES_PAR_FOURNISSEUR":
                raw_data = list(res["resultat"].values())[0]
                df = pd.DataFrame(raw_data, columns=["Année", "Fournisseur", "Montant (TND)"])
                st.table(df)
                
            elif res["intent"] == "VOLS_LES_PLUS_CONSOMMATEURS":
                raw_data = list(res["resultat"].values())[0]
                processed_vols = [[f"{x[1]}-{x[2]}", x[4]] for x in raw_data]
                df = pd.DataFrame(processed_vols, columns=["Vol", "Consommation (GAL)"])
                st.bar_chart(df.set_index("Vol"), color=TUNISAIR_RED)

    if res.get("reponse") or res.get("response"):
        bot_text = res.get("reponse", res.get("response"))
        st.markdown(f"""
            <div style="color:{TEXT_BLACK}; line-height:1.6; font-size:1.1rem; margin-top: 10px; border: none !important;">
                {bot_text}
            </div>
        """, unsafe_allow_html=True)

# ── Input Area ──
st.markdown('<div class="section-title">Question</div>', unsafe_allow_html=True)
c1, c2 = st.columns([5, 1])
with c1:
    user_q = st.text_input("Recherche", placeholder="Tapez votre question...", label_visibility="collapsed")
with c2:
    if st.button("Envoyer") and user_q:
        process_question(user_q)
        st.rerun()

if st.session_state.get("needs_save"):
    local_storage.setItem("chat_history", st.session_state.messages, key="save_msgs_final")
    local_storage.setItem("last_result", st.session_state.last_result, key="save_res_final")
    
    st.session_state.needs_save = False