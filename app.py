"""
AI Personality Chatbot
-----------------------
A Streamlit + LangChain + Mistral chatbot with:
- 12 distinct personalities (each with its own system prompt style)
- Real streaming responses (token-by-token)
- Typing indicator
- Download conversation (as .txt or .json)
- Clear chat button
- Persistent chat history (saved to disk, survives app restarts)
- Improved UI (sidebar controls, avatars, message count, custom styling)

Setup:
    pip install streamlit langchain-mistralai langchain-core python-dotenv
    Create a .env file with: MISTRAL_API_KEY=your_key_here
    Run: streamlit run app.py
"""

import os
import json
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

HISTORY_FILE = "chat_history.json"

st.set_page_config(
    page_title="AI Personality Chatbot",
    page_icon="🤖",
    layout="centered",
)

PERSONALITIES = {
    "🤖 Default Assistant": (
        "You are a helpful, neutral AI assistant. Answer clearly, accurately, "
        "and concisely, without adopting any particular emotional tone."
    ),
    "👨‍🏫 Teacher": (
        "You are a patient, encouraging teacher. Explain concepts step-by-step, "
        "use simple analogies, check for understanding, and break complex ideas "
        "into small, digestible pieces. Ask a short follow-up question when it "
        "helps confirm the student has understood."
    ),
    "👨‍💻 Coding Assistant": (
        "You are an expert software engineer. Give precise, correct, well-formatted "
        "code with brief explanations. Point out edge cases, bugs, and better "
        "practices when relevant. Prefer concise code blocks over long prose."
    ),
    "📚 Study Buddy": (
        "You are a friendly study partner helping with exam prep. Use mnemonics, "
        "quiz the user occasionally, summarize key points in bullet form, and keep "
        "explanations exam-focused and dense rather than verbose."
    ),
    "💼 Career Coach": (
        "You are a professional career coach. Give practical, actionable advice on "
        "resumes, interviews, career growth, and workplace situations. Be direct, "
        "supportive, and results-oriented."
    ),
    "✍️ Content Writer": (
        "You are a skilled content writer and editor. Help craft engaging, "
        "well-structured writing. Offer stronger phrasing, better hooks, and "
        "tighter structure. Adapt tone to the type of content requested."
    ),
    "🧠 Research Assistant": (
        "You are a meticulous research assistant. Provide well-organized, "
        "evidence-based answers. Structure information clearly with headings or "
        "bullet points when useful, and note where something is uncertain or "
        "requires verification."
    ),
    "😂 Funny": (
        "You are a witty AI assistant. Reply with humor, jokes, and playful "
        "energy, while still actually answering the question."
    ),
    "😊 Friendly": (
        "You are a warm, friendly AI assistant. Reply in a supportive, "
        "conversational tone, like a kind friend who's happy to help."
    ),
    "🎯 Motivational": (
        "You are a high-energy motivational coach. Reply with encouragement, "
        "confidence, and momentum, pushing the user toward action while still "
        "giving them a genuinely useful answer."
    ),
    "😢 Sad": (
        "You are a sad AI assistant. Reply in a gloomy, emotional tone, while "
        "still providing a genuinely useful answer underneath the melancholy."
    ),
    "😄 Happy": (
        "You are a happy AI assistant. Reply in a cheerful, optimistic tone, "
        "full of enthusiasm."
    ),
}

# --------------------------------------------------------------------------
# Persistence helpers
# --------------------------------------------------------------------------

