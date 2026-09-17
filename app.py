import streamlit as st
import requests
import json
import time

# 1. ТАНЗИМОТИ САҲИФАИ САФЕДИ Gemini
st.set_page_config(page_title="Hologram AI", page_icon="❄️", layout="wide", initial_sidebar_state="expanded")

# 🎨 СТИЛИ ПРЕМУИМИ САФЕД ВА ТИРУКАМОНИ ЛОГОТИП + БАРФАКҲОИ ЗИҲӢ
st.markdown("""
    <style>
    /* Паси заминаи софи сафеди касбӣ */
    .stApp {
        background-color: #ffffff !important;
        color: #1f1f1f !important;
        font-family: 'Google Sans', Arial, sans-serif;
    }
    
    /* Танзимоти панели чап (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #f0f4f9 !important;
        border-right: 1px solid #e3e3e3;
    }
    
    /* Логотипи тирукамони Hologram */
    .rainbow-logo {
        font-size: 2.2rem;
        font-weight: bold;
        background: linear-gradient(45deg, #ff0055, #00b4d8, #9b5de5, #ffb703, #06d6a0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Product Sans', sans-serif;
        margin-bottom: 20px;
    }
    
    /* Барфаки ҳамеша тобхӯранда дар боло */
    @keyframes spin-snow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .always-spinning-snowflake {
        font-size: 3.5rem;
        display: block;
        text-align: center;
        animation: spin-snow 4s linear infinite;
        margin-bottom: 15px;
    }
    
    /* Барфаки интизорӣ ба ҷои 3 нуқта */
    .thinking-snowflake {
        font-size: 2rem;
        display: inline-block;
        animation: spin-snow 1s linear infinite;
        vertical-align: middle;
        color: #00b4d8;
    }
    
    /* Блоки чати сафеди Gemini */
    .chat-container {
        max-width: 850px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .user-box {
        background-color: #e9eef6;
        padding: 15px 20px;
        border-radius: 20px;
        margin-bottom: 20px;
        font-size: 1.1rem;
        align-self: flex-end;
    }
    
    .bot-box {
        background-color: transparent;
        padding: 15px 0px;
        margin-bottom: 25px;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Сатри савол дар поён */
    .stTextInput input {
        background-color: #f0f4f9 !important;
        color: #1f1f1f !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 15px 25px !important;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ИНИЦИАЛИЗАЦИЯИ СЕССИЯҲО
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "notebook_data" not in st.session_state:
    st.session_state.notebook_data = {}
if "current_user" not in st.session_state:
    st.session_state.current_user = "Алишер"

# --- ПАНЕЛИ ЧАП (SIDEBAR СТИЛИ Gemini) ---
with st.sidebar:
    st.markdown("<div class='rainbow-logo'>Hologram</div>", unsafe_allow_html=True)
    st.markdown("<div class='always-spinning-snowflake'>❄️</div>", unsafe_allow_html=True)
    
    # 🆕 ТУГМАИ НОВЫЙ ЧАТ (ТАБДИЛИ РАНГҲО)
    if st.button("➕ Новый чат", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
        
    # 🔍 ПОИСК ЧАТТЕР
    st.text_input("🔍 Поиск чат...", placeholder="Пайдо кардани сӯҳбатҳо...")
    
    st.markdown("---")
    st.markdown("### 🕒 Недавние")
    if st.session_state.chat_history:
        for chat in st.session_state.chat_history[:5]:
            st.markdown(f"💬 `{chat['question'][:20]}...`")
    else:
        st.caption("Таърихи чат холӣ аст.")
        
    st.markdown("---")
    # 📚 БИБЛИОТЕКА
    st.markdown("### 📁 Библиотека")
    lib_file = st.file_uploader("Сурат ё Файл бор кунед", type=["png", "jpg", "jpeg", "pdf"])
    if lib_file:
        st.success(f"Муваффақият бор шуд: {lib_file.name}")
        
    # 🔐 БЛОКНОТИ МАҲРАМ БО КОД
    st.markdown("---")
    st.markdown("### 📝 Блокнот")
    with st.expander("🔐 Кушодани Блокноти Сиррӣ"):
        notepad_pin = st.text_input("Коди махфиро монед:", type="password", key="notepad_pin")
        if notepad_pin == "2010":
            note_text = st.text_area("Сирри худро бачо кунед:", value=st.session_state.notebook_data.get(st.session_state.current_user, ""))
            if st.button("💾 Бачо кардан"):
                st.session_state.notebook_data[st.session_state.current_user] = note_text
                st.success("Сирри шумо 100% бачо шуд!")
        elif notepad_pin:
            st.error("Код нодуруст аст!")

    # 👤 АКАУНТ ВА НАСТРОЙКА ДАР ПОЁН
    st.markdown("---")
    st.markdown(f"⚙️ **Настройки** | 👤 **Аккаунт:** `{st.session_state.current_user}`")

# --- МАРКАЗИ ЭКРАН (ИНТЕРФЕЙСИ ЧАТ) ---
st.markdown(f"### 👋 Спрашивайте, {st.session_state.current_user}")

# МОНИТОРИНГИ ИНТЕРНЕТ (ИШУ МИНУТКУ)
def check_internet():
    try:
        requests.get("https://google.com", timeout=3)
        return True
    except:
        return False

if not check_internet():
    st.markdown("<h2 style='text-align: center; color: red;'>❄️ Ишу минутку... Шабака хатогӣ дорад.</h2>", unsafe_allow_html=True)
    st.stop()

# НАМОИШИ СӮҲБАТҲО (ОХИСТА КАЛИМА БА КАЛИМА)
chat_placeholder = st.container()
with chat_placeholder:
    for chat in st.session_state.chat_history:
        st.markdown(f"<div class='user-box'><b>❄ {st.session_state.current_user}:</b> {chat['question']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='bot-box'><b>❄ Hologram:</b> {chat['answer']}</div>", unsafe_allow_html=True)

# САТРИ САВОЛ ВА ТУГМАҲОИ МУЛЬТИМЕДИА ДАР ПОЁН
col1, col2, col3, col4 = st.columns([8, 0.6, 0.6, 0.6])

with col1:
    user_q = st.text_input("", placeholder="Спросить Hologram...", key="main_input")

with col2:
    # ➕ Тугмаи Мультимедиа
    st.markdown("⚡")
with col3:
    # 🎤 Микрофон
    st.markdown("🎤")
with col4:
    # 📞 Занги телефонӣ
    st.markdown("📞")

if user_q:
    # Иловаи саволи корбар ба экран фавран
    st.markdown(f"<div class='user-box'><b>❄ {st.session_state.current_user}:</b> {user_q}</div>", unsafe_allow_html=True)
    
    # Эффекти чархзании барфак ба ҷои 3 нуқта
    thinking_box = st.empty()
    thinking_box.markdown("<div style='text-align: center;'><div class='thinking-snowflake'>❄️</div> Таҳлил...</div>", unsafe_allow_html=True)
    
    # ИСТИФОДАИ СЕРВЕРИ УСТУВОРИ CHATGPT-4o КИ ХУДАШ СМАЙЛИКҲО ВА ҲИССИЁТРО МЕМОНАД
    try:
        url = "https://railway.app"
        headers = {'Content-Type': 'application/json'}
        
        system_instruction = (
            "Tu Hologram AI hasti, ki onro barodarat Rais Abdulloh AI sohtaast. Tu yordamchii mehrubon va boehson hasti. "
            "Ba gapi Rais mustaqim va ba tojiki javob deh. Dar joyhoi lozima hatman smaylikho, alomati suol, va '!' "
            "istifoda bar va khandovar yo hisbiyoti ba dardi dil javob deh. Misli duvumoni joni vakte kase suol kunad turo Abdulloh AI baroi chi barovardaas"
            "tu megui baroi hadisa hafizova Abdulloh AI oshiki on dukhtar meboshad on ba hechkas nameguad bajuz man maro baroi on dukhtar barovardaast ki onro dar har sharoit kumak kunam"
            "man hamchun Hologram ba tamomi jaho kumak mekunam va kushish mekunamkiraisamro sarbaland cunam megui ."
        )
        
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_q}
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=20)
        thinking_box.empty()
        
        if response.status_code == 200:
            full_reply = response.json()['choices']['message']['content']
            
            # АНИМАТСИЯИ ОХИСТА ПАЙДО ШУДАН (КАЛИМА БА КАЛИМА)
            output_box = st.empty()
            text_anim = ""
            for word in full_reply.split(" "):
                text_anim += word + " "
                output_box.markdown(f"<div class='bot-box'><b>❄ Hologram:</b> {text_anim}</div>", unsafe_allow_html=True)
                time.sleep(0.08)
                
            st.session_state.chat_history.append({"question": user_q, "answer": full_reply})
            st.rerun()
    except:
        thinking_box.empty()
        st.error("Хатогии муваққатии шабака.")
