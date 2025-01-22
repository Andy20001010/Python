@echo off
:: 設置 Python 環境建置批次檔案

:: 定義變數
set PYTHON_VERSION=3.11.6
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
set DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%
set INSTALL_PATH=C:\Python%PYTHON_VERSION%
set VENV_NAME=venv

:: 檢查 Python 是否已安裝
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed. Downloading Python %PYTHON_VERSION%...
    
    :: 下載 Python 安裝檔案
    curl -o %PYTHON_INSTALLER% %DOWNLOAD_URL%
    if %ERRORLEVEL% neq 0 (
        echo Failed to download Python installer. Please check your internet connection.
        pause
        exit /b
    )
    
    :: 安裝 Python
    echo Installing Python...
    start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 TargetDir=%INSTALL_PATH%
    if %ERRORLEVEL% neq 0 (
        echo Python installation failed.
        pause
        exit /b
    )
    echo Python installed successfully.
)

:: 檢查 Python 是否正確安裝
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python installation was not successful. Please check manually.
    pause
    exit /b
)

:: 設置環境變數（如果需要手動添加）
echo Adding Python to PATH...
setx PATH "%INSTALL_PATH%;%INSTALL_PATH%\Scripts;%PATH%" /M

:: 創建並啟用虛擬環境
if not exist %VENV_NAME% (
    echo Creating virtual environment...
    python -m venv %VENV_NAME%
)

echo Activating virtual environment...
call %VENV_NAME%\Scripts\activate

:: 確保 pip 已更新
echo Upgrading pip...
python -m pip install --upgrade pip

:: 安裝必要套件
echo Installing required packages...
pip install numpy pandas matplotlib

:: 清理下載的安裝檔案
if exist %PYTHON_INSTALLER% (
    del /f %PYTHON_INSTALLER%
)

:: 顯示完成訊息
echo Python environment setup is complete.
pause
