import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("텍스트 인식 프로그램")
        self.setGeometry(100, 100, 400, 200)

        self.pdfButton = QPushButton("📂 PDF 인식 실행", self)
        self.pdfButton.clicked.connect(self.runPDFReader)

        self.webcamButton = QPushButton("📷 웹캠 인식 실행", self)
        self.webcamButton.clicked.connect(self.runWebcamOCR)

        layout = QVBoxLayout()
        layout.addWidget(self.pdfButton)
        layout.addWidget(self.webcamButton)

        self.setLayout(layout)

    def runPDFReader(self):
        """PDF 리더와 점자 변환 실행"""
        subprocess.Popen(["python", "main.py"])  # ✅ `main.py` 실행 → 점자 변환 + PDF 리더

    def runWebcamOCR(self):
        """웹캠 OCR 실행"""
        subprocess.Popen(["python", "webcam.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())
