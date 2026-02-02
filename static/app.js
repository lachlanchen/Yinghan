const form = document.getElementById("upload-form");
const statusEl = document.getElementById("status");
const annotatedImg = document.getElementById("annotated");
const maskImg = document.getElementById("mask");
const overlayCanvas = document.getElementById("overlay");
const fileInput = document.getElementById("image");

function setStatus(message) {
  statusEl.textContent = message;
}

function drawOverlay(imageUrl, polygon) {
  const img = new Image();
  img.onload = () => {
    overlayCanvas.width = img.width;
    overlayCanvas.height = img.height;
    const ctx = overlayCanvas.getContext("2d");
    ctx.clearRect(0, 0, img.width, img.height);
    ctx.drawImage(img, 0, 0);

    if (polygon && polygon.length > 2) {
      ctx.beginPath();
      ctx.moveTo(polygon[0][0], polygon[0][1]);
      for (let i = 1; i < polygon.length; i += 1) {
        ctx.lineTo(polygon[i][0], polygon[i][1]);
      }
      ctx.closePath();
      ctx.fillStyle = "rgba(255, 0, 0, 0.25)";
      ctx.strokeStyle = "rgba(255, 0, 0, 0.9)";
      ctx.lineWidth = 2;
      ctx.fill();
      ctx.stroke();
    }
  };
  img.src = imageUrl;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const file = fileInput.files[0];
  if (!file) {
    setStatus("Please select an image.");
    return;
  }

  const model = document.getElementById("model").value || "gpt-4o-2024-08-06";
  const formData = new FormData();
  formData.append("image", file);
  formData.append("model", model);

  setStatus("Uploading and segmenting…");

  try {
    const response = await fetch("/api/segment", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      const detail = error.error_type ? ` (${error.error_type})` : "";
      throw new Error(`${error.error || "Segmentation failed"}${detail}`);
    }

    const data = await response.json();
    annotatedImg.src = data.annotated_url;
    maskImg.src = data.mask_url;
    drawOverlay(data.upload_url, data.polygon);

    setStatus(`Done. Confidence: ${(data.confidence * 100).toFixed(1)}%`);
  } catch (err) {
    setStatus(`Error: ${err.message}`);
  }
});

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (!file) {
    return;
  }
  const previewUrl = URL.createObjectURL(file);
  drawOverlay(previewUrl, null);
  setStatus("Ready to segment.");
});

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/static/sw.js");
  });
}
