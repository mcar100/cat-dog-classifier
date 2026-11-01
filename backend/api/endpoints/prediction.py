from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from app.model import predict_image
from api.config import IMAGE_MAX_SIZE, ALLOWED_IMAGE_TYPES

router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
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