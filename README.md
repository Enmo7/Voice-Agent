# 🎙️ LiveKit Voice Agent with Gemini Live API & RAG

## 📋 Overview
This project demonstrates a real-time voice AI agent built using **LiveKit Agents** and **Google's Gemini Live API (Multimodal)**. The agent is designed to have natural, low-latency voice conversations with users via a web interface.

Key features include:
- **Native Audio Streaming:** Uses `Gemini 2.0 Flash (Experimental)` for direct speech-to-speech interaction without traditional STT/TTS pipelines.
- **RAG Integration:** Equipped with a Retrieval-Augmented Generation (RAG) system to fetch context from a local knowledge base (`knowledge.txt`) before answering.
- **Web Interface:** A simple frontend to connect to the LiveKit room and interact with the agent.

---

## 🏗️ Architecture

The system consists of three main components:

### 1. **Voice Agent (`agent.py`)**
- Connects to a LiveKit Room
- Uses `AgentSession` with `RealtimeModel` to stream audio directly to/from Gemini Live API
- Defines a custom tool (`search_knowledge`) that Gemini calls when it needs specific information

### 2. **RAG Engine (`rag.py`)**
- Loads text from `knowledge.txt`
- Chunks and embeds the text using `SentenceTransformers`
- Stores embeddings in a FAISS vector index for fast retrieval

### 3. **Token Server (`server.py`)**
- A simple Flask server that authenticates users and generates LiveKit Access Tokens
- Serves the web interface

---

## ⚙️ Prerequisites

- Python 3.10 or higher
- A **LiveKit Cloud** account (project URL, API Key, and Secret)
- A **Google AI Studio** account (API Key for Gemini)

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory and add your API keys:

```env
# LiveKit Credentials (Get from: https://cloud.livekit.io)
LIVEKIT_URL=wss://<your-project>.livekit.cloud
LIVEKIT_API_KEY=<your-api-key>
LIVEKIT_API_SECRET=<your-api-secret>

# Google Gemini API Key (Get from: https://makersuite.google.com/app/apikey)
GOOGLE_API_KEY=<your-google-api-key>
```

**How to get credentials:**
- **LiveKit:** Sign up at https://cloud.livekit.io → Create a new project → Copy URL, API Key, and Secret
- **Google Gemini:** Visit https://makersuite.google.com/app/apikey → Create API key

### 5. Prepare Knowledge Base
Edit the `knowledge.txt` file and add the information you want the agent to know about (e.g., company FAQs, technical docs). Ensure paragraphs are separated by blank lines for better chunking.

---

## ▶️ Usage

### Step 1: Start the Web Server
This server handles client connections and serves the frontend.

```bash
python server.py
```

**Output:** `Running on http://localhost:5000`

### Step 2: Start the Voice Agent
Open a new terminal and run the agent worker.

```bash
python agent.py dev
```

**Output:** `registered worker, waiting for connection.`

### Step 3: Connect
1. Open your browser and navigate to `http://localhost:5000`
2. Click **"Connect"**
3. Allow microphone access when prompted
4. Start talking to the agent! 🎙️

---

## 🧠 How RAG Works with Gemini Live API

1. **User Query:** The user asks a question (e.g., "Who founded the company?")

2. **Tool Calling:** Gemini Live API analyzes the intent. If the answer requires external knowledge, it pauses the voice generation and calls the `search_knowledge` function defined in `agent.py`

3. **Retrieval:** The `rag.py` engine converts the query into a vector and searches the FAISS index for the most relevant text chunks from `knowledge.txt`

4. **Context Injection:** The retrieved text is returned to Gemini

5. **Response:** Gemini generates a voice response incorporating the retrieved facts

---

## 🎯 Example Interactions

Try these questions with your agent:

- "What are your operating hours?"
- "How much does your service cost?"
- "What's your refund policy?"
- "How can I contact support?"
- "Tell me about the company"

The agent will automatically search the knowledge base and provide accurate answers!

---

## ⚠️ Known Limitations (Quota)

This project uses the **Gemini 2.0 Flash Experimental** model for the Live API.

**Quota Limits:** The free tier for this experimental model has strict daily limits. If you encounter a `1011 Internal Error` or `Quota Exceeded`, please:
- Try again later
- Switch to a new API Key
- Consider upgrading to a paid plan

**Alternative:** For production stability, the code can be adapted to use the Pipeline approach (STT→LLM→TTS) with Gemini 1.5 Flash.

---

## 📂 Project Structure

```
voice-agent/
├── agent.py              # Main entry point for the AI agent (LiveKit Worker)
├── server.py             # Flask server for generating tokens & serving UI
├── rag.py                # RAG logic (Loading, Embedding, Searching)
├── knowledge.txt         # The source data for RAG
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (Secrets - create this)
├── public/
│   ├── index.html        # Web interface
│   ├── client.js         # LiveKit client logic
│   └── style.css         # Styling
└── README.md             # This file
```

---

## 🔧 Customization

### Change Agent Voice
In `agent.py`, modify the `voice` parameter:

```python
realtime_model = RealtimeModel(
    voice="Charon",  # Options: Puck, Charon, Kore, Fenrir, Aoede
)
```

### Adjust RAG Behavior
In `rag.py`:
- Change `top_k=3` to retrieve more/fewer results
- Modify chunking strategy in `_load_and_index()`
- Switch embedding model for better accuracy

### Modify Agent Instructions
Edit the `instructions` parameter in `agent.py` to change how the agent behaves and responds.

---

## 🐛 Troubleshooting

### Error: Cannot import RealtimeModel
```bash
pip install --upgrade livekit-plugins-google>=0.6.0
```

### Error: No module named 'sentence_transformers'
```bash
pip install sentence-transformers faiss-cpu
```

### Agent not responding
- Verify `.env` file has correct API keys
- Ensure both `server.py` and `agent.py` are running
- Check browser console for errors (F12)
- Confirm microphone permissions are granted

### Poor audio quality
- Check internet connection stability
- Ensure microphone is working properly
- Try different browser (Chrome/Edge recommended)
- Verify LiveKit URL is correct in `.env`

### Quota exceeded error
- Wait 24 hours for quota reset
- Create a new Google API key
- Consider upgrading to paid tier

---

## 📚 Additional Resources

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [Gemini Live API Docs](https://ai.google.dev/gemini-api/docs/live)
- [FAISS Vector Search](https://github.com/facebookresearch/faiss)
- [SentenceTransformers](https://www.sbert.net/)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs via Issues
- Submit Pull Requests
- Suggest new features
- Improve documentation

---

## 📄 License

This project is provided as-is for educational and demonstration purposes.

---

## 🎉 Next Steps

- **Enhance RAG:** Add PDF/document processing
- **Multi-language Support:** Add translation capabilities
- **Authentication:** Implement user authentication
- **Conversation History:** Store and retrieve past conversations
- **Deploy to Production:** Host on cloud platforms

