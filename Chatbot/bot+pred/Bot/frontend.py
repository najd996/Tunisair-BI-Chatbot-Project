import streamlit as st
import pandas as pd
import time
import base64
import altair as alt
import requests
from connexiondb import get_db_connection

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_image("plane.png")

#  CONFIG & THEME

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

#  CSS

st.markdown(f"""
<style>
            
    .stHtmlHeader a, 
    .st-emotion-cache-15zrgzn, 
    [data-testid="stHeaderActionElements"] {{
        display: none !important;
    }}

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
        color: {TUNISAIR_RED} !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        font-size: 0.9rem !important;
        letter-spacing: 2px;
        margin: 35px 0 15px 0;
        line-height: 1.6 !important;
        display: block !important;
        overflow: visible !important;
        white-space: normal !important;
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

    .stButton.feedback-btn button {{
        width: auto !important;
        padding: 2px 15px !important;
        font-size: 1.2rem !important;
        background-color: transparent !important;
        border: 1px solid {BORDER_GREY} !important;
        color: {TEXT_BLACK} !important;
    }}
    .stButton.feedback-btn button:hover {{
        border-color: {TUNISAIR_RED} !important;
        background-color: #fde8ea !important;
    }}
    
    /* Style pour le message de remerciement feedback */
    .feedback-thanks {{
        color: #28a745;
        font-size: 0.9rem;
        font-style: italic;
        margin-top: 8px;
    }}
</style>
""", unsafe_allow_html=True)

# API

def check_backend_health():
    try:
        requests.get("http://localhost:8000/", timeout=0.5)
        return True
    except:
        return False
    
def check_oracle_health():
    if get_db_connection() is None: 
        return False
    return True

def extract_reponse(res):
    reponse = res.get("reponse", res.get("response", ""))
    if isinstance(reponse, dict):
        return reponse.get("content", str(reponse))
    return str(reponse)

def chat(question):
    try:
        response = requests.post(
            "http://localhost:8000/chat", 
            json={"question": question}
        )
        return response.json()
    except Exception as e:
        return {
            "intent": "ERROR",
            "response": "Erreur de connexion au serveur backend. Veuillez réessayer plus tard.",
            "resultat": None
        }

def send_feedback(question, reponse, feedback_type, intents):
    try:
        response = requests.post(
            "http://localhost:8000/feedback",
            json={
                "question": question,
                "reponse": reponse,
                "type": feedback_type,
                "intents": intents
            }
        )
        if response.status_code == 200:
            st.toast(f"Merci ! Feedback {feedback_type} enregistré.", icon="✅")
            st.session_state.feedback_given = True
            st.rerun()
        else:
            st.error("Erreur serveur lors de l'enregistrement.")
    except Exception as e:
        st.error(f"Erreur de connexion au backend")

#  SESSION STATE & LOGIC

if "session_id" not in st.session_state:
    st.session_state.session_id = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

def process_question(q):
    if not q.strip(): return

    st.session_state.last_result = None

    st.session_state.messages.append({"role":"user","content":q})

    with st.spinner("Analyse..."):
        time.sleep(0.4)
        res = chat(q)

    st.session_state.last_result = res
    st.session_state.feedback_given = False

    st.rerun()  

#  SIDEBAR

with st.sidebar:
    st.image("Tunisair_logo.png", use_container_width=True)
    st.divider()

    st.markdown(f"<p style='font-size:0.9rem; color:#666; font-weight:bold; margin-bottom:15px;'>État du Système</p>", unsafe_allow_html=True)
    
    is_backend_online = check_backend_health()
    bi_color = "#28a745" if is_backend_online else "#dc3545"
    bi_text = "Connecté" if is_backend_online else "Hors ligne"

    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <span style="height: 10px; width: 10px; background-color: {bi_color}; border-radius: 50%; display: inline-block; box-shadow: 0 0 5px {bi_color};"></span>
            <span style="font-size: 0.85rem; font-weight: 600;">Serveur : {bi_text}</span>
        </div>
    """, unsafe_allow_html=True)

    is_oracle_online = check_oracle_health()

    ora_color = "#28a745" if is_oracle_online else "#dc3545"
    ora_text = "Actif" if is_oracle_online else "Inaccessible"

    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
            <span style="height: 10px; width: 10px; background-color: {ora_color}; border-radius: 50%; display: inline-block; box-shadow: 0 0 5px {ora_color};"></span>
            <span style="font-size: 0.85rem; font-weight: 600;">Base de Données : {ora_text}</span>
        </div>
    """, unsafe_allow_html=True)

    from datetime import datetime
    current_date = datetime.now().strftime("%d/%m/%Y")
    st.caption(f"📅 Données à jour : {current_date}")
    
    st.divider()

#  MAIN INTERFACE

st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 20px; padding: 10px 0;">
        <img src="data:image/png;base64,{img_base64}" style="height: 60px; width: auto;">
        <h1 style="margin: 0; font-weight: 900; font-size: 2.5rem; white-space: nowrap;">
            TUNISAIR <span style="color:{TUNISAIR_RED};">BI Consultant</span>
        </h1>
    </div>
    <div style="border-bottom: 4px solid {TUNISAIR_RED}; margin-bottom: 25px;"></div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown(f"""
        <p style="color: #666666; font-style: italic; font-size: 1.1rem; margin-bottom: 25px;">
            Bienvenue. Je suis votre assistant BI dédié à l'analyse des coûts et performances du carburant aviation. Je vous fournis des indicateurs clés, des tendances et des prévisions pour soutenir vos décisions stratégiques.
        </p>
    """, unsafe_allow_html=True)

#  Result 

