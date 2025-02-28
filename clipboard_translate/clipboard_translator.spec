import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# 현재 실행 경로를 가져옴
current_path = os.getcwd()

# 아이콘 파일 절대 경로 설정
icon_path = os.path.join(current_path, "logo.ico")

a = Analysis(
    ['translator.py'],  # ✅ 실행할 Python 파일
    pathex=['.'],
    binaries=[],
    datas=[('NanumGothic.ttf', '.')],  # ✅ 폰트 파일 포함
    hiddenimports=collect_submodules('deep_translator'),  # ✅ deep_translator 모듈 자동 포함
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='clipboard_translator',  # ✅ 실행 파일 이름
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # ✅ EXE 파일 크기 줄이기
    console=False,  # ✅ 터미널 창 없이 실행
    icon=icon_path,  # ✅ 아이콘 적용 (절대 경로)
)
