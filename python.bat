@echo off
REM 設定最新 Python 下載網址
set PYTHON_URL=https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe
set PYTHON_INSTALLER_PATH=%TEMP%\python-3.12.1-amd64.exe

REM 從網路下載最新的 Python
echo Downloading Python...
curl -L -o "%PYTHON_INSTALLER_PATH%" "%PYTHON_URL%" >nul 2>&1
if exist "%PYTHON_INSTALLER_PATH%" (
    echo Python Download success
) else (
    echo Python Download failed
    exit /b 1
)

REM 安裝 Python
echo Installing Python...
"%PYTHON_INSTALLER_PATH%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM 檢查 Python 安裝是否成功
where python >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Python Install success
    python --version
) else (
    echo Python Install failed
    exit /b 1
)

echo Installation complete. Please restart CMD!
pause
