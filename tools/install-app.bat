@echo off
setlocal
if "%~1"=="" (
  echo Usage: install-app.bat path\to\staging.apk
  exit /b 1
)
adb install -r "%~1"
exit /b %ERRORLEVEL%
