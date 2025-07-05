import streamlit as st
import openai
import os

# Set your OpenAI API key (use a .env file or environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Market Intelligence Chatbot", page_icon="📈")
st.title("📊 Market Intelligence Chatbot")

# User input
user_input = st.text_input("Ask a question about the market:")

# Generate response
if user_input:
    with st.spinner("Analyzing..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a financial analyst chatbot."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response['choices'][0]['message']['content'])
        except Exception as e:
            st.error(f"Error: {e}")

