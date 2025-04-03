def decompose_char(char):
        # 한글 음절 범위가 아니라면 그대로 반환
        if not ('가' <= char <= '힣'):
            return char, '', ''
        code = ord(char) - ord('가')
        jong = code % 28
        jung = ((code - jong) // 28) % 21
        cho = ((code - jong) // 28) // 21

        # 초성, 중성, 종성 목록
        CHOSUNG = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
                'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        JUNGSUNG = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
                    'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
        JONGSUNG = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ',
                    'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                    'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        
        return CHOSUNG[cho], JUNGSUNG[jung], JONGSUNG[jong]

def txt_to_list(text):    


    decomposed_list = []


    for char in text:
        if char == " ":
            # 공백은 그대로 추가하거나 건너뛰는 방식 선택 가능
            decomposed_list.append(" ")
        else:
            components = decompose_char(char)
            for idx, comp in enumerate(components):
                decomposed_list.append(comp)

    return decomposed_list


def cho_or_jong(text):
    # 값을 매핑하는 규칙: 초성 -> 0, 중성 -> 0.5, 종성 -> 1
    value_mapping = {0: 0, 1: 0.5, 2: 1}  # 인덱스에 따른 값

    decomposed_chojong = []
    for char in text:
        if char == " ":
            decomposed_chojong.append(None)
        else:
            components = decompose_char(char)
            for idx, comp in enumerate(components):
                decomposed_chojong.append(value_mapping[idx])

    return decomposed_chojong