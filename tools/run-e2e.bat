@echo off
cd /d "%~dp0\.."
maestro test .maestro --include-tags e2e
exit /b %ERRORLEVEL%
