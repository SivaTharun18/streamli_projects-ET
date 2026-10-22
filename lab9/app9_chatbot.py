import streamlit as st
import time
from google import genai

st.set_page_config(page_title="Gemini AI Chatbot", page_icon="💬")

st.title("Gemini AI Chatbot")
st.write("Chat with Gemini AI!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)

        # Prepare conversation history for Gemini
        history = []

        for msg in st.session_state.messages:
            history.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [{"text": msg["content"]}]
            })

        with st.chat_message("assistant"):
            with st.spinner("Gemini is typing..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=history
                )

                reply = response.text

            st.write(reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

    except Exception as e:
        st.error(f"Gemini API Error: {e}")

# Download chat history
if st.session_state.messages:
    chat_text = "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in st.session_state.messages
    )

    st.download_button(
        label="Download Chat History",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )

# Clear chat
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()