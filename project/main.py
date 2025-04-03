import sys
import data_load
import decomposing
from PyQt6.QtWidgets import QApplication
from text_extruder import PDFReader  # text_extruder.py에서 PDFReader 가져옴

# 예외 음절 목록
EXCEPTION_LIST = [
    "가", "나", "다", "라", "마", "바", "사", "아", "자", "차", "카", "파", "하",
    "억", "언", "얼", "연", "열", "영", "옥", "온", "옹", "운", "울", "은", "을",
    "인", "것", "ㅆ"
]

# 된소리(긴장된 자음) 집합
TENSE_CONSONANTS = {"ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ"}

def flatten_data(data):
    """리스트를 완전히 1차원 리스트로 변환"""
    if data is None:
        return None  # None 그대로 유지
    if isinstance(data, list):
        flattened = []
        for item in data:
            if isinstance(item, list):
                flattened.extend(flatten_data(item))  # 재귀적으로 리스트 풀기
            else:
                flattened.append(item)  # 단일 값 추가
        return flattened
    return [data]  # 단일 숫자인 경우 리스트로 변환

def process_syllable(syllable):
    """한 음절을 분석하는 함수"""
    if syllable in EXCEPTION_LIST:
        exception_data = flatten_data(data_load.parsed_data_word.get(syllable))
        return [exception_data, None, None]  # 예외 글자는 [데이터, None, None]

    cho, jung, jong = decomposing.decompose_char(syllable)
    result = [None, None, None]  # [초성, 중성, 종성] 기본 틀 유지

    if cho:
        data_cho = flatten_data(data_load.parsed_data_c_start.get(cho))
        if cho in TENSE_CONSONANTS:
            result[0] = flatten_data(data_load.parsed_data_c_end.get("된소리"))
        result[0] = data_cho if data_cho else None

    if jung:
        data_jung = flatten_data(data_load.parsed_data_v.get(jung))
        result[1] = data_jung if data_jung else None

    if jong:
        data_jong = flatten_data(data_load.parsed_data_c_end.get(jong))
        if jong in TENSE_CONSONANTS:
            result[2] = flatten_data(data_load.parsed_data_c_end.get("된소리"))
        result[2] = data_jong if data_jong else None

    return result

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.reader = PDFReader()
        self.reader.selected_character.connect(self.update_text)  # PDF에서 선택한 글자 연결
        self.reader.show()
    
    def update_text(self, new_char):
        """PDF에서 선택한 글자를 input_text로 업데이트하고, 변환된 데이터를 출력"""
        global input_text
        input_text = new_char  
        print(f"\n🔵 선택된 글자: {input_text}")  # 터미널에 실시간 출력

        processed = process_syllable(input_text)  # 변환 실행
        print("\n🟡 변환된 점자 데이터:")
        print(processed)  # 리스트 형태 그대로 출력

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()