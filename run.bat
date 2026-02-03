@echo off 
title War Lightning - Console
py main.py
if %errorlevel% NEQ 0 (
    echo An error occured.
    pause >nul
)
exit \b 0