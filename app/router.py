from app.classifier import classify_request
from app.generator import generate_response


def route_request(user_request: str) -> dict:
    # Step 1: Classify the request
    classification = classify_request(user_request)

    route = classification.get("route", "SIMPLE_LLM")

    # Step 2: Select the model for the route
    # Initially, all routes use your Qwen model.
    if route in {"SIMPLE_LLM", "CODING"}:
        answer = generate_response(user_request)
    else:
        # Safe fallback until additional models are configured
        answer = generate_response(user_request)

    # Step 3: Return both the routing decision and answer
    return {
        "route": route,
        "reason": classification.get("reason", ""),
        "answer": answer,
    }
