import serial
import time

# 시리얼 포트 설정 (포트명은 사용 환경에 맞게 변경: 예) 'COM3' 또는 '/dev/ttyUSB0')
ser = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)  # 아두이노가 리셋되는 시간을 고려하여 대기

# 예시 리스트: 각 인덱스에 해당하는 서보모터의 동작 상태 (1: 180도, 0: 0도)
motor_list = [1, 0, 1, 0, 1, 0]

# 리스트를 문자열로 변환 ("101010")
data_to_send = ''.join(str(bit) for bit in motor_list)

# 문자열에 개행 문자('\n') 추가 후 전송
ser.write((data_to_send + "\n").encode())
print("전송한 데이터:", data_to_send)

ser.close()