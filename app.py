
import streamlit as st
import os
import time
import re
from google import genai

# =============== PAGE CONFIG ===============

st.set_page_config(
    page_title="Interview Mock Test",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============== SESSION STATE ===============

defaults = {
    "question": None,
    "feedback": None,
    "role": None,
    "page": "Dashboard",
    "theme": "Light",
    "interview_type": "Technical",
    "attempts": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =============== GEMINI CONNECTION ===============

@st.cache_resource
def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        raise ValueError("Gemini API key not found!")

    return genai.Client(api_key=api_key)




MODEL_CANDIDATES = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite"
]


# =============== QUESTION GENERATION ===============
def open_start_test():
    st.session_state.page = "Start Test"
def generate_question(role, difficulty, interview_type):

    prompt = f"""
    You are a professional interview expert.

    Generate ONE interview question.

    Job Role: {role}
    Difficulty: {difficulty}
    Interview Type: {interview_type}

    Also provide:
    1. Skills being tested
    2. One short hint
    """

    client = get_client()

    for model in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text

        except Exception as e:
            print(f"{model} failed: {str(e)[:150]}")
            time.sleep(2)

    raise Exception("All Gemini models are currently unavailable.")


# =============== ANSWER EVALUATION ===============

def evaluate_answer(question, answer, role):

    prompt = f"""
    You are an expert interview evaluator.

    Job Role: {role}

    Interview Question:
    {question}

    Candidate Answer:
    {answer}

    Evaluate fairly.

    Give the result in this format:

    1. SCORE OUT OF 10
    2. ANSWER QUALITY
    3. STRENGTHS
    4. MISTAKES AND MISSING POINTS
    5. IMPROVEMENT SUGGESTIONS
    6. BETTER SAMPLE ANSWER

    Be professional, constructive and accurate.
    Do not give high marks without justification.
    """
    client = get_client()
    for model in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text

        except Exception as e:
            print(f"{model} failed: {str(e)[:150]}")
            time.sleep(2)

    raise Exception("All Gemini models are currently unavailable.")


# =============== THEME COLORS ===============

if st.session_state.theme == "Light":
    BG = "#F4F6FC"
    CARD = "#FFFFFF"
    TEXT = "#17213D"
    MUTED = "#71809B"
    BORDER = "#E3E9F5"
    PRIMARY = "#2155E8"
    SOFT = "#EDF2FF"
else:
    BG = "#10182B"
    CARD = "#1A2740"
    TEXT = "#F2F5FF"
    MUTED = "#A9B6D0"
    BORDER = "#30405D"
    PRIMARY = "#527DFF"
    SOFT = "#243452"


# =============== SIDEBAR ===============

with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🎙️</div>
        <div class="brand-name">Interview<br>Mock Test</div>
        <div class="brand-caption">AI Interview Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-label">MAIN MENU</div>',
                unsafe_allow_html=True)

    st.radio(
        "Navigation",
        [
            "Dashboard",
            "Start Test",
            "Past Attempts",
            "Performance",
            "Settings"
        ],
        key="page",
        label_visibility="collapsed"
    )

    st.markdown('<div class="sidebar-bottom">', unsafe_allow_html=True)

    st.markdown("**AI ENGINE**")
    st.success("Gemini Connected")
    st.caption("Interview Mock Test v1.0")

    st.markdown('</div>', unsafe_allow_html=True)


# =============== CUSTOM DESIGN ===============

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: Inter, sans-serif;
}}

.stApp,
[data-testid="stAppViewContainer"] {{
    background: {BG};
    color: {TEXT};
}}

[data-testid="stHeader"] {{
    background: {BG};
}}

.block-container {{
    max-width: 1450px;
    padding: 1.8rem 2rem 3rem 2rem;
}}

section[data-testid="stSidebar"] {{
    background: #142344;
    min-width: 235px;
    border-right: none;
}}

section[data-testid="stSidebar"] * {{
    color: #F3F6FF;
}}

section[data-testid="stSidebar"] [data-testid="stRadio"] label {{
    background: transparent;
    border-radius: 9px;
    padding: 9px 10px;
}}

section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{
    background: #233D72;
}}

.brand {{
    padding: 22px 5px 30px 5px;
    text-align: center;
}}

