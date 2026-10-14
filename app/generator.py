from gradio_client import Client
import os

client = Client(
    "srinivasmalla/my-Qwen-llm",
    token=os.getenv("HF_TOKEN") or None,
)


def generate_response(user_request: str) -> str:
    prompt = f"""
You are a helpful AI assistant and coding expert.

Answer the user's request directly.
If the user asks for code, provide working code and a
brief explanation.

User request:
{user_request}
"""

    response = client.predict(
        message=prompt,
        api_name="/chat",
    )

    if isinstance(response, dict):
        response = response.get("text", str(response))

    return str(response).strip()
