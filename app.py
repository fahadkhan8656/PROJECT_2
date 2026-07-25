# Credit Card AI Advisor
# app.py

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

@st.cache_resource
def load_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3
    )

llm = load_llm()

st.set_page_config(
    page_title="Credit Card AI Advisor",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(""" <style> @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap'); html, body, [class*="css"]{ font-family:'Plus Jakarta Sans',sans-serif; } .stApp{ background:#0f172a; color:#f8fafc; } #MainMenu{visibility:hidden;} footer{visibility:hidden;} .hero-card{ background:linear-gradient(135deg,#1e293b,#0f172a); padding:2rem; border-radius:18px; border:1px solid #334155; margin-bottom:2rem; } .hero-title{ font-size:2.2rem; font-weight:700; } .hero-subtitle{ color:#94a3b8; margin-top:10px; } .topic-chip{ display:inline-block; padding:6px 10px; margin:4px; border-radius:8px; background:#334155; color:white; font-size:.8rem; } .stChatMessage{ border-radius:14px; } </style> """, unsafe_allow_html=True)

with st.sidebar:
    st.title("💳 Credit Card AI")
    st.caption("Smart Financial Copilot")

    st.subheader("Topics")
    topics=[
        "Credit Score","Rewards","Cashback","EMI",
        "Billing Cycle","Interest","Security",
        "Fees","Statements"
    ]
    st.markdown("".join([f"<span class='topic-chip'>{t}</span>" for t in topics]), unsafe_allow_html=True)

    if st.button("🗑️ Clear Session", use_container_width=True):
        st.session_state.messages=[]
        st.rerun()

st.markdown(""" <div class="hero-card"> <div class="hero-title">💳 Credit Card AI Advisor</div> <div class="hero-subtitle"> Ask anything about credit cards, rewards, EMI, credit score, billing cycles and security. </div> </div> """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    avatar="👤" if message["role"]=="user" else "💳"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if not st.session_state.messages:
    st.subheader("💡 Quick Prompts")
    c1,c2=st.columns(2)

    quick=None
    with c1:
        if st.button("📈 Improve Credit Score"):
            quick="How do I improve my credit score?"
        if st.button("💳 Credit Card EMI"):
            quick="How does Credit Card EMI work?"
    with c2:
        if st.button("⚠️ Minimum Payment"):
            quick="What happens if I pay only the minimum due?"
        if st.button("🎁 Cashback"):
            quick="How can I maximize cashback and reward points?"

else:
    quick=None

typed=st.chat_input("Ask a credit card question...")
question=typed or quick

if question:
    st.session_state.messages.append(
        {"role":"user","content":question}
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    prompt=ChatPromptTemplate.from_template(""" You are an expert Credit Card AI Advisor. Rules: - Answer only credit card related questions. - If unrelated, reply exactly: Sorry, I only answer credit card-related questions. - Keep answers beginner friendly. Question: {question} Format: ## 📘 Simple Explanation ## 📌 Step-by-Step Guidance ## ✅ Best Practices ## ⚠️ Precautions """)

    chain=prompt|llm

    try:
        with st.chat_message("assistant", avatar="💳"):

            def stream():
                for chunk in chain.stream({"question":question}):
                    if chunk.content:
                        yield chunk.content

            response=st.write_stream(stream())

    except Exception as e:
        response=f"❌ Error: {e}"
        st.error(response)

    st.session_state.messages.append(
        {"role":"assistant","content":response}
    )
