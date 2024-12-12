import os
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import (
    load_gemini_pro_model,
    gemini_pro_response,
    gemini_pro_vision_response,
    embeddings_model_response,
)

# Get the working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Streamlit page configuration
st.set_page_config(
    page_title="Bujji AI",
    page_icon="🧠",
    layout="centered",
)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Bujji AI",
        ["ChatBot", "Embed text", "Ask me anything"],
        menu_icon="robot",
        icons=["chat-dots-fill", "textarea-t", "patch-question-fill"],
        default_index=0,
    )

# Function to translate roles for Streamlit chat UI
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role


# Chatbot page
if selected == "ChatBot":
    model = load_gemini_pro_model()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Page title
    st.title("🤖 Bujji")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # User input for chatbot
    user_prompt = st.chat_input("Ask Bujji...")
    if user_prompt:
        # Add user message to chat
        st.chat_message("user").markdown(user_prompt)

        # Send user input to Gemini-Pro model and get response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display assistant's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# Embed Text page
if selected == "Embed text":
    st.title("🔡 Embed Text")

    # User input for text embedding
    user_prompt = st.text_area(label="", placeholder="Enter the text to get embeddings")
    if st.button("Get Embeddings"):
        if user_prompt.strip():
            response = embeddings_model_response(user_prompt)
            st.markdown(response)
        else:
            st.warning("Please enter some text to get embeddings.")

# Ask Me Anything page
if selected == "Ask me anything":
    st.title("❓ Ask me a question")

    # User input for general query
    user_prompt = st.text_area(label="", placeholder="Ask me anything...")
    if st.button("Get Response"):
        if user_prompt.strip():
            response = gemini_pro_response(user_prompt)
            st.markdown(response)
        else:
            st.warning("Please enter a question to get a response.")
          
