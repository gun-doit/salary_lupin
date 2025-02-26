# clipboard_translator.spec 파일
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['translate.py'],
    pathex=['.'],
    binaries=[],
    datas=[('NanumGothic.ttf', '.')],  # ✅ 폰트 파일 포함
    hiddenimports=[],
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
    name='clipboard_translator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=None,  # 실행 파일 아이콘을 설정하려면 여기에 .ico 파일을 지정
)
