@echo off
cd /d "%~dp0\.."
maestro test .maestro --include-tags smoke
exit /b %ERRORLEVEL%
