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

# ---------------- Sidebar ----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("💳 Credit Card AI")
    st.write("Your Smart Credit Card Assistant")

    st.markdown("---")

    st.subheader("Topics Covered")

    st.markdown("""
    ✅ Credit Card Features

    ✅ Rewards & Cashback

    ✅ Credit Score

    ✅ EMI

    ✅ Billing Cycle

    ✅ Interest Rate

    ✅ Card Security

    ✅ Online Payments

    ✅ Fees & Charges
    """)

    st.markdown("---")
    st.caption("Powered by Groq + Llama 3.1")

# ---------------- Main Page ----------------

st.title("💳 Credit Card AI Assistant")

st.markdown(
"""
Welcome!

This AI Assistant answers **only Credit Card related questions**.

Ask anything about:

- Credit Cards
- Rewards
- Cashback
- Credit Score
- EMI
- Billing Cycle
- Security
- Online Payments
"""
)

question = st.text_area(
    "Enter your question",
    placeholder="Example: What is minimum payment on a credit card?"
)

if st.button("🚀 Ask AI", use_container_width=True):

    if question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_template(
    """
    You are an expert Credit Card Advisor.

    Answer ONLY credit card related questions.

    Topics:
    - Eligibility
    - Benefits
    - Rewards
    - Cashback
    - Credit Score
    - Interest
    - EMI
    - Billing Cycle
    - Security
    - Statements
    - Fees
    - Online Transactions

    If the question is unrelated, reply:

    Sorry, I only answer credit card-related questions.

    Question:
    {question}

    Format your answer using:

    ## Simple Explanation

    ## Step-by-Step Guidance

    ## Best Practices

    ## Precautions (if needed)
    """
    )

    chain = prompt | llm

    with st.spinner("Generating answer..."):

        response = chain.invoke(
            {
                "question": question
            }
        )

    st.success("Answer Generated Successfully!")

    st.markdown("## 🤖 AI Response")

    st.info(response.content)

st.markdown("---")
st.caption("© 2026 Credit Card AI Assistant | Built with Streamlit + LangChain + Groq")
