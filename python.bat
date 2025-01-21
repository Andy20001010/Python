@echo off
REM 設定 Miniconda 下載網址及安裝路徑
set MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
set INSTALL_DIR=C:\Users\%USERNAME%\miniconda3
set INSTALLER_PATH=%TEMP%\Miniconda3-latest-Windows-x86_64.exe

REM 從網路下載 Miniconda
echo Dowmloading Miniconda...
curl -L -o "%INSTALLER_PATH%" "%MINICONDA_URL%" >nul 2>&1
if exist "%INSTALLER_PATH%" (
    echo Miniconda Download sucess
) else (
    echo Miniconda Download failed
    exit /b 1
)

REM 安裝 Miniconda
echo Installing Miniconda...
"%INSTALLER_PATH%" /InstallationType=JustMe /RegisterPython=0 /AddToPath=0 /S /D=%INSTALL_DIR%

REM 檢查安裝是否成功
if exist "%INSTALL_DIR%\condabin\conda.bat" (
    echo Miniconda Install sucess
) else (
    echo Miniconda Install failed
    exit /b 1
)

REM 將 Miniconda 添加到系統環境變數
echo Add Miniconda to PATH...
setx PATH "%INSTALL_DIR%\condabin;%INSTALL_DIR%\Scripts;%INSTALL_DIR%\Library\bin;%PATH%"

echo Restart CMD!
pause
