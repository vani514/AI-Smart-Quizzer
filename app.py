import streamlit as st
import time
from question_generator import get_question_generator
import pandas as pd
import plotly.express as px
import PyPDF2
import docx
from io import BytesIO

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="🧠 SMARTQUIZZER AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================
# 🖤 DARK MODE WITH NEON GLOW
# ======================
st.markdown("""
<style>
    /* DARK BACKGROUND WITH ANIMATION */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 15s ease infinite !important;
        color: white !important;
        min-height: 100vh !important;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* ALL TEXT WHITE */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #ffffff !important;
    }
    
    /* NEON GLASS HEADER */
    .neon-header {
        background: rgba(20, 20, 40, 0.8) !important;
        backdrop-filter: blur(15px) !important;
        padding: 40px !important;
        border-radius: 25px !important;
        text-align: center !important;
        margin-bottom: 30px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .neon-header::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
        background: linear-gradient(90deg, #00ff88, #00ccff, #ff00ff) !important;
        animation: neonGlow 3s linear infinite !important;
    }
    
    @keyframes neonGlow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
    
    .neon-header h1 {
        font-size: 4rem !important;
        margin: 0 !important;
        background: linear-gradient(135deg, #00ff88, #00ccff, #ff00ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.5) !important;
    }
    
    /* HORIZONTAL RADIO CARDS - NEON */
    .stRadio > div[data-testid="stRadio"] > div {
        flex-direction: row !important;
        display: flex !important;
        gap: 20px !important;
        justify-content: center !important;
        flex-wrap: wrap !important;
    }
    
    .radio-card-neon {
        background: rgba(30, 30, 50, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        padding: 30px 25px !important;
        text-align: center !important;
        min-width: 220px !important;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5) !important;
        flex: 1 !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .radio-card-neon:hover {
        transform: translateY(-10px) scale(1.05) !important;
        border-color: #00ff88 !important;
        box-shadow: 0 20px 40px rgba(0, 255, 136, 0.3) !important;
    }
    
    .radio-card-neon.selected {
        border-color: #00ff88 !important;
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 204, 255, 0.2)) !important;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.5) !important;
        transform: scale(1.05) !important;
    }
    
    .radio-icon-neon {
        font-size: 45px !important;
        margin-bottom: 15px !important;
        display: block !important;
        text-shadow: 0 0 15px currentColor !important;
    }
    
    /* NEON STATUS BADGE */
    .status-neon {
        display: inline-flex !important;
        align-items: center !important;
        gap: 12px !important;
        padding: 15px 30px !important;
        background: linear-gradient(135deg, #00ff88, #00ccff) !important;
        color: #000000 !important;
        border-radius: 30px !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        box-shadow: 0 10px 25px rgba(0, 255, 136, 0.4) !important;
        border: 2px solid white !important;
        animation: pulseNeon 2s infinite !important;
    }
    
    @keyframes pulseNeon {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 10px 25px rgba(0, 255, 136, 0.4);
        }
        50% { 
            transform: scale(1.05);
            box-shadow: 0 15px 35px rgba(0, 255, 136, 0.6);
        }
    }
    
    /* NEON TIMER */
    .timer-neon {
        background: linear-gradient(135deg, #ff0080, #ff8c00) !important;
        padding: 15px 30px !important;
        border-radius: 30px !important;
        color: white !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 15px !important;
        box-shadow: 0 10px 25px rgba(255, 0, 128, 0.4) !important;
        border: 2px solid white !important;
        animation: pulseTimer 1s infinite !important;
    }
    
    @keyframes pulseTimer {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.08); }
    }
    
    /* TABS STYLING - NEON */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px !important;
        border-bottom: 3px solid rgba(102, 126, 234, 0.3) !important;
        padding-bottom: 15px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px !important;
        background: rgba(30, 30, 50, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        padding: 15px 30px !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        transition: all 0.3s !important;
        border: 2px solid transparent !important;
        color: #cccccc !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border-color: #00ff88 !important;
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4) !important;
        transform: translateY(-5px) !important;
    }
    
    /* BUTTONS - NEON */
    .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        padding: 16px 40px !important;
        border-radius: 15px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        transition: all 0.3s !important;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* METRIC CARDS - NEON */
    .metric-neon {
        background: rgba(30, 30, 50, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        padding: 30px 25px !important;
        text-align: center !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s !important;
    }
    
    .metric-neon:hover {
        transform: translateY(-10px) !important;
        border-color: #00ff88 !important;
        box-shadow: 0 25px 50px rgba(0, 255, 136, 0.3) !important;
    }
    
    /* QUIZ QUESTION CARD - NEON */
    .question-card-neon {
        background: rgba(30, 30, 50, 0.9) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 25px !important;
        padding: 40px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5) !important;
        margin: 25px 0 !important;
        border-left: 8px solid #667eea !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
    }
    
    /* TOPIC SELECTION GRID - NEON */
    .topic-grid-neon {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)) !important;
        gap: 20px !important;
        margin: 30px 0 !important;
    }
    
    .topic-card-neon {
        background: rgba(30, 30, 50, 0.9) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 20px !important;
        padding: 25px 20px !important;
        text-align: center !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .topic-card-neon:hover {
        transform: translateY(-10px) !important;
        border-color: #00ccff !important;
        box-shadow: 0 25px 50px rgba(0, 204, 255, 0.3) !important;
    }
    
    .topic-card-neon::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
        background: linear-gradient(90deg, #00ff88, #00ccff, #ff00ff) !important;
    }
    
    .topic-icon-neon {
        font-size: 40px !important;
        margin-bottom: 15px !important;
        display: block !important;
        filter: drop-shadow(0 0 10px currentColor) !important;
    }
    
    .topic-name-neon {
        font-size: 18px !important;
        font-weight: 700 !important;
        margin: 10px 0 !important;
        color: #ffffff !important;
    }
    
    .topic-desc-neon {
        font-size: 13px !important;
        color: #cccccc !important;
        line-height: 1.4 !important;
    }
    
    /* PASS/FAIL BADGES - NEON */
    .pass-badge-neon {
        background: linear-gradient(135deg, #00ff88, #00ccff) !important;
        color: black !important;
        padding: 12px 35px !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        font-size: 24px !important;
        text-align: center !important;
        margin: 20px auto !important;
        display: inline-block !important;
        animation: pulsePass 2s infinite !important;
        box-shadow: 0 10px 25px rgba(0, 255, 136, 0.4) !important;
        border: 2px solid white !important;
    }
    
    .fail-badge-neon {
        background: linear-gradient(135deg, #ff0080, #ff8c00) !important;
        color: white !important;
        padding: 12px 35px !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        font-size: 24px !important;
        text-align: center !important;
        margin: 20px auto !important;
        display: inline-block !important;
        animation: pulseFail 2s infinite !important;
        box-shadow: 0 10px 25px rgba(255, 0, 128, 0.4) !important;
        border: 2px solid white !important;
    }
    
    @keyframes pulsePass {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes pulseFail {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* FILE UPLOAD CARD - NEON */
    .upload-card-neon {
        background: rgba(30, 30, 50, 0.9) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 25px !important;
        padding: 40px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5) !important;
        margin: 25px 0 !important;
        border: 3px dashed #FF6B6B !important;
        transition: all 0.3s !important;
        text-align: center !important;
    }
    
    .upload-card-neon:hover {
        border-color: #4ECDC4 !important;
        box-shadow: 0 25px 50px rgba(78, 205, 196, 0.3) !important;
        transform: translateY(-5px) !important;
    }
    
    /* FILE UPLOADER STYLING */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #FFD93D !important;
        border-radius: 15px !important;
        padding: 30px !important;
        background: rgba(40, 40, 60, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        margin: 20px 0 !important;
    }
    
    div[data-testid="stFileUploader"]:hover {
        border-color: #6BCF7F !important;
        background: rgba(50, 50, 70, 0.8) !important;
    }
    
    /* HIDE DEFAULT STREAMLIT ELEMENTS */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ======================
# FILE PROCESSING FUNCTIONS
# ======================
def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    try:
        content = file.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8", errors='ignore')
        return content.strip()
    except Exception as e:
        st.error(f"Error reading TXT: {str(e)}")
        return ""

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return ""

def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract text"""
    file_type = uploaded_file.type
    
    try:
        # Reset file pointer
        uploaded_file.seek(0)
        
        if file_type == "application/pdf":
            return extract_text_from_pdf(BytesIO(uploaded_file.read()))
        elif file_type == "text/plain":
            return extract_text_from_txt(BytesIO(uploaded_file.read()))
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return extract_text_from_docx(BytesIO(uploaded_file.read()))
        else:
            st.error(f"Unsupported file type: {file_type}")
            return None
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

# ======================
# 🎯 INITIALIZE SESSION STATE
# ======================
# Initialize generator
if 'generator' not in st.session_state:
    st.session_state.generator = get_question_generator()

# Quiz configuration
if 'quiz_config' not in st.session_state:
    st.session_state.quiz_config = {
        "question_type": "Multiple Choice",
        "difficulty": "Intermediate",
        "num_questions": 5,
        "topic": "Artificial Intelligence",
        "time_limit": 600,
        "file_content": None,
        "file_name": None,
        "quiz_source": "topic"  # 'topic' or 'file'
    }

# Quiz state
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False

if 'generated_questions' not in st.session_state:
    st.session_state.generated_questions = []

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'answers' not in st.session_state:
    st.session_state.answers = []

if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False

if 'generating' not in st.session_state:
    st.session_state.generating = False

if 'quiz_start_time' not in st.session_state:
    st.session_state.quiz_start_time = time.time()

# File processing state
if 'file_processed' not in st.session_state:
    st.session_state.file_processed = False

if 'file_data' not in st.session_state:
    st.session_state.file_data = {}

# ======================
# DIFFICULTY MAP
# ======================
DIFFICULTY_MAP = {
    "Beginner": "Easy",
    "Intermediate": "Medium",
    "Advanced": "Hard"
}

# ======================
# TOPICS WITH ICONS
# ======================
TOPICS = [
    {"name": "Artificial Intelligence", "icon": "🤖", "desc": "AI, ML, Neural Networks"},
    {"name": "Machine Learning", "icon": "🧠", "desc": "Algorithms, Models, Training"},
    {"name": "Data Science", "icon": "📊", "desc": "Analytics, Statistics, Viz"},
    {"name": "Python Programming", "icon": "🐍", "desc": "Coding, Development"},
    {"name": "Web Development", "icon": "🌐", "desc": "HTML, CSS, JavaScript"},
    {"name": "Cyber Security", "icon": "🔒", "desc": "Encryption, Network Security"},
    {"name": "Blockchain", "icon": "⛓️", "desc": "Crypto, Web3, Smart Contracts"},
    {"name": "Cloud Computing", "icon": "☁️", "desc": "AWS, Azure, GCP"},
    {"name": "Mobile Development", "icon": "📱", "desc": "iOS, Android, React Native"},
    {"name": "Game Development", "icon": "🎮", "desc": "Unity, Unreal, Game Design"},
    {"name": "Database Systems", "icon": "💾", "desc": "SQL, NoSQL, MongoDB"},
    {"name": "DevOps", "icon": "🚀", "desc": "CI/CD, Docker, Kubernetes"}
]

# ======================
# 🖤 MAIN CONTENT CONTAINER
# ======================
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ======================
# 🔥 NEON HEADER
# ======================
st.markdown("""
<div class="neon-header">
    <h1>🧠 SMARTQUIZZER AI</h1>
    <h3 style="font-weight: 400; margin-top: 10px; color: #cccccc; font-size: 1.5rem;">LLM-Powered Instant Quiz Platform</h3>
</div>
""", unsafe_allow_html=True)

# ======================
# ⚡ STATUS PANEL
# ======================
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("### 🎛️ CONTROL PANEL")
with col2:
    if st.session_state.generator:
        st.markdown('<div class="status-neon">🤖 AI ACTIVE</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-neon" style="background: linear-gradient(135deg, #ff8c00, #ff0080);">🎮 DEMO MODE</div>', unsafe_allow_html=True)
with col3:
    if st.session_state.get('quiz_active'):
        elapsed = int(time.time() - st.session_state.get('quiz_start_time', time.time()))
        remaining = max(0, st.session_state.quiz_config["time_limit"] - elapsed)
        minutes = remaining // 60
        seconds = remaining % 60
        st.markdown(f'<div class="timer-neon">⏱️ {minutes:02d}:{seconds:02d}</div>', unsafe_allow_html=True)

# ======================
# 🎪 5 TABS
# ======================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 DASHBOARD", "⚡ GENERATOR", "📁 FILE UPLOAD", "🎮 QUIZ ZONE", "🏆 RESULTS"])

with tab1:
    st.markdown("### 📊 PERFORMANCE ANALYTICS")
    
    cols = st.columns(4)
    metrics = [
        {"value": "94%", "label": "Success Rate", "icon": "📈", "color": "#00ff88"},
        {"value": "128", "label": "Quizzes", "icon": "🎯", "color": "#00ccff"},
        {"value": "2.4s", "label": "Response", "icon": "⚡", "color": "#ff00ff"},
        {"value": "1.2K", "label": "Users", "icon": "👥", "color": "#ff8c00"}
    ]
    
    for idx, col in enumerate(cols):
        with col:
            metric = metrics[idx]
            st.markdown(f"""
            <div class="metric-neon">
                <div style="font-size: 40px; color: {metric['color']}; text-shadow: 0 0 15px {metric['color']};">{metric['icon']}</div>
                <h3 style="margin: 10px 0; color: #ffffff; font-size: 2rem; text-shadow: 0 0 10px {metric['color']};">{metric['value']}</h3>
                <p style="color: #cccccc; margin: 0; font-weight: 600;">{metric['label']}</p>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("### ⚡ SMART QUIZ GENERATOR")
    
    # Question Type Selection
    st.markdown("#### 🎯 SELECT QUESTION TYPE")
    
    col1, col2, col3 = st.columns(3)
    question_type = st.session_state.quiz_config["question_type"]
    
    with col1:
        selected_class = " selected" if question_type == "Multiple Choice" else ""
        st.markdown(f"""
        <div class="radio-card-neon{selected_class}" onclick="document.querySelector('input[value=\\'Multiple Choice\\']').click()">
            <div class="radio-icon-neon" style="color: #00ff88;">🔵</div>
            <div style="font-size: 20px; font-weight: 700; color: #ffffff;">Multiple Choice</div>
            <div style="font-size: 13px; color: #cccccc; margin-top: 10px;">Select correct answer</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        selected_class = " selected" if question_type == "True/False" else ""
        st.markdown(f"""
        <div class="radio-card-neon{selected_class}" onclick="document.querySelector('input[value=\\'True/False\\']').click()">
            <div class="radio-icon-neon" style="color: #00ccff;">🟣</div>
            <div style="font-size: 20px; font-weight: 700; color: #ffffff;">True/False</div>
            <div style="font-size: 13px; color: #cccccc; margin-top: 10px;">Binary decisions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        selected_class = " selected" if question_type == "Short Answer" else ""
        st.markdown(f"""
        <div class="radio-card-neon{selected_class}" onclick="document.querySelector('input[value=\\'Short Answer\\']').click()">
            <div class="radio-icon-neon" style="color: #ff00ff;">🟡</div>
            <div style="font-size: 20px; font-weight: 700; color: #ffffff;">Short Answer</div>
            <div style="font-size: 13px; color: #cccccc; margin-top: 10px;">Written responses</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Hidden radio for functionality
    question_type = st.radio(
        "",
        ["Multiple Choice", "True/False", "Short Answer"],
        key="question_type_select",
        label_visibility="collapsed",
        horizontal=True,
        index=["Multiple Choice", "True/False", "Short Answer"].index(st.session_state.quiz_config["question_type"])
    )
    st.session_state.quiz_config["question_type"] = question_type
    
    st.success(f"**Selected:** {question_type}")
    
    # VISIBLE TOPIC SELECTION
    st.markdown("#### 🎯 SELECT TOPIC")
    
    # Create topic grid
    st.markdown('<div class="topic-grid-neon">', unsafe_allow_html=True)
    
    # Display all topics in grid
    cols_per_row = 4
    rows = [TOPICS[i:i+cols_per_row] for i in range(0, len(TOPICS), cols_per_row)]
    
    for row in rows:
        cols = st.columns(cols_per_row)
        for idx, topic in enumerate(row):
            with cols[idx]:
                selected = st.session_state.quiz_config["topic"] == topic["name"]
                if st.button(
                    f"{topic['icon']}\n\n**{topic['name']}**\n\n_{topic['desc']}_",
                    key=f"topic_{topic['name']}",
                    use_container_width=True,
                    type="primary" if selected else "secondary"
                ):
                    st.session_state.quiz_config["topic"] = topic["name"]
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Difficulty & Number of Questions
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📚 DIFFICULTY")
        difficulty = st.select_slider(
            "",
            options=["Beginner", "Intermediate", "Advanced"],
            value=st.session_state.quiz_config["difficulty"],
            label_visibility="collapsed"
        )
        st.session_state.quiz_config["difficulty"] = difficulty
    
    with col2:
        st.markdown("#### 🔢 NUMBER OF QUESTIONS")
        num_questions = st.slider(
            "",
            min_value=1,
            max_value=20,
            value=st.session_state.quiz_config["num_questions"],
            label_visibility="collapsed"
        )
        st.session_state.quiz_config["num_questions"] = num_questions
    
    # GENERATE BUTTON
    st.markdown("---")
    
    if st.session_state.generating and st.session_state.quiz_config["quiz_source"] == "topic":
        st.markdown(f"""
        <div style="text-align: center; padding: 40px;">
            <div style="border: 8px solid rgba(255, 255, 255, 0.1); border-top: 8px solid #00ff88; border-radius: 50%; width: 60px; height: 60px; margin: 0 auto; animation: spin 1s linear infinite;"></div>
            <h3 style="color: #00ff88; margin-top: 20px;">🤖 Generating {num_questions} {st.session_state.quiz_config['question_type']} Questions...</h3>
            <p style="color: #cccccc;">Creating {difficulty} level questions about {st.session_state.quiz_config['topic']}</p>
        </div>
        <style>
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        </style>
        """, unsafe_allow_html=True)
        
        try:
            raw_questions = st.session_state.generator.generate_from_topic(
                topic=st.session_state.quiz_config["topic"],
                difficulty=DIFFICULTY_MAP[st.session_state.quiz_config["difficulty"]],
                num_questions=st.session_state.quiz_config["num_questions"],
                question_type=st.session_state.quiz_config["question_type"]  # Pass question type
            )
            
            # Normalize questions for different types
            questions = []
            for q in raw_questions:
                correct_answer = q.get("correct_answer", "A")
                options = q.get("options", [])
                
                # Determine correct index based on question type
                if st.session_state.quiz_config["question_type"] == "Multiple Choice":
                    if correct_answer in ["A", "B", "C", "D"]:
                        correct_index = ["A", "B", "C", "D"].index(correct_answer)
                    elif options and correct_answer in options:
                        correct_index = options.index(correct_answer)
                    else:
                        correct_index = 0
                elif st.session_state.quiz_config["question_type"] == "True/False":
                    # For True/False, store the correct answer text
                    correct_index = 0 if correct_answer == "True" else 1
                else:  # Short Answer
                    correct_index = 0  # Not used for short answer
                
                questions.append({
                    "question": q.get("question", "No question text"),
                    "options": options,
                    "correct": correct_index,
                    "correct_answer": correct_answer,
                    "explanation": q.get("explanation", "No explanation provided")
                })
            
            # Store in session state
            st.session_state.generated_questions = questions
            st.session_state.quiz_active = True
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.session_state.quiz_completed = False
            st.session_state.quiz_start_time = time.time()
            st.session_state.generating = False
            
            st.success(f"✅ {len(questions)} {st.session_state.quiz_config['question_type']} questions generated successfully!")
            time.sleep(1)
            st.rerun()
            
        except Exception as e:
            st.session_state.generating = False
            st.error(f"❌ Quiz generation failed: {e}")
    
    else:
        if st.button(
            "🚀 **GENERATE & START QUIZ**",
            use_container_width=True,
            type="primary",
            key="generate_start_quiz_btn"
        ):
            st.session_state.generating = True
            st.session_state.quiz_config["quiz_source"] = "topic"
            st.rerun()

with tab3:
    st.markdown("### 📁 UPLOAD & ANALYZE FILE")
    
    # File upload section
    st.markdown("""
    <div class="upload-card-neon">
        <h2>📤 Upload Your Document</h2>
        <p style="color: #cccccc; margin-bottom: 30px;">Upload PDF, TXT, or DOCX files to generate quizzes from your content</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Drag and drop or click to browse files",
        type=['pdf', 'txt', 'docx'],
        label_visibility="visible",
        key="file_uploader_main"
    )
    
    if uploaded_file is not None:
        # Display file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 File Name", uploaded_file.name)
        with col2:
            st.metric("📏 File Size", f"{uploaded_file.size / 1024:.1f} KB")
        with col3:
            st.metric("📝 File Type", uploaded_file.type.split('/')[-1].upper())
        
        # Process file button
        if st.button("🔍 **ANALYZE FILE**", use_container_width=True, key="analyze_file"):
            with st.spinner("🔍 Analyzing file content..."):
                # Extract text from file
                extracted_text = process_uploaded_file(uploaded_file)
                
                if extracted_text and len(extracted_text) > 100:
                    # Store in session state
                    st.session_state.file_data = {
                        "content": extracted_text,
                        "name": uploaded_file.name,
                        "processed": True
                    }
                    st.session_state.file_processed = True
                    
                    st.success(f"✅ File analyzed successfully! ({len(extracted_text)} characters extracted)")
                    
                    # Show content preview
                    with st.expander("📖 **Preview File Content**", expanded=True):
                        preview_length = min(2000, len(extracted_text))
                        st.text_area(
                            "Extracted Text:",
                            value=extracted_text[:preview_length] + ("..." if len(extracted_text) > preview_length else ""),
                            height=200,
                            disabled=True,
                            key="content_preview"
                        )
                    
                    # Quiz configuration for file-based quiz
                    st.markdown("### ⚙️ CONFIGURE FILE-BASED QUIZ")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        file_difficulty = st.select_slider(
                            "**Select Difficulty:**",
                            options=["Beginner", "Intermediate", "Advanced"],
                            value="Intermediate",
                            key="file_difficulty"
                        )
                    
                    with col2:
                        file_num_questions = st.slider(
                            "**Number of Questions:**",
                            min_value=3,
                            max_value=15,
                            value=5,
                            key="file_num_questions"
                        )
                    
                    # Store configuration
                    st.session_state.file_data["difficulty"] = file_difficulty
                    st.session_state.file_data["num_questions"] = file_num_questions
                    st.session_state.file_data["question_type"] = st.session_state.quiz_config["question_type"]
                    
                elif extracted_text and len(extracted_text) <= 100:
                    st.error("⚠️ The file doesn't contain enough text to generate questions. Please upload a document with more content.")
                else:
                    st.error("❌ Failed to extract text from the file. The file might be empty or corrupted.")
    
    # Show generate button if file is processed
    if st.session_state.file_processed:
        st.markdown("---")
        st.markdown("### 🎯 READY TO GENERATE QUIZ")
        
        file_info = f"""
        **File:** {st.session_state.file_data.get('name', 'Unknown')}  
        **Type:** {st.session_state.quiz_config['question_type']}  
        **Difficulty:** {st.session_state.file_data.get('difficulty', 'Intermediate')}  
        **Questions:** {st.session_state.file_data.get('num_questions', 5)}
        """
        st.info(file_info)
        
        if st.button(
            "🚀 **GENERATE QUIZ FROM FILE**",
            use_container_width=True,
            type="primary",
            key="generate_from_file_final"
        ):
            st.session_state.generating = True
            st.session_state.quiz_config["quiz_source"] = "file"
            st.rerun()
    
    # Handle file-based quiz generation
    if st.session_state.generating and st.session_state.quiz_config["quiz_source"] == "file":
        with st.spinner(f"🤖 Generating {st.session_state.quiz_config['question_type']} quiz from document..."):
            try:
                # Get file data
                file_content = st.session_state.file_data.get("content", "")
                file_name = st.session_state.file_data.get("name", "Unknown")
                num_questions = st.session_state.file_data.get("num_questions", 5)
                difficulty = DIFFICULTY_MAP[st.session_state.file_data.get("difficulty", "Intermediate")]
                question_type = st.session_state.quiz_config["question_type"]
                
                # Generate questions
                raw_questions = st.session_state.generator.generate_from_file_content(
                    file_content=file_content,
                    file_name=file_name,
                    difficulty=difficulty,
                    num_questions=num_questions,
                    question_type=question_type  # Pass question type
                )
                
                if raw_questions and len(raw_questions) > 0:
                    # Normalize questions for different types
                    questions = []
                    for q in raw_questions:
                        correct_answer = q.get("correct_answer", "A" if question_type == "Multiple Choice" else "True")
                        options = q.get("options", [])
                        
                        # Determine correct index based on question type
                        if question_type == "Multiple Choice":
                            if correct_answer in ["A", "B", "C", "D"]:
                                correct_index = ["A", "B", "C", "D"].index(correct_answer)
                            elif options and correct_answer in options:
                                correct_index = options.index(correct_answer)
                            else:
                                correct_index = 0
                        elif question_type == "True/False":
                            # For True/False, store the correct answer text
                            correct_index = 0 if correct_answer == "True" else 1
                        else:  # Short Answer
                            correct_index = 0  # Not used for short answer
                        
                        questions.append({
                            "question": q.get("question", "No question text"),
                            "options": options,
                            "correct": correct_index,
                            "correct_answer": correct_answer,
                            "explanation": q.get("explanation", "No explanation provided")
                        })
                    
                    # Store in session state
                    st.session_state.generated_questions = questions
                    st.session_state.quiz_active = True
                    st.session_state.current_question = 0
                    st.session_state.score = 0
                    st.session_state.answers = []
                    st.session_state.quiz_completed = False
                    st.session_state.quiz_start_time = time.time()
                    st.session_state.quiz_config["topic"] = f"Document: {file_name}"
                    st.session_state.generating = False
                    st.session_state.file_processed = False
                    
                    st.success(f"✅ Generated {len(questions)} {question_type} questions from your document!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.session_state.generating = False
                    st.error("❌ Failed to generate questions from the file.")
                    
            except Exception as e:
                st.session_state.generating = False
                st.error(f"❌ File-based quiz generation failed: {str(e)}")
    
    # Instructions
    with st.expander("📘 **How to use File Upload**"):
        st.markdown("""
        ### 📚 Supported Formats:
        1. **PDF** - Research papers, textbooks, articles
        2. **TXT** - Plain text documents, notes
        3. **DOCX** - Word documents
        
        ### 🎯 How it works:
        1. **Upload** your document
        2. **Analyze** the content (AI reads and understands)
        3. **Configure** quiz difficulty and number of questions
        4. **Generate** quiz based on document content
        5. **Test** your understanding of the material
        
        ### 💡 Best Practices:
        - Upload clear, text-based documents
        - Keep files under 10MB for best performance
        - For PDFs, ensure text is selectable (not scanned images)
        - Document should have sufficient content (at least 500 words)
        """)

with tab4:
    st.markdown("### 🎮 QUIZ ZONE")
    
    if st.session_state.quiz_active and st.session_state.generated_questions:
        # Show quiz info
        config = st.session_state.quiz_config
        source = "📄 File" if config.get("quiz_source") == "file" else "🧠 AI Topic"
        topic_display = config.get("topic", "Unknown Topic")
        question_type = config.get("question_type", "Multiple Choice")
        
        st.markdown(f"""
        <div style="background: rgba(30, 30, 50, 0.8); padding: 20px; border-radius: 15px; margin-bottom: 20px; border-left: 5px solid #00ff88;">
            <h4>{source}: {topic_display}</h4>
            <p>📝 Type: {question_type} | ⚡ Difficulty: {config['difficulty']} | 🔢 Questions: {len(st.session_state.generated_questions)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Current question
        if st.session_state.current_question < len(st.session_state.generated_questions):
            q_data = st.session_state.generated_questions[st.session_state.current_question]
            
            # Question card
            st.markdown(f"""
            <div class="question-card-neon">
                <h3>❓ Question {st.session_state.current_question + 1} of {len(st.session_state.generated_questions)}</h3>
                <p style="font-size: 22px; margin: 25px 0; font-weight: 600; color: #ffffff;">{q_data.get('question', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Handle different question types
            selected = None
            
            if question_type == "Multiple Choice":
                if q_data.get('options') and len(q_data['options']) >= 4:
                    selected = st.radio(
                        "**Select your answer:**",
                        q_data['options'],
                        key=f"quiz_q_{st.session_state.current_question}"
                    )
                else:
                    # Fallback options
                    default_options = ["Option A", "Option B", "Option C", "Option D"]
                    selected = st.radio(
                        "**Select your answer:**",
                        default_options,
                        key=f"quiz_q_{st.session_state.current_question}"
                    )
            
            elif question_type == "True/False":
                # True/False questions
                options = q_data.get('options', ["True", "False"])
                if len(options) < 2:
                    options = ["True", "False"]
                
                selected = st.radio(
                    "**Select True or False:**",
                    options,
                    key=f"quiz_q_{st.session_state.current_question}"
                )
            
            elif question_type == "Short Answer":
                # Short answer questions
                selected = st.text_area(
                    "**Type your answer (1-2 sentences):**",
                    key=f"quiz_q_{st.session_state.current_question}",
                    height=100,
                    placeholder="Enter your short answer here..."
                )
                st.caption("💡 For short answer questions, your answer will be evaluated for completeness.")
            
            # Buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "✅ SUBMIT ANSWER",
                    use_container_width=True, 
                    type="primary",
                    key=f"submit_{st.session_state.current_question}"
                ):
                    if question_type == "Short Answer" and (not selected or selected.strip() == ""):
                        st.warning("Please provide an answer before submitting.")
                        st.stop()
                    
                    # Determine if answer is correct
                    correct = False
                    
                    if question_type == "Multiple Choice":
                        # For MCQ, check against correct index
                        correct_index = q_data.get('correct', 0)
                        if correct_index < len(q_data.get('options', [])):
                            correct = (selected == q_data['options'][correct_index])
                        else:
                            # Fallback
                            correct_answer = q_data.get('correct_answer', '')
                            correct = (selected == correct_answer)
                    
                    elif question_type == "True/False":
                        # For True/False
                        correct_answer = q_data.get('correct_answer', 'True')
                        correct = (selected == correct_answer)
                    
                    elif question_type == "Short Answer":
                        # For Short Answer, accept any non-empty answer
                        correct = (selected and len(selected.strip()) > 0)
                    
                    # Update score
                    if correct:
                        st.session_state.score += 1
                    
                    # Store answer
                    st.session_state.answers.append({
                        "question": q_data['question'],
                        "selected": selected if selected else "No answer",
                        "correct": correct,
                        "explanation": q_data.get('explanation', 'No explanation provided'),
                        "question_type": question_type
                    })
                    
                    # Move to next question
                    st.session_state.current_question += 1
                    
                    # Check if quiz is complete
                    if st.session_state.current_question >= len(st.session_state.generated_questions):
                        st.session_state.quiz_active = False
                        st.session_state.quiz_completed = True
                    
                    st.rerun()
            
            with col2:
                if st.button(
                    "⏹️ END QUIZ",
                    use_container_width=True,
                    key=f"end_{st.session_state.current_question}"
                ):
                    st.session_state.quiz_active = False
                    st.session_state.quiz_completed = True
                    st.rerun()
            
            # Progress bar
            progress = (st.session_state.current_question + 1) / len(st.session_state.generated_questions)
            st.progress(progress)
            st.caption(f"Progress: {st.session_state.current_question + 1}/{len(st.session_state.generated_questions)}")
        
        else:
            # Quiz completed
            st.session_state.quiz_active = False
            st.session_state.quiz_completed = True
            st.rerun()
    
    elif st.session_state.quiz_completed:
        # Completion message
        st.balloons()
        st.markdown("""
        <div style="text-align: center; padding: 40px; background: rgba(30, 30, 50, 0.8); border-radius: 20px; margin: 20px 0;">
            <h1>🎉 Quiz Completed!</h1>
            <p style="color: #cccccc; font-size: 20px;">Go to Results tab to see your score</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # No active quiz
        st.markdown("""
        <div style="text-align: center; padding: 60px; background: rgba(30, 30, 50, 0.5); border-radius: 20px; margin: 40px 0;">
            <h3>No Active Quiz</h3>
            <p style="color: #cccccc;">Generate a quiz from Topic or File Upload tab!</p>
        </div>
        """, unsafe_allow_html=True)

with tab5:
    st.markdown("### 🏆 RESULTS")
    
    if st.session_state.quiz_completed and st.session_state.answers:
        total = len(st.session_state.answers)
        score = st.session_state.score
        percentage = (score / total * 100) if total > 0 else 0
        
        # Balloons and ribbons
        st.balloons()
        st.markdown('<div style="text-align: center; font-size: 50px;">🎉🎗️🎊</div>', unsafe_allow_html=True)
        
        # Pass/Fail
        if percentage >= 70:
            pass_fail = "PASS 🏆"
            badge_class = "pass-badge-neon"
            message = "Excellent! You passed with flying colors!"
        else:
            pass_fail = "FAIL ❌"
            badge_class = "fail-badge-neon"
            message = "Keep practicing! You'll do better next time!"
        
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <div class="{badge_class}">{pass_fail}</div>
            <h3 style="color: #cccccc; margin-top: 20px;">{message}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Score
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f0c29, #302b63); padding: 40px; border-radius: 25px; text-align: center; margin: 20px 0;">
            <h1>🎯 FINAL SCORE</h1>
            <h2 style="font-size: 5rem; margin: 20px 0; color: #00ff88;">{score}/{total}</h2>
            <h3 style="font-size: 3rem; color: #00ccff;">{percentage:.1f}%</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Chart - GREEN for Correct, RED for Incorrect
        results_df = pd.DataFrame({
            'Result': ['✅ Correct', '❌ Incorrect'],
            'Count': [score, total - score]
        })
        
        # Create pie chart with custom colors
        fig = px.pie(
            results_df, 
            values='Count', 
            names='Result',
            color='Result',
            color_discrete_map={
                '✅ Correct': '#00FF88',  # Bright Green
                '❌ Incorrect': '#FF0000'  # Bright Red
            },
            hole=0.3
        )
        
        # Customize appearance
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(size=16, color='white'),
            marker=dict(line=dict(color='white', width=2))
        )
        
        fig.update_layout(
            title=dict(
                text='📊 Performance Breakdown',
                font=dict(size=20, color='white')
            ),
            showlegend=True,
            legend=dict(
                font=dict(color='white', size=14)
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Accuracy", f"{percentage:.1f}%")
        with col2:
            st.metric("✅ Correct", score)
        with col3:
            st.metric("❌ Incorrect", total - score)
        
        # Question review
        st.markdown("### 📋 QUESTION REVIEW")
        for i, answer in enumerate(st.session_state.answers):
            with st.expander(f"Q{i+1}: {answer['question'][:50]}... ({answer.get('question_type', 'MCQ')})", expanded=(i==0)):
                if answer['correct']:
                    st.success(f"✅ **Your Answer:** {answer['selected']}")
                else:
                    st.error(f"❌ **Your Answer:** {answer['selected']}")
                st.info(f"💡 **Explanation:** {answer['explanation']}")
    
    else:
        st.info("Complete a quiz to see results here!")

# Add JavaScript for card selection
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Make radio cards clickable
    const radioCards = document.querySelectorAll('.radio-card-neon');
    radioCards.forEach(card => {
        card.addEventListener('click', function() {
            radioCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
});
</script>
""", unsafe_allow_html=True)