import streamlit as st
import requests

# Initialize session state for conversation history and authentication
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Function to handle sign-in
def sign_in(username, password):
    if username == "user" and password == "password":
        st.session_state.authenticated = True
        st.success("Signed in successfully!")
    else:
        st.error("Invalid username or password")

# Function to handle sign-out
def sign_out():
    st.session_state.authenticated = False
    st.success("Signed out successfully!")

# Function to send user input to the Flask backend
def send_to_backend(user_input):
    url = "http://localhost:5000/chat"  # Flask backend URL
    data = {
        "question": user_input,
        "context": "\n".join(st.session_state.conversation_history)
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to get a response from the backend.")
        return None

# Sidebar for authentication
with st.sidebar:
    st.title("Authentication")
    if st.session_state.authenticated:
        st.write("You are signed in.")
        if st.button("Sign Out"):
            sign_out()
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign In"):
            sign_in(username, password)

# Main conversation interface
st.title("MMentor")

# Display the conversation in a chat-like format
st.subheader("Conversation")
for message in st.session_state.conversation_history:
    if message.startswith("You:"):
        st.markdown(f"<div style='text-align: right;'><span style='background-color: #007BFF; padding: 10px; border-radius: 10px;'>{message}</span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left;'><span style='background-color: #007BFF; padding: 10px; border-radius: 10px;'>{message}</span></div>", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 50px;'></div>", unsafe_allow_html=True)

# Place the text input and send button below the conversation
if st.session_state.authenticated:
    user_input = st.text_input("Type your message here...", key="user_input")
    if st.button("Send"):
        if user_input:
            # Send user input to the Flask backend
            backend_response = send_to_backend(user_input)
            if backend_response:
                # Update conversation history
                st.session_state.conversation_history.append(f"You: {user_input}")
                st.session_state.conversation_history.append(f"Bot: {backend_response['response']}")
                st.rerun()  # Refresh the app to show new messages
else:
    st.warning("Please sign in to chat.")