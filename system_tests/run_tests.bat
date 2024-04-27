@echo off
REM Run this directory's tests using the IOC Testing Framework

SET CurrentDir=%~dp0

call "%~dp0..\..\..\..\config_env.bat"

set "PYTHONUNBUFFERED=1"

REM Command line arguments always passed to the test script
SET ARGS=--test_and_emulator %~dp0
%PYTHON3% -u "%EPICS_KIT_ROOT%\support\IocTestFramework\master\run_tests.py" %ARGS% %*

REM preserve errorlevel so not overwritten by taskkill
set errcode=%errorlevel%

taskkill /IM snmpsim-command-responder.exe /F >NUL 2>&1

IF %errcode% NEQ 0 EXIT /b %errcode%
