@echo off

echo Building environment - Python generic v1.0.0

REM get this script's path
set SCRIPT_PATH=%~dp0
echo Script path: %SCRIPT_PATH%

REM get project's root directory (2 levels above this script's path)
for %%a in (%SCRIPT_PATH:~0,-1%) do set "ROOT_PATH=%%~dpa"
REM remove trailing slash (last \)
set ROOT_PATH=%ROOT_PATH:~0,-1%
echo Root path: %ROOT_PATH%

echo Deleting old venv...
REM rmdir: delete directory; /S: also delete directory's content; /Q: Quiet mode, do not ask if ok to remove directory
rmdir %ROOT_PATH%\.venv /S /Q

echo Building new environment...
python -m virtualenv --no-download %ROOT_PATH%\.venv\
set PYTHON_EXE=%ROOT_PATH%\.venv\Scripts\python.exe
set PROXY=custom_proxy

set INTERNAL_PYPI_SERVER=--trusted-host private_pypi_server_host --index-url private_pypi_server _url --extra-index-url https://pypi.python.org/simple


REM It is a good practice to use latest version of PIP
echo Updating PIP tool...
%PYTHON_EXE% -m pip install -U pip --proxy=%PROXY%

REM It is a good practice to use latest version of setuptools
echo Updating setuptools...
%PYTHON_EXE% -m pip install -U setuptools --proxy=%PROXY%

echo Installing project requirements...
%PYTHON_EXE% -m pip install -r %ROOT_PATH%\requirements.txt --proxy=%PROXY% %INTERNAL_PYPI_SERVER%

echo Installing project development requirements...
%PYTHON_EXE% -m pip install -r %ROOT_PATH%\requirements_develop.txt --proxy=%PROXY% %INTERNAL_PYPI_SERVER%

echo Installing PyInstaller from local whl...
%PYTHON_EXE% -m pip install %ROOT_PATH%\tc\whls\PyInstaller-3.5-py2.py3-none-any.whl --proxy %PROXY%
if %errorlevel% exit %errorlevel%