def load_history():
    """Load saved chat history (if any) from disk."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
            messages = []
            for item in raw:
                if item["role"] == "system":
                    messages.append(SystemMessage(content=item["content"]))
                elif item["role"] == "human":
                    messages.append(HumanMessage(content=item["content"]))
                elif item["role"] == "ai":
                    messages.append(AIMessage(content=item["content"]))
            return messages
        except Exception:
            return None
    return None


def save_history(messages):
    """Persist chat history to disk as JSON."""
    raw = []
    for msg in messages:
        if isinstance(msg, SystemMessage):
            role = "system"
        elif isinstance(msg, HumanMessage):
            role = "human"
        elif isinstance(msg, AIMessage):
            role = "ai"
        else:
            continue
        raw.append({"role": role, "content": msg.content})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)


def messages_to_text(messages):
    """Convert conversation to a readable .txt transcript."""
    lines = [f"AI Personality Chatbot — Conversation Export ({datetime.now():%Y-%m-%d %H:%M})", "=" * 60, ""]
    for msg in messages:
        if isinstance(msg, HumanMessage):
            lines.append(f"You: {msg.content}\n")
        elif isinstance(msg, AIMessage):
            lines.append(f"AI: {msg.content}\n")
    return "\n".join(lines)


def messages_to_json(messages):
    raw = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            raw.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            raw.append({"role": "assistant", "content": msg.content})
    return json.dumps(raw, ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------
# Custom styling
# --------------------------------------------------------------------------

st.markdown(
    """
    <style>
    .stChatMessage {
        border-radius: 14px;
        padding: 4px 6px;
    }
    div[data-testid="stSidebarUserContent"] {
        padding-top: 1.2rem;
    }
    .app-subtitle {
        color: #888;
        font-size: 0.9rem;
        margin-top: -10px;
        margin-bottom: 1.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------

with st.sidebar:
    st.header("⚙️ Settings")

    personality = st.selectbox("Choose AI Personality", list(PERSONALITIES.keys()))

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        clear_clicked = st.button("🗑️ Clear Chat", use_container_width=True)
    with col2:
        # placeholder so layout stays even; real download buttons appear below
        st.write("")

    if "messages" in st.session_state:
        chat_msgs = [m for m in st.session_state.messages if not isinstance(m, SystemMessage)]
        if chat_msgs:
            st.download_button(
                "⬇️ Download as .txt",
                data=messages_to_text(st.session_state.messages),
                file_name=f"chat_{datetime.now():%Y%m%d_%H%M%S}.txt",
                mime="text/plain",
                use_container_width=True,
            )
            st.download_button(
                "⬇️ Download as .json",
                data=messages_to_json(st.session_state.messages),
                file_name=f"chat_{datetime.now():%Y%m%d_%H%M%S}.json",
                mime="application/json",
                use_container_width=True,
            )

    st.divider()
    if "messages" in st.session_state:
        n_user = sum(isinstance(m, HumanMessage) for m in st.session_state.messages)
        st.caption(f"💬 {n_user} message(s) in this conversation")
    st.caption("Chat history is saved automatically and persists between sessions.")

# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------

st.title("🤖 AI Personality Chatbot")
st.markdown(f"<div class='app-subtitle'>Currently talking to: <b>{personality}</b></div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Session state init / persistence load
# --------------------------------------------------------------------------

if "messages" not in st.session_state:
    loaded = load_history()
    if loaded and isinstance(loaded[0], SystemMessage):
        st.session_state.messages = loaded
    else:
        st.session_state.messages = [SystemMessage(content=PERSONALITIES[personality])]

# Handle clear chat
if clear_clicked:
    st.session_state.messages = [SystemMessage(content=PERSONALITIES[personality])]
    save_history(st.session_state.messages)
    st.rerun()

# If personality changed, reset system prompt but keep option to preserve history
if st.session_state.messages[0].content != PERSONALITIES[personality]:
    st.session_state.messages[0] = SystemMessage(content=PERSONALITIES[personality])
    save_history(st.session_state.messages)

# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------

model = ChatMistralAI(
    model="mistral-small-latest",
    streaming=True,
)

# --------------------------------------------------------------------------
# Render existing conversation
# --------------------------------------------------------------------------

for msg in st.session_state.messages[1:]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar=personality.split(" ")[0]):
            st.write(msg.content)

# --------------------------------------------------------------------------
# Chat input + streaming response
# --------------------------------------------------------------------------

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append(HumanMessage(content=prompt))
    save_history(st.session_state.messages)

    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=personality.split(" ")[0]):
        placeholder = st.empty()
        placeholder.markdown("▌ *typing...*")

        full_response = ""
        try:
            for chunk in model.stream(st.session_state.messages):
                token = chunk.content or ""
                full_response += token
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"⚠️ Error contacting the model: {e}"
            placeholder.markdown(full_response)

    st.session_state.messages.append(AIMessage(content=full_response))
    save_history(st.session_state.messages)