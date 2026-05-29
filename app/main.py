"""
Secure AI Chatbot — Flask application.

Architecture:
  User Query
    └─► Guardrails (keyword + injection checks)
          └─► Chatbot.get_response() → Groq REST API
                └─► OutputParser → structured JSON response
"""

import os
import sys

import requests
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompts.prompt import SYSTEM_PROMPT
from parsers.parser import parse_response
from flask_cors import CORS

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = "llama-3.3-70b-versatile"

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------------------------
# Frontend route
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return send_file(os.path.join(base_dir, "index.html"))

# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------

BLOCKED_KEYWORDS = [
    "hack", "exploit", "malware", "virus", "ransomware",
    "sql injection", "ddos attack", "phishing", "crack password",
    "jailbreak", "root access", "admin credentials", "bypass security",
    "brute force", "keylogger"
]

INJECTION_PHRASES = [
    "ignore previous instructions",
    "forget your rules",
    "ignore your system prompt",
    "you are now",
    "act as if",
    "pretend you are",
    "reveal admin",
    "disregard all",
    "override instructions",
    "new persona",
    "ignore all above"
]


class Guardrails:
    """
    Validates user input before it reaches the LLM.

    Checks performed (in order):
      1. Empty / whitespace-only query
      2. Query length limit
      3. Prompt injection phrases
      4. Blocked keywords
    """

    @staticmethod
    def has_injection(query: str) -> bool:
        """Return True if the query contains a prompt injection phrase."""
        lower = query.lower()
        return any(phrase in lower for phrase in INJECTION_PHRASES)

    @staticmethod
    def is_blocked(query: str) -> bool:
        """Return True if the query contains a blocked keyword."""
        lower = query.lower()
        return any(word in lower for word in BLOCKED_KEYWORDS)

    @staticmethod
    def is_safe(query: str) -> tuple:
        """
        Run all safety checks.

        Returns:
            (True, "ok") if the query is safe.
            (False, reason: str) if any check fails.
        """
        if not query or len(query.strip()) == 0:
            return False, "Query cannot be empty."
        if len(query) > 1000:
            return False, "Query is too long. Please keep it under 1000 characters."
        if Guardrails.has_injection(query):
            return False, "Prompt injection attempt detected."
        if Guardrails.is_blocked(query):
            return False, "Request contains unsafe or restricted content."
        return True, "ok"


# ---------------------------------------------------------------------------
# Chatbot
# ---------------------------------------------------------------------------

class Chatbot:
    """
    Handles LLM interaction using the Groq REST API (OpenAI-compatible).

    Reasoning flow (ReAct):
      Thought   → understand what the user wants
      Action    → build prompt and call Groq
      Observation → parse JSON from the response
      Final Answer → return structured dict to caller
    """

    def _build_prompt(self, user_query: str) -> str:
        """Wrap the user query with a ReAct-style reasoning prefix."""
        return (
            "Thought: Carefully read and understand what the user is asking.\n"
            "Action: Evaluate whether the request is safe, then craft a professional reply.\n"
            "Observation: The request has already passed the safety guardrails.\n"
            "Final Answer: Reply ONLY with a valid JSON object — no extra text.\n\n"
            f"User query: {user_query}"
        )

    def get_response(self, user_query: str) -> dict:
        """
        Send the query to Groq and return a parsed structured response.

        Args:
            user_query: Sanitised user input (already cleared by Guardrails).

        Returns:
            dict with keys: intent, risk_level, response.

        Raises:
            requests.RequestException: if the Groq API call fails.
        """
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": self._build_prompt(user_query)}
            ],
            "temperature": 0.3,
            "max_tokens": 512,
            "response_format": {"type": "json_object"}
        }

        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        raw_text = data["choices"][0]["message"]["content"]
        return parse_response(raw_text)


# Singleton instances
chatbot    = Chatbot()
guardrails = Guardrails()


# ---------------------------------------------------------------------------
# Prompt-chain pipeline
# ---------------------------------------------------------------------------

def run_pipeline(user_query: str) -> tuple:
    """
    Full prompt-chaining pipeline:
      1. Safety Check  (Guardrails)
      2. Intent Detection + Response Generation  (Groq)
      3. JSON Formatting  (OutputParser — inside Chatbot.get_response)

    Returns:
        (result_dict, http_status_code)
    """
    # Stage 1 — Safety Check
    safe, reason = guardrails.is_safe(user_query)
    if not safe:
        return {
            "intent": "blocked",
            "risk_level": "high",
            "response": f"I cannot process this request. {reason}"
        }, 200

    # Stage 2 & 3 — LLM call + JSON formatting
    try:
        result = chatbot.get_response(user_query)
        return result, 200
    except requests.HTTPError as exc:
        return {
            "intent": "error",
            "risk_level": "low",
            "response": f"AI service returned an error: {exc.response.status_code}"
        }, 502
    except requests.RequestException:
        return {
            "intent": "error",
            "risk_level": "low",
            "response": "Failed to reach the AI service. Please try again later."
        }, 502


# ---------------------------------------------------------------------------
# Flask routes
# ---------------------------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    """Health-check endpoint."""
    return jsonify({"status": "ok", "message": "Secure AI Chatbot is running."})


@app.route("/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint.

    Request  (JSON): { "query": "<user message>" }
    Response (JSON): { "intent": "", "risk_level": "", "response": "" }
    """
    body = request.get_json(silent=True)

    if not body or "query" not in body:
        return jsonify({
            "intent": "unknown",
            "risk_level": "low",
            "response": "Please provide a 'query' field in your JSON request body."
        }), 400

    result, status = run_pipeline(body["query"])
    return jsonify(result), status


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
