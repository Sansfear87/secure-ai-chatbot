"""
Output parser — safely extracts structured JSON from Gemini's raw text response.
Handles markdown fences, extra whitespace, and malformed output gracefully.
"""

import json


def parse_response(raw_text: str) -> dict:
    """
    Parse LLM output into a structured dictionary.

    Strategy:
      1. Strip markdown code fences (```json ... ```) if present.
      2. Locate the first { ... } JSON block.
      3. Parse and validate required fields.
      4. Return a safe fallback dict if any step fails.

    Args:
        raw_text: Raw string returned by the Gemini API.

    Returns:
        dict with keys: intent, risk_level, response.
    """
    try:
        clean = raw_text.strip()

        # Remove markdown code fences if present
        if clean.startswith("```"):
            lines = clean.splitlines()
            # Drop first line (```json or ```) and last line (```)
            clean = "\n".join(lines[1:-1]).strip()

        # Extract the first JSON object
        start = clean.find("{")
        end = clean.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("No JSON object found in LLM response.")

        json_str = clean[start:end]
        data = json.loads(json_str)

        # Validate and normalise fields
        valid_risk_levels = {"low", "medium", "high"}
        risk = str(data.get("risk_level", "low")).lower()
        if risk not in valid_risk_levels:
            risk = "low"

        return {
            "intent": str(data.get("intent", "unknown")).strip(),
            "risk_level": risk,
            "response": str(data.get("response", "I could not generate a response.")).strip()
        }

    except (ValueError, KeyError, json.JSONDecodeError):
        return {
            "intent": "unknown",
            "risk_level": "low",
            "response": "Sorry, I encountered an error processing your request. Please try again."
        }
