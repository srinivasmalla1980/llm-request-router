const userInput = document.getElementById("userInput");
const runButton = document.getElementById("runButton");
const chatForm = document.getElementById("chatForm");
const chatHistory = document.getElementById("chatHistory");
const status = document.getElementById("status");

// Replace this with your actual Render service URL.
const API_URL = "https://llm-request-router-api.onrender.com";

function addMessage(role, text) {
  const message = document.createElement("div");
  message.className = "message " + role;

  const heading = document.createElement("strong");
  heading.textContent = role === "user" ? "You" : "AI Assistant";

  const content = document.createElement("p");
  content.textContent = text;

  message.appendChild(heading);
  message.appendChild(content);
  chatHistory.appendChild(message);

  message.scrollIntoView({
    behavior: "smooth",
    block: "end"
  });
}

chatForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const question = userInput.value.trim();

  if (!question) {
    status.textContent = "Please enter a question.";
    userInput.focus();
    return;
  }

  addMessage("user", question);

  userInput.value = "";
  userInput.disabled = true;
  runButton.disabled = true;
  status.textContent = "Generating response...";

  const loadingMessage = document.createElement("div");
  loadingMessage.className = "message assistant";
  loadingMessage.textContent = "Thinking...";
  chatHistory.appendChild(loadingMessage);

  try {
    const response = await fetch(API_URL + "/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question: question })
    });

    if (!response.ok) {
      throw new Error("API returned HTTP " + response.status);
    }

    const data = await response.json();

    const answer =
      data.answer ??
      data.response ??
      data.result ??
      data.output;

    if (answer === undefined || answer === null) {
      throw new Error("No answer found in the API response.");
    }

    loadingMessage.remove();

    addMessage(
      "assistant",
      typeof answer === "string"
        ? answer
        : JSON.stringify(answer, null, 2)
    );

    status.textContent = "Response received.";
  } catch (error) {
    console.error("Chat API error:", error);

    loadingMessage.textContent =
      "Unable to get a response. Please check the API configuration.";

    status.textContent = error.message;
  } finally {
    userInput.disabled = false;
    runButton.disabled = false;
    userInput.focus();
  }
});
