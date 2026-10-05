from app.classifier import classify_request


questions = [
    "What is our company's parental leave policy?",
    "Summarize this paragraph for me.",
    "Find my open invoices and email them to me.",
]


for question in questions:
    result = classify_request(question)

    print("\nQuestion:", question)
    print("Classification:", result)
