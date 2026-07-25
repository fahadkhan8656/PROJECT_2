import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Credit Card AI Advisor",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    /* Main Background & Clean Font Styling */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Header Card */
    .header-card {
        background: linear-gradient(135deg, #0E4D92 0%, #002244 100%);
        padding: 1.8rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(14, 77, 146, 0.2);
    }
    
    .header-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-subtitle {
        color: #cbd5e1;
        font-size: 0.95rem;
        margin-top: 6px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Topic Tag Badges */
    .topic-chip {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 3px 2px;
    }

    /* Chat Bubble Tweaks */
    .stChatMessage {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px !important;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    /* Reduce vertical padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 💳 Credit Card AI")
    st.caption("Your Personal Financial Assistant")
    
    st.divider()

    st.markdown("#### 🟢 Model Status")
    st.caption("Powered by **Groq • Llama 3.1 8B**")

    st.divider()

    st.markdown("#### 📚 Covered Topics")
    topics = [
        "Credit Score", "Rewards & Cashback", "EMI", 
        "Billing Cycle", "Interest Rates", "Minimum Payment", 
        "Security", "Fees & Charges", "Online Safety"
    ]
    
    # Render topics as clean visual tags
    topic_html = "".join([f'<span class="topic-chip">{t}</span>' for t in topics])
    st.markdown(f"<div>{topic_html}</div>", unsafe_allow_html=True)

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("© 2026 Credit Card AI • Built with Streamlit & LangChain")

# ---------------- MAIN HEADER ----------------
st.markdown("""
<div class="header-card">
    <div class="header-title">💳 Credit Card AI Advisor</div>
    <div class="header-subtitle">Get instant, simplified answers about credit scores, cashback, EMI, fees, and smart card management.</div>
</div>
""", unsafe_allow_html=True)

# ---------------- CHAT SESSION SETUP ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick Start Suggestion Handler
if "active_question" not in st.session_state:
    st.session_state.active_question = None

# Show Welcome & Quick Prompts ONLY when conversation hasn't started
if len(st.session_state.messages) == 0:
    st.markdown("#### 💡 Quick Questions to Ask")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📈 How do I increase my Credit Score?", use_container_width=True):
            st.session_state.active_question = "How do I increase my Credit Score?"
        if st.button("⚖️ How does Credit Card EMI work?", use_container_width=True):
            st.session_state.active_question = "How does Credit Card EMI work?"

    with col2:
        if st.button("⚠️ What happens if I pay only the Minimum Balance?", use_container_width=True):
            st.session_state.active_question = "What happens if I pay only the Minimum Balance?"
        if st.button("🎁 How do credit card cashback rewards work?", use_container_width=True):
            st.session_state.active_question = "How do credit card cashback rewards work?"

    st.divider()

# ---------------- CHAT HISTORY RENDER ----------------
for message in st.session_state.messages:
    avatar = "💳" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------- USER INPUT & RESPONSE LOGIC ----------------
prompt_input = st.chat_input("Ask any question about credit cards...")

# Determine if input comes from text box or quick prompt button
question = prompt_input or st.session_state.active_question

if question:
    # Reset prompt trigger state
    st.session_state.active_question = None

    # Append & Display User Message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    # Setup LangChain Chain
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

    # Assistant Streaming Response
    with st.chat_message("assistant", avatar="💳"):
        # Stream response chunk by chunk for dynamic effect
        def stream_generator():
            for chunk in chain.stream({"question": question}):
                yield chunk.content

        full_response = st.write_stream(stream_generator())

    # Store assistant response in session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # Rerun to sync UI cleanly
    st.rerun()
