def classify_request(user_request):
    response = llm.invoke(...)

    return {
        "route": response.route,
        "reason": response.reason
    }
