const testType = document.getElementById("testType");
const userInput = document.getElementById("userInput");
const runButton = document.getElementById("runButton");
const status = document.getElementById("status");

runButton.addEventListener("click", () => {
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

  status.textContent =
    `Selected test: ${script}\n` +
    "The interface is ready. Python execution is not connected yet.";
});
