console.log("✅ background.js loaded");

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "detect-deepfake",
    title: "Detect Deepfake",
    contexts: ["image"]
  });
});

chrome.contextMenus.onClicked.addListener((info) => {
  if (info.menuItemId === "detect-deepfake") {
    analyzeImage(info.srcUrl);
  }
});

async function analyzeImage(imageUrl) {
  try {
    console.log("🖼 Image URL:", imageUrl);

    // 1️⃣ IMAGE → BLOB (THIS IS CORRECT)
    const response = await fetch(imageUrl);
    const blob = await response.blob();

    // 2️⃣ FORM DATA
    const formData = new FormData();
    formData.append("file", blob, "image.jpg");

    console.log("🚀 Calling backend...");

    // 3️⃣ CALL IMAGE-BYTES ENDPOINT (IMPORTANT)
    const apiResponse = await fetch(
      "http://127.0.0.1:8000/image/predict/image-bytes",
      {
        method: "POST",
        body: formData   // ❌ NO headers here
      }
    );

    const data = await apiResponse.json();
    console.log("✅ API Response:", data);

    // 4️⃣ SAFE READ
    const label = data.label || "Unknown";
    const confidence = data.confidence ?? "N/A";

    // 5️⃣ NOTIFICATION
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icon.png",
      title: "Deepfake Result",
      message: `${label} (${confidence}%)`
    });

  } catch (err) {
    console.error("❌ Error:", err);

    chrome.notifications.create({
      type: "basic",
      iconUrl: "icon.png",
      title: "Deepfake Detector Error",
      message: "Failed to analyze image"
    });
  }
}
