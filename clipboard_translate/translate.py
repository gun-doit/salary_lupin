import tkinter as tk
import pyperclip
import time
from deep_translator import GoogleTranslator

# 번역기 설정 (자동 감지 → 한국어 번역)
translator = GoogleTranslator(source='auto', target='ko')

# Tkinter 윈도우 생성
root = tk.Tk()
root.title("번역기")
root.geometry("400x150")

# 번역 결과 표시 라벨
result_label = tk.Label(root, text="복사한 텍스트를 번역합니다.", font=("Arial", 14), wraplength=350)
result_label.pack(pady=20)

# 클립보드 감시 함수
def check_clipboard():
    try:
        clipboard_text = pyperclip.paste()  # 클립보드 내용 가져오기
        if clipboard_text and clipboard_text != check_clipboard.previous_text:
            translated_text = translator.translate(clipboard_text)  # 번역 실행
            result_label.config(text=translated_text)  # 번역된 텍스트 UI 업데이트
            check_clipboard.previous_text = clipboard_text
    except Exception as e:
        result_label.config(text="번역 오류 발생")

    root.after(1000, check_clipboard)  # 1초마다 반복 실행

# 이전 텍스트 저장 변수
check_clipboard.previous_text = ""

# 클립보드 감지 시작
check_clipboard()

# Tkinter 실행
root.mainloop()
