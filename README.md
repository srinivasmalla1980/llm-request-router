LLM Request Router

An LLM-powered request routing system that classifies user queries into SIMPLE_LLM, RAG, or AGENT routes using a Mistral LLM hosted on Hugging Face Spaces. Based on the classification result, the application routes the original request to the appropriate LLM or execution pipeline.

Architecture
flowchart TD
    A["User Request"] --> B["Classifier.py"]

    subgraph APP["LLM Request Router Application"]
        B
        D["Parse Classification JSON"]
        E{"Route Decision"}

        F["General-Purpose LLM"]
        G["RAG Pipeline"]
        H["Agent / Tool Execution"]

        I["Generate Final Response"]

        B --> D
        D --> E

        E -->|SIMPLE_LLM| F
        E -->|RAG| G
        E -->|AGENT| H

        F --> I
        G --> I
        H --> I
    end

    subgraph HF["Hugging Face Spaces"]
        C["Mistral LLM Endpoint"]
    end

    B <-->|"API Request / Response"| C

    I --> J["Return Response to User"]

    classDef app fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef hf fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef routing fill:#ede9fe,stroke:#7c3aed,color:#4c1d95
    classDef output fill:#dcfce7,stroke:#16a34a,color:#14532d

    class A,B,D app
    class C hf
    class E,F,G,H routing
    class I,J output

How It Works
User Request: The application receives a question or instruction from the user.
Request Classification: Classifier.py combines the user's request with the classification system prompt.
Mistral LLM Endpoint: The classifier sends the prompt to the Mistral LLM endpoint hosted on Hugging Face Spaces using gradio_client.
Classification Response: The endpoint returns a classification result containing the selected route and a short explanation.
Route Selection: The application parses the classification result and determines which processing pipeline should handle the request.
Request Execution: The original user request is forwarded to the appropriate LLM, RAG pipeline, or agent.
Final Response: The selected component generates the answer, which is returned to the user.
Available Routes
Route	Purpose	Example
SIMPLE_LLM	Handles requests that can be answered using general knowledge, reasoning, or text generation.	Explain how Python decorators work.
RAG	Handles requests that require information from enterprise documents, internal databases, policies, or other private knowledge sources.	What is our company's leave policy?
AGENT	Handles requests that require tools, APIs, external systems, or multiple operational steps.	Create a support ticket for this issue.
Classification Output

The classifier returns a JSON object with two fields:

{
  "route": "RAG",
  "reason": "The request requires information from enterprise documents."
}


The route field determines the execution path, while the reason field explains the classification decision.

Technology Stack
Python — Application and routing logic.
Mistral LLM — Request classification.
Hugging Face Spaces — Hosting the classification model endpoint.
Gradio Client — Communicating with the hosted model endpoint.
LLM / RAG / Agent pipelines — Processing requests after classification.
Project Goal

The goal of this project is to separate request classification from request execution. Instead of sending every request to the same LLM or pipeline, the application identifies the type of request first and routes it to the appropriate processing component.

This architecture can be extended with additional models, routing rules, fallback mechanisms, and model-selection strategies as the application evolves.
