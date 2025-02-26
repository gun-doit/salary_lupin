import os
import sys
import tkinter as tk
import tkinter.font as tkFont
import pyperclip
from deep_translator import GoogleTranslator
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

# 스크롤바 숨기기 위한 설정
text_widget = tk.Text(root, wrap=tk.WORD, width=50, height=20)
text_widget.pack(expand=True, fill="both", padx=10, pady=10)

# 텍스트 박스에 폰트 적용
text_widget.configure(font=custom_font)

# 스크롤바 숨기기 (위젯은 사용하지만 UI에서는 보이지 않도록 설정)
text_widget.config(yscrollcommand=lambda f, l: None, xscrollcommand=lambda f, l: None)  # 스크롤 동작은 유지하되 UI에 표시하지 않음

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

# 폰트 크기 조정 함수
def increase_font_size():
    current_size = custom_font.cget("size")
    new_size = current_size + 2  # 2 포인트 증가
    custom_font.config(size=new_size)
    text_widget.configure(font=custom_font)

def decrease_font_size():
    current_size = custom_font.cget("size")
    new_size = max(8, current_size - 2)  # 최소 폰트 크기를 8로 설정
    custom_font.config(size=new_size)
    text_widget.configure(font=custom_font)

# 버튼 추가 (폰트 크기 조절)
font_size_frame = tk.Frame(root)
font_size_frame.pack(pady=10)

decrease_button = tk.Button(font_size_frame, text="폰트 작게", command=decrease_font_size)
decrease_button.pack(side=tk.LEFT, padx=10)

increase_button = tk.Button(font_size_frame, text="폰트 크게", command=increase_font_size)
increase_button.pack(side=tk.LEFT)


root.mainloop()
