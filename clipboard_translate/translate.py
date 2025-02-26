import os
import sys
import tkinter as tk
import tkinter.font as tkFont
import pyperclip
import time
from deep_translator import GoogleTranslator
from tkinter import scrolledtext
from ctypes import windll

# ✅ 실행 파일 내부에서 폰트 경로 설정
def resource_path(relative_path):
    """ PyInstaller 사용 시, 실행 파일 내부의 리소스 경로를 반환 """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)  # EXE 내부 경로
    return os.path.join(os.path.abspath("."), relative_path)  # 일반 실행 경로

# TTF 폰트 경로 설정
FONT_PATH = resource_path("NanumGothic.ttf")

# Windows에서 외부 폰트 등록
def load_ttf_font(font_path):
    FR_PRIVATE = 0x10
    FR_NOT_ENUM = 0x20
    windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)

load_ttf_font(FONT_PATH)  # ✅ 폰트 로드

# Tkinter 창 생성
root = tk.Tk()
root.title("Clipboard Translator")

# 번역기 설정
translator = GoogleTranslator(source='auto', target='ko')

# 폰트 적용 (예외 처리 포함)
try:
    custom_font = tkFont.Font(root=root, family="NanumGothic", size=14)
except:
    custom_font = tkFont.Font(root=root, family="Arial", size=14)  # 대체 폰트 적용

# 텍스트 박스 (스크롤 가능)
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
text_widget.pack(expand=True, fill="both")

# 폰트 적용
text_widget.configure(font=custom_font, padx=10, pady=10)

# 클립보드 감시 함수
def check_clipboard():
    try:
        clipboard_text = pyperclip.paste()
        if clipboard_text and clipboard_text != check_clipboard.previous_text:
            translated_text = translator.translate(clipboard_text)

            text_widget.configure(state="normal")
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, translated_text)
            text_widget.configure(state="disabled")

            check_clipboard.previous_text = clipboard_text
    except Exception as e:
        text_widget.configure(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, "번역 오류 발생")
        text_widget.configure(state="disabled")

    root.after(1000, check_clipboard)

check_clipboard.previous_text = ""
check_clipboard()
root.mainloop()
