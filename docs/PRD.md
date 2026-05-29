# PRD — Product Requirements Document
## Secure AI Chatbot (Gemini Edition)

**Version:** 1.0  
**Date:** 2025

---

## 1. Overview

A secure, AI-powered chatbot that answers user queries professionally while enforcing strict safety rules and resisting malicious inputs. Powered by **Google Gemini 1.5 Flash**.

---

## 2. Problem Statement

Generic chatbots can be manipulated via prompt injection or tricked into producing harmful content. This product needs guardrails baked in at both the application layer and the LLM prompt layer.

---

## 3. Goals

| Goal | Description |
|------|-------------|
| Understand queries | Parse natural language user questions |
| Safe responses | Refuse harmful, illegal, or sensitive requests |
| Structured output | Return every response as `{ intent, risk_level, response }` |
| Injection resistance | Detect and block prompt injection attempts |

---

## 4. Target Users

- Internal company employees seeking quick answers
- Customer support teams using a chatbot front-end

---

## 5. Key Features

| # | Feature | Priority |
|---|---------|----------|
| 1 | `POST /chat` — main chat endpoint | P0 |
| 2 | `GET /health` — liveness probe | P0 |
| 3 | Keyword-based guardrails | P0 |
| 4 | Prompt injection detection | P0 |
| 5 | Gemini 1.5 Flash LLM integration | P0 |
| 6 | Structured JSON output (intent / risk_level / response) | P0 |

---

## 6. Non-Goals (v1)

- No user authentication or session management
- No persistent chat history / memory
- No multi-language support
- No rate limiting (add in v2)

---

## 7. Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Framework | Flask 3 |
| LLM | Google Gemini 1.5 Flash (REST) |
| HTTP Client | requests |
| Config | python-dotenv |

---

## 8. Success Metrics

- Blocked queries return `risk_level: high` within 50 ms (no LLM call)
- Safe queries return valid JSON 100% of the time
- Zero prompt injection bypasses in manual testing
