
from io import BytesIO
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware 
from PIL import Image, UnidentifiedImageError
from .model import predict_image

# 엔드포인트
app = FastAPI(title="Cats vs Dogs API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],)

IMAGE_MAX_SIZE = 10 * 1024 * 1024

@app.get("/health")
def health_check():
    return { "status": "ok" }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in {
        "image/jpeg",
        "image/png",
        "image/webp",
    }:
        raise HTTPException(
            status_code=400,
            detail="JPG, PNG, WEBP 이미지 파일만 지원가능합니다."
        )
    content = await file.read()

    if len(content) > IMAGE_MAX_SIZE:
        raise HTTPException(
            status_code=413,
            detail="이미지는 10MB 이하만 업로드할 수 있습니다."
        )

    try:
        image = Image.open(BytesIO(content))
        image.load()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="올바른 이미지 파일이 아닙니다."
        )

    return predict_image(image)
