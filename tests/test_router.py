from app.router import route_request


result = route_request(
    "Write a Python function to sort a list of integers"
)

print("\n--- ROUTING RESULT ---")
print("Route:", result["route"])
print("Reason:", result["reason"])

print("\n--- GENERATED ANSWER ---")
print(result["answer"])
