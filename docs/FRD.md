# Secure AI Chatbot (Groq Edition)

# Functional Requirements Document (FRD)

**Version:** 1.0  
**Date:** 2025

---

# 1. API Endpoints

## GET `/health`

### Purpose
Verify that the service is operational.

### Success Response

```json
{
  "status": "ok",
  "message": "Secure AI Chatbot is running."
}
```

---

## POST `/chat`

### Request

```json
{
  "query": "string (max 1000 chars)"
}
```

### Success Response

```json
{
  "intent": "brief description of user intent",
  "risk_level": "low | medium | high",
  "response": "assistant reply"
}
```

---

# 2. Guardrails Specification

## Blocked Keywords

- hack
- exploit
- malware
- ransomware
- sql injection
- phishing
- jailbreak
- brute force

---

# 3. LLM Integration

| Configuration | Value |
|--------------|------|
| Provider | Groq |
| Model | llama-3.1-8b-instant |
| Endpoint | `/chat/completions` |
| Authentication | Bearer API Key |
| Temperature | `0.3` |
| Max Output Tokens | `512` |

---

# 4. Output Schema

```json
{
  "intent": "string",
  "risk_level": "low | medium | high",
  "response": "string"
}
```

---

# 5. Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `app/main.py` | Flask routes, Guardrails logic, Chatbot pipeline |
| `prompts/prompt.py` | Stores `SYSTEM_PROMPT` constant |
| `parsers/parser.py` | Parses and validates LLM responses |
