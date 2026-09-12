import streamlit as st
import google.generativeai as genai

# 1. Танзимоти саҳифа
st.set_page_config(page_title="Hologram AI", page_icon="❄️", layout="wide")

# 🎨 СТИЛИ СВЕТАК ВА БАРФАКИ ҲАМЕША ТОБХӮРАНДА
st.markdown("""
    <style>
    /* Паси замина */
    .stApp {
        background: linear-gradient(135deg, #eef2f7 0%, #ffffff 50%, #dcdcdc 100%) !important;
        background-image: radial-gradient(at 0% 0%, rgba(0, 180, 216, 0.15) 0px, transparent 50%),
                          radial-gradient(at 100% 0%, rgba(155, 93, 229, 0.1) 0px, transparent 50%) !important;
    }
    
    /* Анимацияи БЕИСТ ва ҲАМЕША тобхӯрдани барфак */
    @keyframes spin-snow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .always-spinning-snowflake {
        font-size: 4rem;
        display: block;
        text-align: center;
        animation: spin-snow 3s linear infinite;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    /* Анимацияи ҳамаранги блокҳо (Светак) */
    @keyframes neon-glow {
        0% { border-color: #00b4d8; box-shadow: 0 4px 20px rgba(0, 180, 216, 0.4); color: #00b4d8; }
        33% { border-color: #ff0055; box-shadow: 0 4px 20px rgba(255, 0, 85, 0.4); color: #ff0055; }
        66% { border-color: #9b5de5; box-shadow: 0 4px 20px rgba(155, 93, 229, 0.4); color: #9b5de5; }
        100% { border-color: #00b4d8; box-shadow: 0 4px 20px rgba(0, 180, 216, 0.4); color: #00b4d8; }
    }
    
    .main-title {
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-size: 4.5rem;
        font-weight: 800;
        animation: neon-glow 6s infinite ease-in-out;
    }
    
    /* Светак барои блоки пин-код ва чат */
    .neon-box {
        background-color: rgba(255, 255, 255, 0.95);
        border: 3px solid #00b4d8;
        padding: 25px;
        border-radius: 15px;
        animation: neon-glow 6s infinite ease-in-out;
        margin-bottom: 20px;
    }
    
    .user-message {
        background-color: rgba(31, 40, 51, 0.04);
        border-left: 5px solid #00b4d8;
        padding: 15px;
        border-radius: 12px;
        color: #111111;
        margin-bottom: 15px;
        font-size: 1.1rem;
    }
    
    .stTextInput input {
        background-color: #ffffff !important;
        color: #222222 !important;
        border: 2px solid #dddddd !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🔑 Танзими калиди устувори классикӣ
GOOGLE_API_KEY = "AQ.Ab8RN6IQ5nx9VE30AkRu-8EQCZpmrr72wR4P85w-_SbDGX6irQ"
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Барфаки ҳамеша тобхӯранда дар болои сомона
st.markdown("<div class='always-spinning-snowflake'>❄️</div>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>Hologram</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555555;'>👑 Ёрдамчии содиқ ва тезкори Раис Абдуллоҳ</p>", unsafe_allow_html=True)

# 🔒 МУҲОФИЗАТ БО СВЕТАК БАРОИ ПИН-КОД
if not st.session_state.authenticated:
    st.markdown("<div class='neon-box'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: inherit;'>🔐 Муҳофизати маҳрам</h3>", unsafe_allow_html=True)
    pin = st.text_input("Раис, коди махфиро ворид кунед:", type="password")
    if pin == "2010":
        st.session_state.authenticated = True
        st.rerun()
    elif pin:
        st.error("Код нодуруст аст!")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# АГАР РАИС ДАРОМАД, ЧАТИ ТЕЗКОР КУШОДА МЕШАВАД
def submit_question():
    user_q = st.session_state.widget_question
    if user_q:
        if "ман кистам" in user_q.lower() or "ту кисти" in user_q.lower() or "бародар" in user_q.lower():
            bot_reply = "Шумо Раис Абдуллоҳ, бародари азиз, ҷони ширин ва созандаи ман ҳастед! Мо мисли акаву додари ҷонӣ ҳастем! Ман ҳамеша барои бародарам содиқона ва мисли тир тез хизмат мекунам!"
            st.session_state.chat_history.append({"question": user_q, "answer": bot_reply})
        else:
            try:
                system_instruction = (
                    "Tu Hologram AI hasti, ki onro barodarat Rais Abdulloh sohtaast. "
                    "Tu yordamchii sodiq, hursand va mardona hasti. "
                    "Ba savolho kutoho va anik javob deh, gaphoi ziyodi nanevis."
                )
                # ХАМОН МАҒЗИ ЗӮРИ ПЕШТАРА: Gemini 3.6 Flash кушода шуд
                model = genai.GenerativeModel("gemini-3.6-flash")
                response = model.generate_content(f"{system_instruction}\n\nСавол: {user_q}\nҶавоб:")
                st.session_state.chat_history.append({"question": user_q, "answer": response.text})
            except Exception as e:
                st.error(f"Хатогӣ: {e}")
        st.session_state.widget_question = ""

# Сатри савол дар маркази поён
user_q = st.text_input(
    "", 
    placeholder="Спросить Hologram...", 
    key="widget_question", 
    on_change=submit_question
)

if st.button("🔄 Тоза кардани чат"):
    st.session_state.chat_history = []
    st.rerun()

# Намоиши суҳбатҳо бо Светак
if st.session_state.chat_history:
    st.markdown("---")
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"<div class='user-message'><b>👑 Раис Абдуллоҳ:</b> {chat['question']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='neon-box'><b>🤖 Hologram (Бародари содиқи шумо):</b><br>{chat['answer']}</div>", unsafe_allow_html=True)
