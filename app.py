import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.set_page_config(
    page_title="Credit Card Assistant",
    page_icon="💳"
)

st.title("Credit Card AI Assistant")
st.write("This is an AI Credit Card Assistant, this bot will be useful")

st.write("Ask anything related to credit cards")

question = st.text_area(
    "Enter Your Credit Card Question"
)

if st.button("Ask AI"):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3

    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are a Credit Card Expert.
        Your job is to answer ONLY credit card-related questions.

        Topics include:
        - Credit Card Features
        - Credit Card Eligibility
        - Credit Card Benefits
        - Rewards & Cashback
        - Credit Limit
        - Interest Rates
        - Billing Cycle
        - Minimum Payment
        - EMI on Credit Cards
        - Credit Score
        - Fees & Charges
        - Safe Credit Card Usage
        - Card Security
        - Online Transactions
        - Credit Card Statements

        If the user asks anything outside credit cards,
        reply:

        "Sorry, I only answer credit card-related questions."

        Question:
        {question}

        Provide:
        1. Simple Explanation
        2. Step-by-step guidance
        3. Best Practices
        4. Precautions if needed
        """
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "question": question
        }
    )

    st.success(response.content)