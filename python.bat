@echo off
REM 設定 Miniconda 下載網址及安裝路徑
set MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
set INSTALL_DIR=C:\Users\%USERNAME%\miniconda3
set INSTALLER_PATH=%TEMP%\Miniconda3-latest-Windows-x86_64.exe

REM 設定最新 Python 下載網址
set PYTHON_URL=https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe
set PYTHON_INSTALLER_PATH=%TEMP%\python-3.12.1-amd64.exe

REM 從網路下載 Miniconda
echo Downloading Miniconda...
curl -L -o "%INSTALLER_PATH%" "%MINICONDA_URL%" >nul 2>&1
if exist "%INSTALLER_PATH%" (
    echo Miniconda Download success
) else (
    echo Miniconda Download failed
    exit /b 1
)

REM 安裝 Miniconda
echo Installing Miniconda...
"%INSTALLER_PATH%" /InstallationType=JustMe /RegisterPython=0 /AddToPath=0 /S /D=%INSTALL_DIR%

REM 檢查 Miniconda 安裝是否成功
if exist "%INSTALL_DIR%\condabin\conda.bat" (
    echo Miniconda Install success
) else (
    echo Miniconda Install failed
    exit /b 1
)

REM 將 Miniconda 添加到系統環境變數
echo Adding Miniconda to PATH...
setx PATH "%INSTALL_DIR%\condabin;%INSTALL_DIR%\Scripts;%INSTALL_DIR%\Library\bin;%PATH%"

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
