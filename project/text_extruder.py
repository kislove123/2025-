import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QFileDialog
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor
from PyQt6.QtCore import Qt, pyqtSignal
import PyPDF2
from PyQt6.QtCore import Qt, QEvent

class PDFReader(QWidget):
    selected_character = pyqtSignal(str)  # ✅ 선택된 글자를 main.py로 전달하는 시그널

    def __init__(self):
        super().__init__()

        self.initUI()
        self.text = ""
        self.index = 0  # 현재 글자 위치
        self.current_char = ""  # 현재 하이라이트된 글자

    def initUI(self):
        self.setWindowTitle("PDF Reader")
        self.setGeometry(100, 100, 800, 600)

        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.textEdit.installEventFilter(self)

        # ✅ QTextEdit가 방향키 이벤트를 잡아먹지 않도록 변경
        self.textEdit.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.openButton = QPushButton("📂 PDF 열기", self)
        self.openButton.clicked.connect(self.loadPDF)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.openButton)

        self.setLayout(layout)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # ✅ 창에 포커스 유지
        self.setFocus()  # ✅ 창이 열릴 때 포커스를 메인 창으로 설정

        # ✅ GUI 디자인 변경
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QTextEdit {
                background-color: white;
                color: black;
                font-size: 16px;
                border: 2px solid #cccccc;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                font-size: 14px;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)

    def loadPDF(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        
        if filePath:
            self.extractText(filePath)
            self.index = 0  # 처음부터 시작
            self.textEdit.setPlainText(self.text)  
            self.highlightCharacter()  

    def extractText(self, filePath):
        with open(filePath, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            self.text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])

    def keyPressEvent(self, event):
        """ 방향키를 눌렀을 때 글자 이동 """
        if event.key() == Qt.Key.Key_Right and self.index < len(self.text) - 1:
            self.index += 1
        elif event.key() == Qt.Key.Key_Left and self.index > 0:
            self.index -= 1

        self.highlightCharacter()  

    def highlightCharacter(self):
        """현재 글자를 노란색으로 하이라이트하고, 이전 글자의 하이라이트를 제거"""
        cursor = self.textEdit.textCursor()

        cursor.select(QTextCursor.SelectionType.Document)
        clear_format = QTextCharFormat()
        clear_format.setBackground(QColor("white"))  
        cursor.mergeCharFormat(clear_format)

        cursor.setPosition(self.index)
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)

        fmt = QTextCharFormat()
        fmt.setBackground(QColor("yellow"))  
        fmt.setForeground(QColor("black"))  # ✅ 포커스를 잃어도 글자가 회색으로 변하지 않도록 설정
        cursor.mergeCharFormat(fmt)

        self.textEdit.setTextCursor(cursor)  

        self.current_char = self.text[self.index]
        print(f"현재 글자: {self.current_char}")  

        self.selected_character.emit(self.current_char)  # ✅ 선택된 글자를 시그널로 보냄

    def eventFilter(self, obj, event):
        """ QTextEdit의 기본 하이라이트(회색)를 무시하고 노란색으로 유지 """
        if obj == self.textEdit and event.type() == QEvent.Type.FocusIn:
            self.highlightCharacter()  # ✅ 포커스를 얻을 때 다시 노란색으로 설정
        return super().eventFilter(obj, event)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFReader()
    window.show()
    sys.exit(app.exec())