if st.session_state.last_result and len(st.session_state.messages) > 0:
    res = st.session_state.last_result
    intents = res.get("tools", [])

    if res.get("intent") == "ERROR":
        st.markdown('<p class="section-title">Erreur</p>', unsafe_allow_html=True)
        error_msg = res.get("response", "Le serveur backend est indisponible.")
        st.error(f"🚫 {error_msg}")
    
    else:
        tools = res.get("tools", [])
        resultats = res.get("resultat", {}) or {}

        st.markdown('<p class="section-title">Analyse & Visualisation</p>', unsafe_allow_html=True)

        if tools:
            badges = " ".join([
                f'<span style="background:#fde8ea; color:{TUNISAIR_RED};'
                f'padding:3px 10px; border-radius:12px; font-size:0.75rem;'
                f'font-weight:600; margin:2px; white-space: nowrap;"> {t}</span>'
                for t in tools
            ])
            st.markdown(f"<div style='margin-bottom:12px;'>{badges}</div>", unsafe_allow_html=True)

        for tool_name, tool_data in resultats.items():
            if not tool_data:
                continue

            if tool_name == "synthese_annuelle":
                items = list(tool_data.items())
                for i in range(0, len(items), 2):
                    cols = st.columns(2)
                    for j, (label, rows) in enumerate(items[i:i+2]):
                        if rows:
                            cols[j].metric(label=label.strip(), value=f"{rows[0][1]:,.2f}")

            elif tool_name in ("evolution_des_prix", "evolution_des_taxes"):
                raw = list(tool_data.values())[0]
                df = pd.DataFrame(raw, columns=["Année", "Valeur"]).sort_values("Année")
                chart = alt.Chart(df).mark_line(color=TUNISAIR_RED, point=True).encode(
                    x=alt.X("Année:N", title="Année"),
                    y=alt.Y("Valeur:Q", title="Valeur (USD/gal)", scale=alt.Scale(domain=[df["Valeur"].min()*0.9, df["Valeur"].max()*1.1]))
                ).properties(height=300)
                st.altair_chart(chart, use_container_width=True)

            elif tool_name == "depenses_par_fournisseur":
                raw = list(tool_data.values())[0]
                df = pd.DataFrame(raw, columns=["Année", "Fournisseur", "Montant (USD)"])
                st.dataframe(df, use_container_width=True, hide_index=True)

            elif tool_name == "vols_les_plus_consommateurs":
                raw = list(tool_data.values())[0]
                df = pd.DataFrame(raw, columns=["Année","Départ","Arrivée","Conso (L)","Rang"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            elif tool_name == "analyse_des_couts":
                raw = list(tool_data.values())[0]
                df = pd.DataFrame(raw, columns=["Année","Ratio_cout_carburant_par_dépense_totale"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            elif tool_name == "tendance_mensuelle":
                raw = list(tool_data.values())[0]
                raw2 =list(tool_data.values())[1]
                df = pd.DataFrame(raw, columns=["Année","Mois", "CONSOMMATION_GALLON_AMÉRICAIN"])
                st.dataframe(df, use_container_width=True, hide_index=True)
                df2 = pd.DataFrame(raw2, columns=["Année","Mois", "Dépense_USD"])
                st.dataframe(df2, use_container_width=True, hide_index=True)
            elif tool_name == "tendance_annuelle":
                raw = list(tool_data.values())[0]
                raw2 =list(tool_data.values())[1]
                df = pd.DataFrame(raw, columns=["Année", "CONSOMMATION_GALLON_AMÉRICAIN"])
                st.dataframe(df, use_container_width=True, hide_index=True)
                df2 = pd.DataFrame(raw2, columns=["Année", "Dépense_USD"])
                st.dataframe(df2, use_container_width=True, hide_index=True)
            elif tool_name == "consommation_moyenne_annuelle":
                raw = list(tool_data.values())[0]
                df = pd.DataFrame(raw, columns=["Année", "CONSOMMATION_GALLON_AMÉRICAIN"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            elif tool_name == "depense_moyenne_annuelle":
                raw = list(tool_data.values())[0]
                df = pd.DataFrame(raw, columns=["Année", "Dépense_USD"])
                st.dataframe(df, use_container_width=True, hide_index=True)

        bot_text = extract_reponse(res)
        if bot_text:
            st.markdown('<p class="section-title">Interprétation</p>', unsafe_allow_html=True)
            st.markdown(f"""
                <div style="background:white; border-left:4px solid {TUNISAIR_RED};
                            border-radius:8px; padding:20px; line-height:1.7;
                            font-size:1rem; margin-top:10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    {bot_text}
                </div>
            """, unsafe_allow_html=True)

            last_user_msg = next((m['content'] for m in reversed(st.session_state.messages) if m['role'] == 'user'), "")
            
            if st.session_state.feedback_given:
                st.markdown("""
                    <p class="feedback-thanks">✓ Merci pour votre retour !</p>
                """, unsafe_allow_html=True)
            else:
                col_fb1, col_fb2, _ = st.columns([0.1, 0.1, 0.8])
                
                with col_fb1:
                    if st.button("👍", key="btn_like"):
                        send_feedback(last_user_msg, bot_text, "LIKE", intents)

                with col_fb2:
                    if st.button("👎", key="btn_dislike"):
                        send_feedback(last_user_msg, bot_text, "DISLIKE", intents)

#  Input Area 

st.markdown('<p class="section-title">Question</p>', unsafe_allow_html=True)
c1, c2 = st.columns([5, 1])
with c1:
    user_q = st.text_input("Recherche", placeholder="Tapez votre question...", label_visibility="collapsed")
with c2:
    if st.button("Envoyer") and user_q:
        process_question(user_q)
        st.rerun()