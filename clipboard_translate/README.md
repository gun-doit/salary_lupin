## Clipboard Translator
이 프로그램은 클립보드에 있는 텍스트를 자동으로 감지하여, 해당 텍스트를 한국어로 번역하고, Tkinter GUI를 통해 사용자에게 보여줍니다. 또한, 폰트는 NanumGothic을 사용하여 번역된 텍스트를 보기 좋게 표시합니다.

## 기능
클립보드 감지: 사용자가 클립보드에 복사한 텍스트를 실시간으로 감지합니다.
자동 번역: 감지된 텍스트는 Google Translator API를 통해 자동으로 번역됩니다.
번역된 텍스트 출력: 번역된 텍스트가 GUI에 표시됩니다.
폰트: NanumGothic.ttf 폰트를 사용하여 텍스트를 표시합니다.
줄 간격: 텍스트 간 간격을 조정하여 보기 쉽게 만듭니다.
설치 및 실행
### 1. 필수 라이브러리 설치
이 프로그램을 실행하려면 Python에 다음과 같은 라이브러리가 필요합니다.

**bash**
복사
편집
pip install pyperclip deep-translator
### 2. 폰트 파일 준비
NanumGothic.ttf 폰트 파일이 필요합니다. 이 폰트를 프로그램의 실행 폴더에 배치하거나, 폰트 파일 경로를 코드에 맞게 설정합니다.

### 3. 실행 방법
스크립트를 실행하려면 아래와 같이 Python 환경에서 실행합니다.

**bash**
복사
편집
python translate.py
### 4. EXE 파일 실행
dist/*.exe
이 프로그램은 pyinstaller를 사용하여 EXE 파일로 변환할 수 있습니다. EXE 파일을 실행하려면, 먼저 spec 파일을 수정한 후 아래 명령어로 EXE 파일을 빌드합니다.

**bash**
복사
편집
pyinstaller --onefile clipboard_translator.spec
빌드 후 생성된 dist/clipboard_translator.exe 파일을 실행하여, 클립보드의 텍스트가 자동으로 번역되고 GUI에 표시되는 것을 확인할 수 있습니다.

## 기능 설명
### 1. 클립보드 감지
pyperclip 라이브러리를 사용하여 클립보드 내용을 1초마다 확인합니다.
클립보드에 새로운 텍스트가 복사되면, 이를 번역하여 GUI에 표시합니다.
### 2. 번역
deep-translator 라이브러리의 Google Translator API를 사용하여 자동으로 텍스트를 한국어로 번역합니다.
번역된 텍스트는 ScrolledText 위젯에 출력됩니다.
### 3. 폰트
프로그램 실행 시 NanumGothic.ttf 폰트를 사용하여 텍스트를 표시합니다.
Windows 환경에서 외부 폰트를 등록하기 위해 windll.gdi32.AddFontResourceExW를 사용하여 폰트를 등록합니다.
### 4. 줄 간격
텍스트 간의 간격을 조정하기 위해 text_widget.tag_configure("spacing", spacing1=10, spacing2=5, spacing3=10)을 사용하여 줄 간격을 설정합니다.

<<<<<<< HEAD
python
복사
편집
FONT_PATH = resource_path("NanumGothic.ttf")
클립보드 감지 및 번역

python
복사
편집
def check_clipboard():
    clipboard_text = pyperclip.paste()
    translated_text = translator.translate(clipboard_text)
GUI 구성

python
복사
편집
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
text_widget.configure(font=custom_font, padx=10, pady=10)
EXE 파일 변환 .spec 파일을 수정하여 폰트 파일을 포함시킵니다:

python
복사
편집
datas=[('NanumGothic.ttf', '.')]
파일 구성
translate.py: 메인 프로그램 파일.
NanumGothic.ttf: 프로그램에서 사용되는 폰트 파일.
clipboard_translator.spec: EXE 파일 빌드를 위한 설정 파일.
dist/clipboard_translator.exe: EXE 파일 (빌드 후 생성).
주의 사항
폰트 파일: NanumGothic.ttf 폰트 파일이 프로그램 폴더에 있어야 합니다.
클립보드 권한: 일부 운영 체제에서는 클립보드 접근 권한을 요구할 수 있습니다.
인터넷 연결: 번역을 위해 인터넷 연결이 필요합니다.

기여 방법
이 프로젝트는 오픈 소스로 제공됩니다. 사용자가 기능을 추가하거나 개선할 수 있습니다.

라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

pyinstaller --onefile --windowed --icon=logo.ico translate.py

pyinstaller --onefile --windowed --icon=logo.ico clipboard_translator.spec
=======
이 프로젝트는 오픈 소스로 제공됩니다.
이 프로젝트는 MIT 라이선스 하에 배포됩니다.
>>>>>>> 83296af91b0de6ba5146bd022f79edc74189209f
