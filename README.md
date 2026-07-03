# 🤖 AI Personality Chatbot

An interactive AI chatbot built with **Streamlit**, **LangChain**, and **Mistral AI** that allows users to chat with different AI personalities such as a Teacher, Coding Assistant, Career Coach, Research Assistant, Content Writer, Study Buddy, and more.

## 🚀 Live Demo

https://ai-personality-chatbot.onrender.com

---

## ✨ Features

- 🎭 Multiple AI Personalities
  - Teacher
  - Coding Assistant
  - Study Buddy
  - Career Coach
  - Content Writer
  - Research Assistant
  - Friendly Assistant
  - Funny Assistant
  - Motivational Coach
  - Default Assistant

- 💬 Interactive chat interface
- ⚡ Real-time streaming responses
- 📝 Chat history saved locally
- 📥 Download conversation
- 🗑️ Clear chat history
- 🎨 Clean and responsive Streamlit UI
- 🔄 Easy personality switching

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Mistral AI
- python-dotenv

---

## 📂 Project Structure

```
AI-Personality-Chatbot/
│
├── chatmodels/
│   ├── chatbot.py
│   ├── chat.py
│   └── UIchatbot.py
│
├── app.py
├── chat_history.json
├── requirements.txt
├── .gitignore
├── .env (not included)
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/2k23cs2313652-rishi/AI-Personality-Chatbot.git

cd AI-Personality-Chatbot
```

### 2. Create a virtual environment

Using **uv**

```bash
uv venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

---

### 4. Create a `.env` file

Create a file named `.env` in the project root.

```env
MISTRAL_API_KEY=your_api_key_here
```

---

### 5. Run the application

```bash
streamlit run app.py
```

---

## 🎮 Usage

1. Launch the application.
2. Select an AI personality.
3. Type your question.
4. Receive intelligent responses powered by Mistral AI.
5. Download or clear the conversation anytime.

---

## 📸 Screenshots

Add screenshots of your application here.

Example:

```
images/
├── home.png
├── chat.png
└── personalities.png
```

---

## 📦 Requirements

Major libraries used:

- streamlit
- langchain
- langchain-mistralai
- python-dotenv

See `requirements.txt` for the complete list.

---

## 🔮 Future Improvements

- Voice input
- Voice output
- Conversation memory
- RAG (Retrieval-Augmented Generation)
- PDF Chat
- Web Search
- Image generation
- Multi-language support
- User authentication
- Cloud deployment

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature-name
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push to your branch.

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

## 👨‍💻 Author

**Rishi Gupta**

GitHub:
https://github.com/2k23cs2313652-rishi

---

## ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates further development.

---

## 📄 License

This project is licensed under the MIT License.
