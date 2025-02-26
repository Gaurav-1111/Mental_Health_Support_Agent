import streamlit as st
import base64
import os
from langchain_groq import ChatGroq

st.set_page_config(page_title="Mental Health Chatbot", layout="wide")

def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64("background.png")

st.markdown(f"""
    <style>
        .main {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
    </style>
    """, unsafe_allow_html=True)

st.session_state.setdefault('conversation_history', [])


llm = ChatGroq(
    model_name="gemma2-9b-it",  
    temperature=0.7,
    groq_api_key="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" 
)

def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})
    
    try:
        response = llm.invoke(user_input)  # Groq API Call
        ai_response = response.content
    except Exception as e:
        ai_response = "Sorry, I couldn't process your request. Please try again later."
    
    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    response = llm.invoke(prompt)
    return response.content

def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    response = llm.invoke(prompt)
    return response.content

st.title("Mental Health Support Agent")

for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")


user_message = st.text_input("How can I help you today?")

if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

col1, col2 = st.columns(2)

with col1:
    if st.button("Give me a positive Affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Give me a guided meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")
