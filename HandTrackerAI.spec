# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run_app.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('src/handtracker_ai/pngfortutor', 'handtracker_ai/pngfortutor'),
        ('venv/lib/python3.12/site-packages/mediapipe/modules', 'mediapipe/modules'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['pyinstaller_runtime_hook.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='HandTrackerAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='HandTrackerAI',
)
app = BUNDLE(
    coll,
    name='HandTrackerAI.app',
    icon=None,
    bundle_identifier='ai.handtracker.demo',
    info_plist={
        'NSCameraUsageDescription': 'HandTrackerAI uses the camera to detect hand gestures.',
        'NSAppleEventsUsageDescription': 'HandTrackerAI sends system events to control the cursor and media keys.',
    },
)
