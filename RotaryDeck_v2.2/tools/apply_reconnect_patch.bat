@echo off
cd /d "%~dp0"
if exist "..\companion\.venv\Scripts\python.exe" (
 "..\companion\.venv\Scripts\python.exe" apply_reconnect_patch.py %*
) else (
 py -3 apply_reconnect_patch.py %*
)
pause
