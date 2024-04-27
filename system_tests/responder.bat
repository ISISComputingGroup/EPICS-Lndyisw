setlocal
call %~dp0..\..\..\..\config_env.bat
start "The SNMP Emulator" %PYTHON3DIR%\Scripts\snmpsim-command-responder.exe --agent-udpv4-endpoint=127.0.0.1:161 --data-dir=%~dp0tests
