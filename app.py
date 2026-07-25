import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Credit Card Information Chatbot Using AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    /* Global Imports & Base Theme */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Hide Default Header/Footer elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Modern Hero Header */
    .hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        padding: 2.2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, rgba(0,0,0,0) 70%);
        pointer-events: none;
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 8px;
        max-width: 650px;
        line-height: 1.5;
    }

    .badge-status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: #34d399;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 9999px;
        margin-top: 12px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }

    /* Topic Tag Badges */
    .topic-chip {
        display: inline-block;
        background-color: #334155;
        color: #e2e8f0;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 4px 3px;
        border: 1px solid #475569;
        transition: all 0.2s ease;
    }
    
    .topic-chip:hover {
        border-color: #3b82f6;
        color: #60a5fa;
    }

    /* Chat Messages */
    .stChatMessage {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* User Message Highlight */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #0f172a !important;
        border-color: #3b82f6 !important;
    }

    /* Streamlit Buttons Style */
    .stButton > button {
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        background: #1e293b !important;
        color: #cbd5e1 !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        padding: 0.6rem 1rem !important;
    }

    .stButton > button:hover {
        border-color: #3b82f6 !important;
        color: #ffffff !important;
        background: #2563eb !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }

    /* Chat Input Bar */
    .stChatInputContainer {
        border-radius: 16px !important;
        border-color: #334155 !important;
    }

    /* Reduce vertical padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 💳 Credit Card AI")
    st.caption("Smart Financial Copilot")
    
    st.divider()

    st.markdown("#### ⚡ Engine")
    st.markdown("""
        <div class="badge-status">
            <span>●</span> Groq • Llama 3.1 8B
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("#### 📚 Covered Topics")
    topics = [
        "Credit Score", "Rewards & Cashback", "EMI", 
        "Billing Cycle", "Interest Rates", "Minimum Payment", 
        "Security", "Fees & Charges", "Online Safety"
    ]
    
    topic_html = "".join([f'<span class="topic-chip">{t}</span>' for t in topics])
    st.markdown(f"<div>{topic_html}</div>", unsafe_allow_html=True)

    st.divider()

    if st.button("🗑️ Clear Session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.active_question = None
        st.rerun()

    st.caption("© 2026 Credit Card AI • Streamlit & LangChain")

# ---------------- HERO HEADER ----------------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">💳 Credit Card Information Chatbot Using AI</div>
    <div class="hero-subtitle">Ask anything about credit scores, cashback tricks, EMI math, fees, and smart habits. Get direct, simple, expert answers.</div>
</div>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE SETUP ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_question" not in st.session_state:
    st.session_state.active_question = None

# ---------------- STARTER SUGGESTIONS ----------------
if len(st.session_state.messages) == 0:
    st.markdown("#### 💡 Quick Prompts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📈 How do I increase my Credit Score quickly?", use_container_width=True):
            st.session_state.active_question = "How do I increase my Credit Score quickly?"
        if st.button("⚖️ How does Credit Card EMI actually work?", use_container_width=True):
            st.session_state.active_question = "How does Credit Card EMI actually work?"

    with col2:
        if st.button("⚠️ What happens if I only pay the Minimum Balance?", use_container_width=True):
            st.session_state.active_question = "What happens if I only pay the Minimum Balance?"
        if st.button("🎁 How can I maximize cashback and reward points?", use_container_width=True):
            st.session_state.active_question = "How can I maximize cashback and reward points?"

    st.markdown("---")

# ---------------- CHAT HISTORY RENDER ----------------
for message in st.session_state.messages:
    avatar = "💳" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------- USER INPUT & LLM PIPELINE ----------------
prompt_input = st.chat_input("Ask any question about credit cards...")

# Determine if input came from typed box or quick-action button
question = prompt_input or st.session_state.active_question

if question:
    # Clear the quick question trigger state
    st.session_state.active_question = None

    # Render User Message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    # LangChain Pipeline Setup
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_template(
"""
You are a Professional Credit Card Advisor.

Answer ONLY Credit Card related questions.

Topics include:
- Credit Card Features
- Eligibility
- Rewards & Cashback
- Credit Limit & Score
- Interest Rate & Billing Cycle
- Minimum Payment & EMI
- Security & Online Transactions
- Statements, Fees & Charges

If the question is outside credit cards reply exactly:
Sorry, I only answer credit card-related questions.

Question:
{question}

Answer using this clean format:

# 📘 Simple Explanation

# 📌 Step-by-Step Guidance

# ✅ Best Practices

# ⚠️ Precautions (if needed)

Keep the answer simple and beginner friendly.
"""
    )

    chain = prompt | llm

    # Render Assistant Message Stream
    with st.chat_message("assistant", avatar="💳"):
        def stream_generator():
            for chunk in chain.stream({"question": question}):
                yield chunk.content

        full_response = st.write_stream(stream_generator())

    # Store assistant response and trigger sync rerun
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()
