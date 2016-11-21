@echo off

cd %~dp0
C:\Python27\python.exe magic.py
if %ERRORLEVEL% NEQ 0 (
  pause
)