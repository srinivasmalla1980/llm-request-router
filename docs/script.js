```javascript
const testType = document.getElementById("testType");
const userInput = document.getElementById("userInput");
const runButton = document.getElementById("runButton");
const status = document.getElementById("status");

// Replace with your actual Render service URL
const API_URL = "https://llm-request-router-api.onrender.com/";

runButton.addEventListener("click", async () => {
  const selectedTest = testType.value;
  const input = userInput.value.trim();

  if (!input) {
    status.textContent = "Please enter a test input.";
    userInput.focus();
    return;
  }

  const script =
    selectedTest === "classifier"
      ? "tests/test_classifier.py"
      : "tests/test_router.py";

  runButton.disabled = true;
  status.textContent =
    `Selected test: ${script}\n` +
    "Sending request to the API...";

  try {
    const response = await fetch(`${API_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question: input
      })
    });

    if (!response.ok) {
      throw new Error(`API request failed: HTTP ${response.status}`);
    }

    const data = await response.json();

    status.textContent =
      `Selected test: ${script}\n\n` +
      "API response:\n" +
      (data.answer ?? data.response ?? JSON.stringify(data, null, 2));

  } catch (error) {
    console.error("API error:", error);

    status.textContent =
      `Selected test: ${script}\n\n` +
      `Request failed: ${error.message}\n` +
      "Check the Render API URL, service status, and CORS settings.";
  } finally {
    runButton.disabled = false;
  }
});
```
