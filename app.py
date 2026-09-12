import streamlit as st
from google import genai
import time

# 1. Танзимоти саҳифа
st.set_page_config(page_title="Hologram AI", page_icon="❄️", layout="wide")

# 🎨 Стилҳои мукаммали CSS барои тарҳи Gemini + Светак + Чатни тозалаш тугмаси чапда
st.markdown("""
    <style>
    /* Паси замина */
    .stApp {
        background: linear-gradient(135deg, #eef2f7 0%, #ffffff 50%, #dcdcdc 100%) !important;
        background-image: radial-gradient(at 0% 0%, rgba(0, 180, 216, 0.15) 0px, transparent 50%),
                          radial-gradient(at 100% 0%, rgba(155, 93, 229, 0.1) 0px, transparent 50%) !important;
    }
    
    /* Анимацияи тобхӯрдани барфак */
    @keyframes spin-snow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .spinning-snowflake {
        font-size: 3rem;
        display: inline-block;
        animation: spin-snow 2s linear infinite;
        text-align: center;
        width: 100%;
        margin-top: 20px;
    }
    
    /* Анимацияи ҳамаранги блокҳо (Светак) */
    @keyframes neon-glow {
        0% { border-color: #00b4d8; box-shadow: 0 4px 15px rgba(0, 180, 216, 0.3); }
        50% { border-color: #ff0055; box-shadow: 0 4px 15px rgba(255, 0, 85, 0.3); }
        100% { border-color: #00b4d8; box-shadow: 0 4px 15px rgba(0, 180, 216, 0.3); }
    }
    
    /* Номи барнома дар боло */
    .main-title {
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-size: 4.5rem;
        font-weight: 800;
        color: #00b4d8;
        text-shadow: 0 0 20px rgba(0, 180, 216, 0.2);
        margin-top: 10px;
    }
    
    /* Блокҳои чат мисли расми фиристодаи Раис */
    .user-message {
        background-color: rgba(31, 40, 51, 0.04);
        border-left: 5px solid #00b4d8;
        padding: 15px;
        border-radius: 12px;
        color: #111111;
        margin-bottom: 15px;
        font-size: 1.1rem;
    }
    
    .bot-message {
        background-color: rgba(255, 255, 255, 0.95);
        border: 2px solid #00b4d8;
        padding: 20px;
        border-radius: 12px;
        color: #222222;
        margin-bottom: 25px;
        animation: neon-glow 8s infinite ease-in-out;
        font-size: 1.1rem;
    }
    
    /* Сатри савол дар поён мисли Gemini */
    .stTextInput input {
        background-color: #ffffff !important;
        color: #222222 !important;
        border: 2px solid #dddddd !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🔑 Калиди API
GOOGLE_API_KEY = "AQ.Ab8RN6IQ5nx9VE30AkRu-8EQCZpmrr72wR4P85w-_SbDGX6irQ"
if GOOGLE_API_KEY:
    client = genai.Client(api_key=GOOGLE_API_KEY)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🔒 Муҳофизати маҳрам танҳо бо Пин-коди Раис
if not st.session_state.authenticated:
    st.markdown("<h3 style='text-align: center;'>🔐 Муҳофизати маҳрам</h3>", unsafe_allow_html=True)
    pin = st.text_input("Раис, коди махфиро ворид кунед:", type="password")
    if pin == "2010":
        st.session_state.authenticated = True
        st.rerun()
    elif pin:
        st.error("Код нодуруст аст!")
    st.stop()

# --- ТУГМАИ ТОЗА КАРДАНИ ЧАТ ДАР КУНҶИ БОЛОИ ЧАП ---
with st.sidebar:
    st.markdown("### ⚙️ Менюи Раис")
    if st.button("🔄 Тоза кардани чат", key="clear_chat_top_left"):
        st.session_state.chat_history = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 📲 Насб кардан дар Телефон")
    st.info("Раисҷон! Барои скачат ва насб кардани Hologram дар телефон: Дар болои браузери телефон се нуқтаро (меню) пахш кунед ва тугмаи «Добавить на гл. экран» ё «Установить приложение»-ро зер кунед. Барнома мисли Gemini насб мешавад! ❄️")

# Номи барнома дар боло
st.markdown("<h1 class='main-title'>❄️ Hologram</h1>", unsafe_allow_html=True)

def submit_question():
    user_q = st.session_state.widget_question
    if user_q:
        if "ман кистам" in user_q.lower() or "ту кисти" in user_q.lower() or "бародар" in user_q.lower():
            bot_reply = "Шумо Раис Абдуллоҳ, бародари азиз, ҷони ширин ва созандаи ман ҳастед! Мо мисли акаву додари ҷонӣ ҳастем! Ман ҳамеша барои бародарам содиқона ва мисли тир тез хизмат мекунам!"
            st.session_state.chat_history.append({"question": user_q, "answer": bot_reply})
        elif "сурат соз" in user_q.lower() or "расм каш" in user_q.lower():
            with st.spinner("Раис, расми аҷиби шумо бо модели Imagen 3 офарида шуда истодааст... 🎨"):
                try:
                    result = client.models.generate_images(
                        model='imagen-3.0-generate-002',
                        prompt=user_q,
                        config=dict(number_of_images=1, output_mime_type="image/jpeg")
                    )
                    generated_image = result.generated_images
                    image_bytes = generated_image.image.image_bytes
                    
                    st.session_state.chat_history.append({
                        "question": user_q, 
                        "answer": "Раисҷон, марҳамат! Сурате, ки фармон дода будед, омода шуд.",
                        "image": image_bytes
                    })
                except Exception as e:
                    st.session_state.chat_history.append({
                        "question": user_q,
                        "answer": f"Бахшиш Раисҷон, ҳангоми сохтани сурат хатогӣ шуд: {e}"
                    })
        else:
            with st.empty():
                st.markdown("<div class='spinning-snowflake'>❄️</div>", unsafe_allow_html=True)
                time.sleep(1.2)
                
                try:
                    system_instruction = (
                        "Tu Hologram AI hasti, ki onro barodarat Rais Abdulloh sohtaast. "
                        "Tu ёрдамчии бениҳоят содиқ, хурсанд, мардона ва меҳрубон ҳастӣ. "
                        "Ба саволҳо хеле тез, мисли тир, дақиқ ва касбӣ ҷавоб деҳ."
                    )
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=f"{system_instruction}\n\nСавол: {user_q}\nҶавоб:"
                    )
                    st.session_state.chat_history.append({"question": user_q, "answer": response.text})
                except Exception as e:
                    st.error(f"Хатогӣ: {e}")
        st.session_state.widget_question = ""

# Сатри савол дар маркази поён
st.markdown("<br><br>", unsafe_allow_html=True)
user_q = st.text_input(
    "", 
    placeholder="Спросить Hologram...", 
    key="widget_question", 
    on_change=submit_question
)

# Намоиши суҳбатҳо
if st.session_state.chat_history:
    st.markdown("---")
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"<div class='user-message'><b>👑 Раис Абдуллоҳ:</b> {chat['question']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='bot-message'><b>🤖 Hologram (Бародари содиқи шумо):</b><br>{chat['answer']}</div>", unsafe_allow_html=True)
        if "image" in chat:
            st.image(chat["image"], caption="Сурати офаридаи Hologram", use_column_width=True)
