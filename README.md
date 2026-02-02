# 🕵️‍♂️ Deepfake Detector

A **full-stack AI-powered Deepfake Detection system** that allows users to **right-click on any image in the browser** and instantly check whether it is **AI-generated or real**.

This project combines:

* 🧠 **Deep Learning (PyTorch + CNN)**
* 🌐 **FastAPI backend**
* 🧩 **Chrome Extension (Manifest V3)**

---

## ✨ Key Features

* 🔍 Right-click **Detect Deepfake** on any image
* ⚡ Real-time inference using a CNN model
* 📊 Confidence-based output (AI / Real / Uncertain)
* 🧠 Smart thresholding to reduce false positives
* 🔔 Native Chrome notifications
* 🛡️ Handles hotlink-protected images safely

---

## 🏗️ Project Architecture

```
Deepfake Detector
│
├── chrome_extension/
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── popup.html
│   ├── popup.js
│   ├── styles.css
│   └── icon.png
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── api/
│       │   ├── image_routes.py
│       │   └── video_routes.py
│       ├── services/
│       │   └── image_infer.py
│       └── core/
│           └── model_loader.py
│
├── ml/
│   └── checkpoints/
│       └── image_model.pth
│
├── requirements.txt
└── README.md
```

---

## 🧠 Tech Stack

### 🔹 Backend

* **FastAPI** – REST API
* **Uvicorn** – ASGI server
* **PyTorch** – Model inference
* **Torchvision** – Image transforms
* **Pillow / OpenCV** – Image processing
* **Requests** – Fetch image URLs
* **Pydantic** – Request validation

### 🔹 Frontend (Chrome Extension)

* JavaScript (Vanilla)
* Chrome Extensions API (Manifest V3)
* Context Menus
* Notifications API

---

## 🚀 How to Run the Project

### 1️⃣ Backend Setup

#### 📦 Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

#### 📥 Install dependencies

```bash
pip install -r requirements.txt
```

#### ▶️ Start FastAPI server

```bash
uvicorn backend.app.main:app --reload
```

📍 Server runs at: `http://127.0.0.1:8000`

Swagger UI:
👉 `http://127.0.0.1:8000/docs`

---

### 2️⃣ Chrome Extension Setup

1. Open Chrome → `chrome://extensions`
2. Enable **Developer Mode**
3. Click **Load unpacked**
4. Select `chrome_extension/` folder
5. Done ✅

---

## 🖱️ How to Use

1. Open any website with images
2. Right-click on an image
3. Click **Detect Deepfake**
4. Get instant notification:

   * **AI Generated**
   * **Real**
   * **Uncertain**

---

## 📊 API Response Format

```json
{
  "label": "AI Generated | Real | Uncertain",
  "confidence": 92.3,
  "ai_probability": 92.3
}
```

* `confidence` → final confidence (%)
* `ai_probability` → raw model probability

---

## 🎯 Model Logic (Important)

* Sigmoid-based CNN output
* Smart thresholds:

```text
AI Generated  → score ≥ 0.75
Real          → score ≤ 0.45
Uncertain     → otherwise
```

This avoids **overconfident false positives**.

---

## 🧪 Testing Websites

* Google Images
* Unsplash (real photos)
* Midjourney / DALL·E samples
* Reddit AI Art communities

---

## ⚠️ Known Limitations

* Small images (<160px) → marked Uncertain
* Highly edited real images may confuse model
* Model trained only on images (not video frames yet)

---

## 🔮 Future Improvements

* ✅ Dataset expansion
* 🎥 Video deepfake detection
* 📈 Confidence calibration
* ☁️ Cloud deployment
* 🧪 Ensemble models

---

## 🧑‍💻 Author

**Akash Singh**
AI / ML | Full Stack | Chrome Extensions

---

## ⭐ Final Note

This project demonstrates **end-to-end AI system building**:

* Model → API → Browser Extension → User

Perfect for:

* Major project
* Portfolio
* Interviews

---

🚀 *Built with logic, patience, and lots of debugging.*
