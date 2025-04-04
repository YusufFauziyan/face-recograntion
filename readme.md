---
## 📸 Face Attendance API

A simple face attendance system using **FastAPI** and **face\_recognition**. The API compares an uploaded face image to reference model photos stored in a folder.
---

### ✅ Features

- Upload face image via API
- Verify if the face matches any registered model
- Returns matched model name and similarity score

---

### 🛠️ Requirements

- Python 3.8+
- CMake installed (required for `dlib`)
- pip packages (see below)

---

### 📦 Installation

```bash
# 1. Clone this repository
git clone https://github.com/YusufFauziyan/face-attendance-api.git
cd face-attendance-api

# 2. (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install CMake (for macOS)
brew install cmake

# 4. Install Python dependencies
pip install -r requirements.txt
```

---

### 📂 Project Structure

```
face_attendance/
├── main.py              # Main API script
├── models/              # Folder with model images (e.g., model1.jpg)
    ├── temp_*.jpg           # Temporary files (auto deleted)
├── .gitignore
└── README.md
```

---

### 🚀 Running the API

```bash
uvicorn main:app --reload
```

Then open Swagger UI documentation at:

```
http://127.0.0.1:8000/docs
```

---

### 📤 API Endpoint

#### `POST /verify-face`

Uploads an image and verifies the face against known models.

**Request:**

- Form-data:
  - `file`: Image file (JPG/PNG)

**Successful match response:**

```json
{
  "status": "valid",
  "matched_with": "model1.jpg",
  "similarity_score": 0.85
}
```

**No match found:**

```json
{
  "status": "invalid",
  "message": "No matching face found"
}
```

---

### 📝 Notes

- Model face images must be placed inside the `models/` folder.
- If no face is detected in the uploaded image, the request will be rejected.
- Suitable for building prototypes of face-based attendance or access control systems.

---
