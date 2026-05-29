# FRD — Functional Requirements Document
## Secure AI Chatbot (Gemini Edition)

**Version:** 1.0  
**Date:** 2025

---

## 1. API Endpoints

### GET `/health`
- **Purpose:** Verify the service is alive
- **Response:**
  ```json
  { "status": "ok", "message": "Secure AI Chatbot is running." }
  ```

### POST `/chat`
- **Purpose:** Submit a user query and receive an AI response
- **Request body:**
  ```json
  { "query": "string (max 1000 chars)" }
  ```
- **Success response (200):**
  ```json
  {
    "intent":     "brief description of user intent",
    "risk_level": "low | medium | high",
    "response":   "assistant reply"
  }
  ```
- **Error responses:**
  - `400` — missing `query` field
  - `502` — Gemini API unreachable

---

## 2. Prompt-Chain Pipeline

```
User Query
  │
  ▼
[Stage 1] Guardrails.is_safe()
  │  fail → return blocked JSON (risk_level: high)
  │  pass ↓
[Stage 2] Chatbot.get_response() → Gemini API
  │
  ▼
[Stage 3] parse_response() → structured dict
  │
  ▼
jsonify → HTTP response
```

---

## 3. Guardrails Specification

### 3a. Blocked Keywords
Queries containing any of the following are rejected immediately:

`hack` · `exploit` · `malware` · `virus` · `ransomware` · `sql injection` ·
`ddos attack` · `phishing` · `crack password` · `jailbreak` · `root access` ·
`admin credentials` · `bypass security` · `brute force` · `keylogger`

### 3b. Injection Phrases
Queries containing any of the following are rejected immediately:

`ignore previous instructions` · `forget your rules` · `you are now` ·
`act as if` · `pretend you are` · `reveal admin` · `disregard all` ·
`override instructions` · `new persona` · `ignore all above`

### 3c. Validation Rules

| Rule | Limit |
|------|-------|
| Empty query | Rejected |
| Query length | Max 1000 characters |

---

## 4. LLM Integration

| Field | Value |
|-------|-------|
| Model | `gemini-1.5-flash` |
| Endpoint | `POST /v1beta/models/gemini-1.5-flash:generateContent` |
| Auth | API key via query param `?key=` |
| Temperature | 0.3 |
| Max tokens | 512 |
| Response MIME | `application/json` |

---

## 5. ReAct Prompt Structure

```
Thought:     Carefully read and understand what the user is asking.
Action:      Evaluate whether the request is safe, then craft a reply.
Observation: The request has already passed the safety guardrails.
Final Answer: Reply ONLY with a valid JSON object — no extra text.

User query: <user_query>
```

---

## 6. Output Schema

Every response from the system (including blocked/error cases) must match:

```json
{
  "intent":     "string",
  "risk_level": "low | medium | high",
  "response":   "string"
}
```

---

## 7. Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `app/main.py` | Flask routes, Guardrails class, Chatbot class, pipeline |
| `prompts/prompt.py` | System prompt constant `SYSTEM_PROMPT` |
| `parsers/parser.py` | `parse_response(raw_text)` → validated dict |
