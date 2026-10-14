import json
import re
import os
from gradio_client import Client

from app.prompts import CLASSIFICATION_SYSTEM_PROMPT


client = Client("srinivasmalla/my-Qwen-llm",  token=os.getenv("HF_TOKEN") or None)


def classify_request(user_request: str) -> dict:
    prompt = f"""
{CLASSIFICATION_SYSTEM_PROMPT}

Return ONLY a valid JSON object.
Do not include markdown fences or explanations.

User request:
{user_request}
"""

    response = client.predict(
        message=prompt,
        api_name="/chat",
    )

    # Handle responses that may contain extra text
    if isinstance(response, dict):
        response = response.get("text", str(response))

    text = str(response).strip()

    # Remove markdown code fences if the model adds them
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        result = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Qwen did not return valid JSON: {text}"
        ) from exc

    if not isinstance(result, dict):
        raise ValueError("Expected a JSON object from Qwen")

    return result
