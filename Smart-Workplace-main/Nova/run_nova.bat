@echo off
echo Starting Nova AI Assistant...

REM Start Nova with the clean flag to kill any existing processes
echo Starting Nova...
start python nova.py --clean

echo Nova has been started in a new window.
echo You can close this window now.
timeout /t 3 