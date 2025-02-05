import streamlit as st
import requests

st.title("Chat with Mentor")

if 'context' not in st.session_state:
    st.session_state['context'] = ''

def send_message():
    user_input = st.session_state['user_input']
    if user_input:
        response = requests.post('http://localhost:5000/chat', json={'question': user_input, 'context': st.session_state['context']})
        data = response.json()
        st.session_state['context'] = data['context']
        st.session_state['chat_history'].append(f"You: {user_input}")
        st.session_state['chat_history'].append(f"Mentor: {data['response']}")
        st.session_state['user_input'] = ''

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

st.text_area("Chat History", value="\n".join(st.session_state['chat_history']), height=400, disabled=True)
st.text_input("Your message", key='user_input', on_change=send_message)