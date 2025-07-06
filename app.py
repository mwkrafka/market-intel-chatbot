from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import os

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit UI setup
st.set_page_config(page_title="Market Intelligence Chatbot", page_icon="📈")
st.title("📊 Market Intelligence Chatbot")

# Sidebar: Prompt Templates
st.sidebar.header("Prompt Templates")
templates = {
    "— Select a template —": "",
    "📈 Market Movers": "Summarize today’s top market movers and explain why they moved.",
    "💡 Interest Rate Impact": "How are rising interest rates affecting tech stocks this quarter?",
    "📊 Sector Comparison": "Compare the performance of the S&P 500 and Nasdaq in Q3 2025.",
    "🧠 Economic Outlook": "What are the key macroeconomic risks for the U.S. economy in Q3 2025?",
}
selected_template = st.sidebar.selectbox("Choose a prompt", list(templates.keys()))
default_prompt = templates[selected_template]

# Sidebar: Model + Creativity
model = st.sidebar.selectbox("Model", ["gpt-3.5-turbo"])
temperature = st.sidebar.slider("Creativity", 0.0, 1.0, 0.5)

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.text_area("Ask a market question:", value=default_prompt, height=100)

# Prompt builder
def build_prompt(user_query):
    return [
        {"role": "system", "content": "You are a financial analyst chatbot that provides concise, data-driven insights."},
        {"role": "user", "content": user_query}
    ]

# Generate response
if st.button("Analyze"):
    if user_input.strip():
        with st.spinner("Analyzing..."):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=build_prompt(user_input),
                    temperature=temperature
                )
                answer = response.choices[0].message.content
                st.session_state.chat_history.append((user_input, answer))
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question or select a template.")

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 💬 Chat History")
    for i, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**Q{i}:** {q}")
        st.markdown(f"**A{i}:** {a}")
        st.markdown("---")

# Clear history
if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.chat_history = []
