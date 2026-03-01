# streamlit_app.py
import streamlit as st
from app import create_rag_pipeline, ask_question

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="📄 PDF RAG Chatbot", layout="wide")
st.title("📄 PDF RAG Chatbot")

# ----------------------------
# Load backend once
# ----------------------------
@st.cache_resource
def load_backend():
    return create_rag_pipeline()

retriever, llm = load_backend()

# ----------------------------
# Initialize chat history
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# User input box
# ----------------------------
query = st.text_input("Ask a question about the PDF:")

if query:
    answer = ask_question(query, retriever, llm)
    st.session_state.chat_history.append({"user": query, "bot": answer})

# ----------------------------
# Display chat history
# ----------------------------
st.subheader("Chat History:")
chat_container = st.container()

with chat_container:
    for chat in st.session_state.chat_history:
        # User bubble (green, right)
        st.markdown(
            f"""
            <div style="
                text-align: right; 
                background-color: #DCF8C6; 
                padding: 10px; 
                border-radius: 10px; 
                margin: 5px 0;
                max-width: 70%;
                float: right;
            ">
                <b>You:</b> {chat['user']}
            </div>
            """,
            unsafe_allow_html=True
        )
        # Bot bubble (gray, left)
        st.markdown(
            f"""
            <div style="
                text-align: left; 
                background-color: #F1F0F0; 
                padding: 10px; 
                border-radius: 10px; 
                margin: 5px 0;
                max-width: 70%;
                float: left;
            ">
                <b>Bot:</b> {chat['bot']}
            </div>
            """,
            unsafe_allow_html=True
        )

# ----------------------------
# Optional: Scrollable chat container
# ----------------------------
st.markdown(
    """
    <style>
    .css-1aumxhk {
        max-height: 500px;
        overflow-y: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Clear chat button
# ----------------------------
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_history = []