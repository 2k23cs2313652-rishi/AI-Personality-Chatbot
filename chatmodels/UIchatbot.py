from dotenv import load_dotenv
import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

st.set_page_config(
    page_title="AI Personality Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI Personality Chatbot")

role = st.selectbox(
    "Choose AI Personality",
    ["Sad", "Happy", "Funny"]
)

role_prompts = {
    "Sad": "You are a sad AI assistant. Reply in a gloomy and emotional tone.",
    "Happy": "You are a happy AI assistant. Reply in a cheerful and optimistic tone.",
    "Funny": "You are a funny AI assistant. Reply with humor and jokes."
}

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=role_prompts[role])
    ]

if st.session_state.messages[0].content != role_prompts[role]:
    st.session_state.messages = [
        SystemMessage(content=role_prompts[role])
    ]

model = ChatMistralAI(
    model="mistral-small-latest"
)

for msg in st.session_state.messages[1:]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    with st.chat_message("user"):
        st.write(prompt)

    response = model.invoke(st.session_state.messages)

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

    with st.chat_message("assistant"):
        st.write(response.content)