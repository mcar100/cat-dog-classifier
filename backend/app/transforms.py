import torchvision.transforms as transforms

# 학습 데이터에 적용할 변환 및 증강
train_transforms = transforms.Compose([
    transforms.RandomRotation(10),  # 무작위로 10도 회전
    transforms.RandomResizedCrop(224),  # 무작위로 자른 후 224x224로 크기 조정
    transforms.RandomHorizontalFlip(),  # 무작위로 좌우 반전
    transforms.ToTensor(),  # 이미지 -> 텐서
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 정규화 - ImageNet의 최적 평균과 표준편차 사용
])

# 검증 및 테스트 데이터에 적용할 변환
# 평가용 데이터에는 증강 적용X
valid_transforms = transforms.Compose([
    transforms.Resize(256),  # 256x256로 크기 조정
    transforms.CenterCrop(224),  # 중앙에서 224x224로 자르기
    transforms.ToTensor(),  # 이미지 -> 텐서
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 정규화 - ImageNet의 최적 평균과 표준편차 사용
])