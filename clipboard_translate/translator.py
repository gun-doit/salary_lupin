import sys, os
import pyperclip
from deep_translator import GoogleTranslator
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QToolBar, QToolButton
from PySide6.QtGui import QAction, QFont, QFontDatabase
from PySide6.QtCore import QTimer

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = GoogleTranslator(source="auto", target="ko")
        self.previous_text = ""
        self.is_translation_locked = False  # 번역 고정 여부
        self.setWindowTitle("Clipboard Translator")
        self.setGeometry(100, 100, 600, 400)

        # QTextEdit - 텍스트 출력 영역
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.setCentralWidget(self.text_edit)

        # 폰트 설정
        font_path = os.path.join(os.path.dirname(__file__), 'NanumGothic.ttf') 
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != 1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            font_family = "Arial"
            
        font = QFont(font_family, 12)
        self.text_edit.setFont(font)

        # QToolBar - 기능 바
        toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(toolbar)

        # 번역 고정 버튼 추가 (QToolButton 사용)
        self.button_lock_translation = QToolButton(self)
        self.button_lock_translation.setText("번역 고정")
        self.button_lock_translation.setCheckable(True)  # 버튼이 체크 가능하도록 설정
        self.button_lock_translation.clicked.connect(self.toggle_translation_lock)
        toolbar.addWidget(self.button_lock_translation)

        # 종료 버튼 추가
        action_exit = QAction("Exit", self)
        action_exit.triggered.connect(self.close)
        toolbar.addAction(action_exit)

        # QTimer 사용하여 클립보드를 주기적으로 확인
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_clipboard)  # 타이머가 종료될 때마다 클립보드 확인
        self.timer.setInterval(500)  # 1초마다 체크 (1000ms)

        # 번역 고정된 상태에서 타이머 시작
        self.timer.start()

    def toggle_translation_lock(self):
        """번역 고정 상태를 토글"""
        self.is_translation_locked = not self.is_translation_locked


    def check_clipboard(self):
        """클립보드를 확인하여 텍스트가 변경되었을 때 번역 후 업데이트"""
        if self.is_translation_locked:
            return  # 번역 고정 시, 클립보드 내용에 관계없이 업데이트하지 않음

        clipboard_text = pyperclip.paste()
        if clipboard_text and clipboard_text != self.previous_text:
            self.previous_text = clipboard_text
            self.update_translate_text(clipboard_text)

    def update_translate_text(self, new_text):
        """클립보드 내용이 변경되었을 때 번역 후 업데이트"""
        translated_text = self.translator.translate(new_text)
        self.text_edit.setText(f"{translated_text}")

    def closeEvent(self, event):
        """창 닫기 이벤트"""
        self.timer.stop()  # 타이머 종료
        event.accept()  # 창 닫기 실행

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
