@echo off
setlocal EnableDelayedExpansion
REM Run this directory's tests using the IOC Testing Framework

SET CurrentDir=%~dp0

call "%~dp0..\..\..\..\config_env.bat"

set "PYTHONUNBUFFERED=1"

REM snmpsim needs HOMEPATH set and it seems to be missing when run in jenkins on some nodes
if "%HOMEPATH%" == "" (
    for %%F in ("%USERPROFILE%") do set HOMEPATH=%%~pnF
)

REM Command line arguments always passed to the test script
SET ARGS=--test_and_emulator %~dp0
"%PYTHON3%" -u "%EPICS_KIT_ROOT%\support\IocTestFramework\master\run_tests.py" %ARGS% %*
set errcode=!errorlevel!

REM errcode preserves errorlevel so not overwritten by taskkill
taskkill /IM snmpsim-command-responder.exe /F >NUL 2>&1

EXIT /b !errcode!
