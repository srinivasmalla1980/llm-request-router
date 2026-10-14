from app.classifier import classify_request

result = classify_request(
    "Write a Python function to sort a list"
)

print(result)
print(type(result))