.brand-icon {{
    font-size: 38px;
    background: #254B99;
    width: 65px;
    height: 65px;
    border-radius: 50%;
    margin: auto auto 14px auto;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.brand-name {{
    font-size: 21px;
    line-height: 1.25;
    font-weight: 800;
}}

.brand-caption {{
    font-size: 11px;
    color: #AFC2E8;
    margin-top: 9px;
}}

.nav-label {{
    color: #91A8D2;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin: 10px 0 12px 5px;
}}

.sidebar-bottom {{
    margin-top: 35px;
    padding: 15px 5px;
}}

h1, h2, h3, h4, p, label {{
    color: {TEXT};
}}

.stMarkdown p {{
    color: {TEXT};
}}

.stCaption, [data-testid="stCaptionContainer"] {{
    color: {MUTED} !important;
}}

.dashboard-banner {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    padding: 25px 30px;
    border: 1px solid #DCE5FF;
    border-radius: 15px;
    background: linear-gradient(110deg, #DDE8FF, #F2F5FF);
    color: #17213D;
    margin-bottom: 22px;
    min-height: 145px;
}}

.banner-title {{
    font-size: 27px;
    font-weight: 800;
    color: #17213D;
}}

.banner-sub {{
    font-size: 13px;
    color: #526484;
    margin-top: 8px;
}}

.banner-art {{
    font-size: 65px;
    padding: 5px 20px;
}}

.section-heading {{
    font-size: 19px;
    font-weight: 800;
    color: {TEXT};
    margin: 8px 0 15px 0;
}}

.app-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 18px;
    min-height: 150px;
}}

.app-card h3 {{
    font-size: 17px;
    margin: 0 0 10px 0;
}}

.app-card p {{
    font-size: 13px;
    color: {MUTED};
}}

.big-icon {{
    font-size: 36px;
    margin-bottom: 8px;
}}

.category {{
    text-align: center;
    background: {SOFT};
    border: 1px solid {BORDER};
    border-radius: 11px;
    padding: 13px 5px;
    min-height: 95px;
}}

.category-icon {{
    font-size: 26px;
}}

.category-name {{
    font-size: 12px;
    font-weight: 700;
    color: {TEXT};
    margin-top: 8px;
}}

.stButton > button,
.stFormSubmitButton > button {{
    background: {PRIMARY};
    color: white;
    border: none;
    border-radius: 9px;
    min-height: 43px;
    font-weight: 700;
}}

.stButton > button:hover,
.stFormSubmitButton > button:hover {{
    background: #1745C7;
    color: white;
    border: none;
}}

.stTextArea textarea {{
    background: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}

[data-testid="stForm"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 20px;
}}

[data-testid="stMetric"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 15px;
}}

hr {{
    border-color: {BORDER};
}}

footer {{
    visibility: hidden;
}}

@media(max-width: 768px) {{
    .block-container {{
        padding: 1rem;
    }}
    .dashboard-banner {{
        padding: 18px;
    }}
    .banner-title {{
        font-size: 21px;
    }}
    .banner-art {{
        font-size: 40px;
    }}
}}

