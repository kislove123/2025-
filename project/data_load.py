# parser_module.py

import re
import json

def parse_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 기본 패턴: r = [[0,0],[0,0],[0,0]]
    pattern_single = r'(\w+)\s*=\s*(\[\[.*?\]\])'
    # 예외 패턴: ㄱ = [[0,0],[0,0],[0,0]], [[0,0],[0,0],[0,0]]
    pattern_multi = r'(\w+)\s*=\s*(\[\[.*?\]\](?:,\s*\[\[.*?\]\])*)'

    data = {}

    # 여러 개의 리스트가 포함된 패턴 탐색
    for match in re.findall(pattern_multi, content):
        key, value = match
        data[key] = json.loads(f"[{value}]")  # 안전한 변환

    # 단일 리스트 패턴 탐색
    for match in re.findall(pattern_single, content):
        key, value = match
        if key not in data:
            data[key] = json.loads(value)

    return data

# 파일을 불러와 전역 변수에 저장
parsed_data_v = parse_txt_file(r"C:\Users\KOREAN\Downloads\project\grammar_data\모음.txt")
parsed_data_c_end = parse_txt_file(r"C:\Users\KOREAN\Downloads\project\grammar_data\자음 종성.txt")
parsed_data_c_start = parse_txt_file(r"C:\Users\KOREAN\Downloads\project\grammar_data\자음 초성.txt")
parsed_data_word = parse_txt_file(r"C:\Users\KOREAN\Downloads\project\grammar_data\예외사항.txt")
parsed_data_n = parse_txt_file(r"C:\Users\KOREAN\Downloads\project\grammar_data\숫자.txt")
parsed_data_caution = parse_txt_file(r"C:\Users\KOREAN\Downloads\project\grammar_data\주위해야 할것.txt")
parsed_data_symb = parse_txt_file(r"C:\Users\KOREAN\Downloads\project\grammar_data\문장부호.txt")

# 모듈을 import한 다른 파일에서 바로 접근할 수 있습니다.

