# Secure AI Chatbot (Groq Edition)

## Product Requirements Document (PRD)

**Version:** 1.0  
**Date:** 2025

---

# 1. Product Overview

The Secure AI Chatbot is an AI-powered conversational assistant designed to answer user queries professionally while enforcing strict safety and security rules.

The system integrates with Groq-hosted LLMs and includes multiple layers of protection against:

- Prompt injection attacks
- Harmful or illegal requests
- Sensitive data extraction attempts
- Unsafe model behavior

The chatbot returns structured JSON responses for reliable downstream integration.

---

# 2. Problem Statement

Traditional AI chatbots can often be manipulated through malicious prompts, jailbreak attempts, or prompt injection techniques.

This project aims to provide a chatbot architecture with guardrails enforced at both:

1. Application Layer
2. LLM Prompt Layer

---

# 3. Product Goals

| Goal | Description |
|------|-------------|
| Natural Language Understanding | Interpret and respond to user queries accurately |
| Safety Enforcement | Block harmful, illegal, or unsafe requests |
| Structured Output | Return consistent JSON responses |
| Injection Resistance | Detect and reject prompt injection attempts |

---

# 4. Target Users

- Internal company employees
- Customer support teams
- Organizations requiring safe AI interactions

---

# 5. Core Features

| Priority | Feature | Description |
|----------|---------|-------------|
| P0 | `POST /chat` | Main chatbot interaction endpoint |
| P0 | `GET /health` | Service health/liveness endpoint |
| P0 | Keyword-Based Guardrails | Detect harmful or restricted content |
| P0 | Prompt Injection Detection | Identify jailbreak and injection attempts |
| P0 | Groq LLM Integration | AI response generation |
| P0 | Structured JSON Responses | Consistent machine-readable output |

---

# 6. Tech Stack

| Layer | Technology |
|------|-------------|
| Programming Language | Python 3.10+ |
| Backend Framework | Flask 3 |
| LLM Provider | Groq |
| Model | llama-3.1-8b-instant |
| HTTP Client | requests |
| Environment Config | python-dotenv |
