# 학습한 모델로 새로운 이미지 분류하기
import torch
import torch.nn as nn
import torchvision
from pathlib import Path
from PIL import Image
from .transforms import valid_transforms  # 변환 정의 가져오기

# 프로젝트 루트 및 모델 파일 경로
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_SAVE_PATH = BASE_DIR / 'models' / 'cat_dog_classifier.pth'  # 학습된 모델 저장 경로
# 실행 장치 설정
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model():
    # 1. 모델 아키텍처 정의
    model = torchvision.models.resnet18(weights=None)  # 사전 훈련된 가중치 없이 ResNet18 모델 생성
    model.fc = nn.Linear(model.fc.in_features, 2)  # 마지막 레이어의 입력 뉴런 조정: 고양이와 개로 출력 (0: 고양이, 1: 개)

    # 2. 저장된 모델 상태 사전 불러오기
    state_dict = torch.load(
        MODEL_SAVE_PATH, 
        map_location=DEVICE, 
        weights_only=True
    )
    model.load_state_dict(state_dict)
    # 3. 모델 평가모드로 전환
    model = model.to(DEVICE)
    model.eval()
    return model

model = load_model()

# 5. 이미지 전처리 정의 
def preprocess_image(image: Image.Image):
    # PIL 라이브러리로 이미지 로드
    image = image.convert('RGB')  # 이미지를 RGB로 변환
    # 전처리 불러오기 및 적용 후 반환
    return valid_transforms(image).unsqueeze(0).to(DEVICE)  # 배치 차원 추가 및 GPU 이동

# 6. 예측 수행 및 결과 반환
def predict_image(image: Image.Image) -> dict:
    # 이미지 전처리
    image_tensor = preprocess_image(image)

    # 예측 수행
    with torch.inference_mode():
        outputs = model(image_tensor)
        # 클래스별 확률 계산
        probabilities = nn.functional.softmax(outputs, dim=1)[0]

    # 클래스별 확률
    cat_probability = probabilities[0].item()
    dog_probability = probabilities[1].item()

    predicted_class = (
        "cat" if cat_probability >= dog_probability else "dog"
    )

    # API 응답결과
    return {
        "class_name": predicted_class,
        "cat_probability": round(cat_probability, 6),
        "dog_probability": round(dog_probability, 6)
    }
