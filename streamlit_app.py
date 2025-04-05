import streamlit as st
import openai

# Initialize OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set app title
st.title("Wellness Symptom Guide")

# Guardrail / System instruction to set chatbot boundaries
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a helpful wellness assistant. "
        "You can provide general health and wellness suggestions like home remedies, hydration tips, or lifestyle advice. "
        "Do not provide a diagnosis, prescription, or emergency advice. "
        "Always recommend the user consult a medical professional for any serious symptoms."
    )
}

# Initialize chat history with the system message
if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_PROMPT]

# Display previous messages (excluding system)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Function to get response from OpenAI
def get_response(prompt):
    messages = st.session_state.messages + [{"role": "user", "content": prompt}]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message["content"]

# Input box
user_input = st.chat_input("Describe your symptoms here...")

# Handle input and response
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    assistant_response = get_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

# Optional disclaimer below chat
st.caption("⚠️ This assistant provides general wellness tips and does not replace professional medical advice.")
