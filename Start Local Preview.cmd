@echo off
setlocal
cd /d "%~dp0"
title KhiangteVillain local preview

where py >nul 2>nul
if not errorlevel 1 goto use_py

where python >nul 2>nul
if not errorlevel 1 goto use_python

echo.
echo Python was not found on this computer.
echo Install Python, then run this file again.
pause
exit /b 1

:use_py
start "" /b py -3 -m http.server 4175 --bind 127.0.0.1
goto open_preview

:use_python
start "" /b python -m http.server 4175 --bind 127.0.0.1

:open_preview
echo Starting the preview...
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:4175/"
echo.
echo Preview is running. Keep this window open while you review the site.
pause
goto finished

:finished
