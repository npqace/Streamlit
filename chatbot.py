import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.title("Basic Chatbot")

# Hugging Face Credentials
with st.sidebar:
    st.title("Login HugChat")
    hf_email = st.text_input("Enter E-mail:")
    hf_pwd = st.text_input("Enter Password:", type="password")
    if not(hf_email and hf_pwd):
        st.warning("Please enter your email!")
    else:
        st.success("Proceed to entering your prompt message!")
        
        
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{'role': "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
# Function for generating LLM response
def gen_res(prompt, email, pwd):
    # Hugging Face Login
    sign = Login(email, pwd)
    cookies = sign.login()
    # Create chatbot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt)

# User-provided prompt
if prompt := st.chat_input(disabled=not(hf_email and hf_pwd)):
    st.session_state.messages.append({'role': "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = gen_res(prompt, hf_email, hf_pwd)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)