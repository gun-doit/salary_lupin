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
pip install pyperclip
pip install deep-translator
pip install pyinstaller
### 2. 폰트 파일 준비
NanumGothic.ttf 폰트 파일이 필요합니다. 이 폰트를 프로그램의 실행 폴더에 배치하거나, 폰트 파일 경로를 코드에 맞게 설정합니다.

### 3. 실행 방법
스크립트를 실행하려면 아래와 같이 Python 환경에서 실행합니다.

**bash**
복사
편집
python translate.py
4. EXE 파일 실행
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

이 프로젝트는 오픈 소스로 제공됩니다.
이 프로젝트는 MIT 라이선스 하에 배포됩니다.
