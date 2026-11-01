@echo off
cd /d "%~dp0\.."
maestro test .maestro
exit /b %ERRORLEVEL%
