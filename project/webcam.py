import cv2
import easyocr
import data_load
import decomposing

# ✅ main.py의 점자 변환 데이터 가져오기
parsed_data_v = data_load.parsed_data_v
parsed_data_c_start = data_load.parsed_data_c_start
parsed_data_c_end = data_load.parsed_data_c_end
parsed_data_word = data_load.parsed_data_word

# 예외 음절 목록
EXCEPTION_LIST = [
    "가", "나", "다", "라", "마", "바", "사", "아", "자", "차", "카", "파", "하",
    "억", "언", "얼", "연", "열", "영", "옥", "온", "옹", "운", "울", "은", "을",
    "인", "것", "ㅆ"
]

# 된소리(긴장된 자음) 집합
TENSE_CONSONANTS = {"ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ"}

def flatten_data(data):
    """ 🚀 중첩 리스트를 모두 1차원으로 변환하는 함수 (재귀적으로 처리) """
    if data is None:
        return None
    if isinstance(data, list):
        return [bit for item in data for bit in (flatten_data(item) if isinstance(item, list) else [item])]
    return [data]  # 단일 값이면 리스트로 반환

def process_syllable(syllable):
    """ 한 음절을 분석하는 함수 """
    if syllable in EXCEPTION_LIST:
        # ✅ 예외 글자는 [데이터, None, None]으로 고정
        data = flatten_data(parsed_data_word.get(syllable))
        return [data, None, None]

    cho, jung, jong = decomposing.decompose_char(syllable)

    # ✅ 초성이 'ㅇ'이면 None 처리
    cho_data = flatten_data(parsed_data_c_start.get(cho)) if cho and cho != "ㅇ" else None
    jung_data = flatten_data(parsed_data_v.get(jung)) if jung else None
    jong_data = flatten_data(parsed_data_c_end.get(jong)) if jong else None

    # ✅ 된소리 처리
    if cho in TENSE_CONSONANTS:
        cho_data = flatten_data([parsed_data_c_end.get("된소리"), cho_data])
    if jong in TENSE_CONSONANTS:
        jong_data = flatten_data([parsed_data_c_end.get("된소리"), jong_data])

    return [cho_data, jung_data, jong_data]  # ✅ 반드시 [초성/None, 중성/None, 종성/None] 형태 유지

# ✅ OCR을 위한 EasyOCR 설정
reader = easyocr.Reader(['ko'])

# ✅ 웹캠 실행
cap = cv2.VideoCapture(1)

print("실시간 영상 창이 열립니다. OCR 수행은 'c' 키, 종료는 'q' 키를 누르세요.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 웹캠 영상 표시
    cv2.imshow("Webcam Feed", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        # ✅ OCR 수행
        results = reader.readtext(frame, detail=1)

        if results:
            best_result = max(results, key=lambda x: x[2])  # 가장 높은 정확도의 텍스트 선택
            best_text = best_result[1]
            print(f"\n🔵 인식된 텍스트: '{best_text}'")

            # ✅ 한 글자씩 점자로 변환하여 개별 출력
            for char in best_text:
                processed = process_syllable(char)
                print(f"\n🔠 글자: {char}")
                print(f"🟡 변환된 점자 데이터: {processed}")

        else:
            print("❌ 텍스트를 인식하지 못했습니다.")
    
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
