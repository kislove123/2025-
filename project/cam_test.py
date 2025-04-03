import cv2
import numpy as np

def decode_predictions(scores, geometry, conf_threshold):
    """
    EAST 모델의 예측 결과에서 바운딩 박스 좌표와 신뢰도를 디코딩합니다.
    """
    (num_rows, num_cols) = scores.shape[2:4]
    rects = []
    confidences = []

    # 각 행과 열을 순회하며
    for y in range(num_rows):
        scoresData = scores[0, 0, y]
        x0_data = geometry[0, 0, y]
        x1_data = geometry[0, 1, y]
        x2_data = geometry[0, 2, y]
        x3_data = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        for x in range(num_cols):
            score = scoresData[x]
            if score < conf_threshold:
                continue

            # 해당 셀의 오프셋 계산 (4픽셀 단위)
            offsetX = x * 4.0
            offsetY = y * 4.0
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # 박스의 높이와 너비 계산
            h = x0_data[x] + x2_data[x]
            w = x1_data[x] + x3_data[x]

            # 회전 변환을 고려한 박스의 좌표 계산
            endX = int(offsetX + (cos * x1_data[x]) + (sin * x2_data[x]))
            endY = int(offsetY - (sin * x1_data[x]) + (cos * x2_data[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            rects.append((startX, startY, endX, endY))
            confidences.append(float(score))

    return rects, confidences

# 이미지와 모델 로드
image = cv2.imread(r"C:\Users\Admin\Downloads\project\text_images\Cider.png")  # 분석할 이미지 경로 지정
orig = image.copy()
(H, W) = image.shape[:2]

# EAST 모델은 320x320 등 고정 크기의 입력을 사용합니다.
(newW, newH) = (320, 320)
rW = W / float(newW)
rH = H / float(newH)

# 이미지 리사이즈 및 blob 변환
resized = cv2.resize(image, (newW, newH))
blob = cv2.dnn.blobFromImage(resized, 1.0, (newW, newH),
                              (123.68, 116.78, 103.94), swapRB=True, crop=False)

# EAST 텍스트 감지 모델 로드 (사전 학습된 모델 파일 필요: frozen_east_text_detection.pb)
net = cv2.dnn.readNet("frozen_east_text_detection.pb")

# 모델의 출력 레이어 이름 지정
layerNames = [
    "feature_fusion/Conv_7/Sigmoid",  # 텍스트 확률
    "feature_fusion/concat_3"         # 기하학 정보
]

net.setInput(blob)
(scores, geometry) = net.forward(layerNames)

# 디코딩을 통해 바운딩 박스와 신뢰도 얻기
conf_threshold = 0.5  # 신뢰도 임계값 (필요에 따라 조정)
rects, confidences = decode_predictions(scores, geometry, conf_threshold)

# Non-Maximum Suppression으로 중복 박스 제거
indices = cv2.dnn.NMSBoxes(rects, confidences, conf_threshold, 0.4)

# 검출된 박스를 원본 이미지에 표시 (원본 크기로 좌표 보정)
if len(indices) > 0:
    for i in indices.flatten():
        (startX, startY, endX, endY) = rects[i]
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

cv2.imshow("Detected Text", orig)
cv2.waitKey(0)
cv2.destroyAllWindows()
