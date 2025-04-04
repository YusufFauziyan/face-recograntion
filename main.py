from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import face_recognition
import numpy as np
import os
import shutil
from typing import List
from pathlib import Path

app = FastAPI()

# Folder tempat foto model disimpan
MODEL_FOLDER = "models"

# Load face encodings dari folder model
def load_known_faces():
    known_encodings = []
    known_names = []

    for filename in os.listdir(MODEL_FOLDER):
        path = os.path.join(MODEL_FOLDER, filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(filename)
        else:
            print(f"Wajah tidak terdeteksi di {filename}")

    return known_encodings, known_names

# Endpoint untuk verifikasi wajah
@app.post("/verify-face")
async def verify_face(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="File harus berupa gambar")

    # Simpan file sementara
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Load dan encode wajah yang diupload
        unknown_image = face_recognition.load_image_file(temp_path)
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        if not unknown_encodings:
            raise HTTPException(status_code=400, detail="Wajah tidak terdeteksi di gambar")

        unknown_encoding = unknown_encodings[0]

        # Bandingkan dengan wajah-wajah model
        known_encodings, known_names = load_known_faces()
        results = face_recognition.compare_faces(known_encodings, unknown_encoding)
        face_distances = face_recognition.face_distance(known_encodings, unknown_encoding)

        if True in results:
            best_match_index = np.argmin(face_distances)
            matched_name = known_names[best_match_index]
            similarity = 1 - face_distances[best_match_index]
            return JSONResponse(content={
                "status": "valid",
                "matched_with": matched_name,
                "similarity_score": round(float(similarity), 2)
            })
        else:
            return JSONResponse(content={
                "status": "invalid",
                "message": "Tidak ada wajah yang cocok ditemukan"
            })

    finally:
        os.remove(temp_path)
