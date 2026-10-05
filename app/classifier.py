import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.prompts import CLASSIFICATION_SYSTEM_PROMPT


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_request(user_request: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": CLASSIFICATION_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_request,
            },
        ],
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)

    return result
