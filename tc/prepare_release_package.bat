@echo off
cls

Echo Prepare release package v1.0.0


REM get this script's path
set SCRIPT_PATH=%~dp0
echo Script path: %SCRIPT_PATH%

REM get project's root directory (2 levels above this script's path)
for %%a in (%SCRIPT_PATH:~0,-1%) do set "ROOT_PATH=%%~dpa"
REM remove trailing slash (last \)
set ROOT_PATH=%ROOT_PATH:~0,-1%
echo Root path: %ROOT_PATH%


REM Call Python script
set PY_SCRIPT=prepare_release_package.py
set PYTHON_EXE=%ROOT_PATH%\.venv\Scripts\python.exe
%PYTHON_EXE% %SCRIPT_PATH%\scripts\%PY_SCRIPT%