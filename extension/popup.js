document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const fileInput = document.getElementById("fileInput");
  const result = document.getElementById("result");

  if (!fileInput.files.length) {
    result.innerText = "Please select a file";
    return;
  }

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  const isVideo = file.type.startsWith("video");
  const url = isVideo
    ? "http://127.0.0.1:8000/predict/video"
    : "http://127.0.0.1:8000/predict/image";

  result.innerText = "Analyzing...";

  const response = await fetch(url, {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  result.innerText = `${data.label} (confidence: ${data.confidence})`;
});