</style>
""", unsafe_allow_html=True)


# =============== TOP HEADER ===============

top1, top2 = st.columns([5, 1])

with top1:
    st.caption("INTERVIEW MOCK TEST / YOUR WORKSPACE")

with top2:
    st.markdown(
        f"<div style='text-align:right;color:{MUTED};font-size:13px'>"
        f"● Online</div>",
        unsafe_allow_html=True
    )


# =============== DASHBOARD ===============

if st.session_state.page == "Dashboard":

    st.markdown("""
    <div class="dashboard-banner">
        <div>
            <div class="banner-title">Welcome to Interview Pro! 👋</div>
            <div class="banner-sub">
                Sharpen your interview skills with AI-powered mock interviews.
            </div>
        </div>
        <div class="banner-art">🎯</div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown('<div class="section-heading">Start a Mock Interview</div>',
                    unsafe_allow_html=True)

        st.markdown("""
        <div class="app-card">
            <div class="big-icon">💻 👨‍💼</div>
            <h3>Practice with AI</h3>
            <p>Answer real interview-style questions and receive
            instant feedback from Gemini AI.</p>
        </div>
        """, unsafe_allow_html=True)

       st.button(
    "Begin Test  →",
    use_container_width=True,
    on_click=open_start_test
)

    with right:
        st.markdown('<div class="section-heading">Your Progress</div>',
                    unsafe_allow_html=True)

        if st.session_state.attempts:
            st.metric("Tests Attempted", st.session_state.attempts)
            st.success("Your interview practice is underway.")
        else:
            st.markdown("""
            <div class="app-card">
                <div class="big-icon">📈</div>
                <h3>Your progress starts here</h3>
                <p>No completed attempts yet. Complete your first
                interview to begin tracking progress.</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Recent Attempts</div>',
                unsafe_allow_html=True)

    if st.session_state.feedback:
        st.markdown(f"""
        <div class="app-card">
            <h3>Latest Interview</h3>
            <p>Role: {st.session_state.role}</p>
            <p>AI evaluation completed in this session.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="app-card">
            <p>No interview attempts yet.</p>
            <p style="color:{MUTED}">
            Your completed sessions will appear here in a future update.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Popular Categories</div>',
                unsafe_allow_html=True)

    categories = st.columns(4)

    category_data = [
        ("💻", "Technical"),
        ("👥", "HR"),
        ("💼", "Mixed"),
        ("✨", "More")
    ]

    for col, (emoji, name) in zip(categories, category_data):
        with col:
            st.markdown(f"""
            <div class="category">
                <div class="category-icon">{emoji}</div>
                <div class="category-name">{name}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    if st.button("Practice a Category  →", use_container_width=True):
        st.session_state.page = "Start Test"
        st.rerun()


# =============== START TEST ===============

elif st.session_state.page == "Start Test":

    st.markdown("""
    <div class="dashboard-banner">
        <div>
            <div class="banner-title">Start Your Interview 🚀</div>
            <div class="banner-sub">
                Configure your interview and meet your AI interviewer.
            </div>
        </div>
        <div class="banner-art">🎙️</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Interview Setup</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        role = st.selectbox(
            "Select Job Role",
            [
                "Python Developer",
                "Web Developer",
                "Data Analyst",
                "AI Engineer",
                "Software Engineer"
            ]
        )

        difficulty = st.selectbox(
            "Select Difficulty",
            ["Beginner", "Intermediate", "Advanced"]
        )

    with col2:
        interview_type = st.selectbox(
            "Interview Category",
            ["Technical", "HR", "Mixed"],
            key="interview_type"
        )

        st.info("Choose the settings for your practice session.")

    if st.button("Generate Interview Question  →",
                 use_container_width=True):

        with st.spinner("Gemini is preparing your question..."):

            try:
                question = generate_question(
                    role, difficulty, interview_type
                )

                st.session_state.question = question
                st.session_state.role = role
                st.session_state.feedback = None
                st.session_state.pop("answer_text", None)

            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.question:

        st.divider()
        st.markdown('<div class="section-heading">Your Question</div>',
                    unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(st.session_state.question)

        st.markdown('<div class="section-heading">Your Answer</div>',
                    unsafe_allow_html=True)

        with st.form("answer_form"):

            answer = st.text_area(
                "Write your answer",
                height=180,
                placeholder="Type your answer here...",
                key="answer_text"
            )

            submit = st.form_submit_button(
                "Submit Answer for Evaluation",
                use_container_width=True
            )

        if submit:

            if not answer.strip():
                st.warning("Please write your answer first.")

            else:
                with st.spinner("Gemini is evaluating your answer..."):

                    try:
                        feedback = evaluate_answer(
                            st.session_state.question,
                            answer,
                            st.session_state.role
                        )

                        st.session_state.feedback = feedback
                        st.session_state.attempts += 1

                    except Exception as e:
                        st.error(f"Evaluation Error: {e}")

    if st.session_state.feedback:
        st.divider()
        st.markdown('<div class="section-heading">AI Evaluation Report</div>',
                    unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(st.session_state.feedback)


# =============== PAST ATTEMPTS ===============

elif st.session_state.page == "Past Attempts":

    st.title("Past Attempts")
    st.info(
        "Interview history will be added in a future update. "
        "Currently, sessions are not permanently stored."
    )


# =============== PERFORMANCE ===============

elif st.session_state.page == "Performance":

    st.title("Performance")
    st.info(
        "Performance charts, average scores and progress tracking "
        "will be added in a future update."
    )


# =============== SETTINGS ===============

elif st.session_state.page == "Settings":

    st.title("Settings")
    st.subheader("Appearance")

    st.radio(
        "Select App Theme",
        ["Light", "Dark"],
        key="theme",
        horizontal=True
    )

    st.caption("Your selected theme will apply to the interface.")


# =============== FOOTER ===============

st.divider()
st.caption("Interview Mock Test | Powered by Google Gemini AI")
