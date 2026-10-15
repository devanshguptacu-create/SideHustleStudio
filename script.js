const form = document.getElementById("listingForm");
const generateBtn = document.getElementById("generateBtn");
const emptyState = document.getElementById("emptyState");
const loadingState = document.getElementById("loadingState");
const resultWrap = document.getElementById("resultWrap");
const resultText = document.getElementById("resultText");
const errorBox = document.getElementById("errorBox");

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
}
function hideError() {
  errorBox.textContent = "";
  errorBox.classList.add("hidden");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError();
  emptyState.classList.add("hidden");
  resultWrap.classList.add("hidden");
  loadingState.classList.remove("hidden");
  generateBtn.disabled = true;
  generateBtn.innerHTML = '<span>✦</span> Generating locally…';

  const payload = {
    product: document.getElementById("product").value.trim(),
    platform: document.getElementById("platform").value,
    language: document.getElementById("language").value,
    audience: document.getElementById("audience").value.trim(),
    tone: document.getElementById("tone").value,
    price: document.getElementById("price").value.trim(),
    details: document.getElementById("details").value.trim()
  };

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "The listing could not be generated.");
    resultText.value = data.result;
    resultWrap.classList.remove("hidden");
  } catch (error) {
    emptyState.classList.remove("hidden");
    showError(error.message || "Could not connect to the local AI backend.");
  } finally {
    loadingState.classList.add("hidden");
    generateBtn.disabled = false;
    generateBtn.innerHTML = '<span>✦</span> Generate my listing <span class="arrow">↗</span>';
  }
});

document.getElementById("copyBtn").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(resultText.value);
    const button = document.getElementById("copyBtn");
    button.textContent = "Copied!";
    setTimeout(() => button.textContent = "Copy draft", 1500);
  } catch {
    resultText.select();
    document.execCommand("copy");
  }
});

document.getElementById("downloadBtn").addEventListener("click", () => {
  const blob = new Blob([resultText.value], {type: "text/plain;charset=utf-8"});
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "sidehustle-listing.txt";
  link.click();
  URL.revokeObjectURL(url);
});
