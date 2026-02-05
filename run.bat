@echo off 
title War Lightning - Console
:loop
py auf.py
if %errorlevel% NEQ 0 (
    echo An error occured.
    pause >nul
    exit /b 0
)
set /p key="Press Q to quit: "
if /i "%key%"=="Q" goto end
goto loop
:end
echo Exiting...
exit /b 0