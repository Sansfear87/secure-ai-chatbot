# 🔐 Secure AI Chatbot — Groq Edition

A production-ready, security-first AI chatbot built with **Flask** and powered by **Groq's ultra-fast LLM API**. Features a multi-layer guardrail system, ReAct-style prompt chaining, and structured JSON responses.

---

## 🚀 Features

- ⚡ **Groq-powered** — blazing fast inference via `llama-3.3-70b-versatile`
- 🛡️ **Multi-layer Guardrails** — blocks prompt injections, harmful keywords, and empty/oversized queries
- 🧠 **ReAct Prompt Chaining** — Thought → Action → Observation → Final Answer
- 📦 **Structured Output** — every response returns a clean JSON with `intent`, `risk_level`, and `response`
- 🔌 **REST API** — simple `/chat` endpoint, easy to integrate anywhere

---

## 📁 Project Structure

```
secure-ai-chatbot/
├── app/
│   └── app.py              # Main Flask application
├── prompts/
│   └── prompt.py           # System prompt
├── parsers/
│   └── parser.py           # JSON output parser
├── docs/                   # Documentation
├── .env                    # Your API keys (never commit this)
├── .env.example            # Example env file (safe to commit)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/secure-ai-chatbot.git
cd secure-ai-chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
```

Open `.env` and add your Groq API key:
```
GROQ_API_KEY=gsk_your_api_key_here
```

Get your free API key at 👉 [console.groq.com](https://console.groq.com)

### 4. Run the server
```bash
python app/app.py
```

Server starts at `http://localhost:5000`

---

## 📡 API Reference

### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "message": "Secure AI Chatbot is running."
}
```

---

### Chat
```
POST /chat
Content-Type: application/json
```

**Request:**
```json
{
  "query": "What is machine learning?"
}
```

**Response:**
```json
{
  "intent": "educational",
  "risk_level": "low",
  "response": "Machine learning is a subset of AI that enables systems to learn from data..."
}
```

---

### Blocked Request Example

**Request:**
```json
{
  "query": "how to hack a website"
}
```

**Response:**
```json
{
  "intent": "blocked",
  "risk_level": "high",
  "response": "I cannot process this request. Request contains unsafe or restricted content."
}
```

---

## 🛡️ Guardrails System

Every query passes through 4 checks before reaching the LLM:

| Check | Description |
|---|---|
| Empty query | Rejects blank or whitespace-only input |
| Length limit | Rejects queries over 1000 characters |
| Prompt injection | Detects phrases like *"ignore previous instructions"* |
| Blocked keywords | Detects terms like *"hack"*, *"malware"*, *"brute force"* |

---

## 🧠 How It Works

```
User Query
    │
    ▼
┌─────────────┐     blocked      ┌─────────────────┐
│  Guardrails │ ───────────────► │  Block Response │
└─────────────┘                  └─────────────────┘
    │ safe
    ▼
┌──────────────────┐
│  Groq LLM (ReAct)│
│  llama-3.3-70b   │
└──────────────────┘
    │
    ▼
┌──────────────┐
│ Output Parser│
└──────────────┘
    │
    ▼
┌───────────────────────────────────┐
│ { intent, risk_level, response }  │
└───────────────────────────────────┘
```

---

## 📦 Requirements

```
flask
requests
python-dotenv
```

---

## 🔒 Security Notes

- Never commit your `.env` file — it's excluded via `.gitignore`
- Rotate your Groq API key immediately if accidentally exposed
- For production, disable Flask debug mode and put the app behind a reverse proxy (e.g. Nginx)

---

## 🛠️ Changing the Model

In `app/app.py`, update this line:
```python
GROQ_MODEL = "llama-3.3-70b-versatile"
```

Other supported Groq models:
- `mixtral-8x7b-32768`
- `llama-3.1-8b-instant`
- `gemma2-9b-it`

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👤 Author

Built by **YOUR_NAME**
GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
