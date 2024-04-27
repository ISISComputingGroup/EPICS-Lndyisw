setlocal
call %~dp0..\..\..\..\config_env.bat
REM we cannot call use Scripts\snmpsim-command-responder.exe as it embeds path to build server within it when
REM generated and so fails on system tests server 
start "The SNMP Emulator" %PYTHON3% %~dp0responder.py --agent-udpv4-endpoint=127.0.0.1:161 --data-dir=%~dp0tests
