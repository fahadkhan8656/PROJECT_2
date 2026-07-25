import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.set_page_config(
    page_title="Credit Card AI Assistant",
    page_icon="💳",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

.stChatMessage{
    border-radius:15px;
}

h1{
    color:#0E4D92;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("💳 Credit Card AI")

    st.write("Your Personal Credit Card Expert")

    st.divider()

    st.subheader("📚 Topics")

    st.write("""
✅ Credit Card Features

✅ Rewards & Cashback

✅ Credit Score

✅ EMI

✅ Billing Cycle

✅ Interest Rate

✅ Minimum Payment

✅ Security

✅ Online Transactions

✅ Fees & Charges
""")

    st.divider()

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Powered by Groq + Llama 3.1")

# ---------------- TITLE ----------------

st.title("💳 Credit Card AI Assistant")

st.write(
"""
Welcome!

Ask anything related to **Credit Cards**.

Examples:

• What is Credit Score?

• What is Minimum Payment?

• How does EMI work?

• Which card gives best cashback?

"""
)

# ---------------- CHAT HISTORY ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- USER INPUT ----------------

question = st.chat_input("Ask your Credit Card Question...")

if question:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

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

- Rewards

- Cashback

- Credit Limit

- Interest Rate

- Billing Cycle

- Minimum Payment

- EMI

- Credit Score

- Security

- Online Transactions

- Statements

- Fees & Charges

If the question is outside credit cards reply exactly:

Sorry, I only answer credit card-related questions.

Question:

{question}

Answer using this format:

# 📘 Simple Explanation

# 📌 Step-by-Step Guidance

# ✅ Best Practices

# ⚠ Precautions (if needed)

Keep the answer simple and beginner friendly.
"""
    )

    chain = prompt | llm

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = chain.invoke(
                {
                    "question":question
                }
            )

            st.markdown(response.content)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response.content
        }
    )

st.divider()

st.caption("© 2026 Credit Card AI Assistant | Built with Streamlit • LangChain • Groq")
