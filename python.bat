@echo off
:: Simplified Python Setup Script (No Administrator Required)
:: Define variables
set PYTHON_VERSION=3.12.8
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
set DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%
set INSTALL_PATH=%USERPROFILE%\Python%PYTHON_VERSION%

:: Step 1: Download Python installer
echo Downloading Python %PYTHON_VERSION% installer...
curl -o %PYTHON_INSTALLER% %DOWNLOAD_URL%
if %ERRORLEVEL% neq 0 (
    echo Failed to download Python installer. Please check your internet connection.
    pause
    exit /b
)
echo Python installer downloaded successfully.

:: Step 2: Install Python and add to PATH
echo Installing Python to user-specific directory...
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=0 PrependPath=0 TargetDir=%INSTALL_PATH%
if %ERRORLEVEL% neq 0 (
    echo Python installation failed.
    pause
    exit /b
)
echo Python installed successfully.

:: Step 3: Update user-specific PATH
echo Setting up environment variables for current user...
set PYTHON_USER_PATH=%INSTALL_PATH%;%INSTALL_PATH%\Scripts;
setx PATH "%PYTHON_USER_PATH%%PATH%"
if %ERRORLEVEL% neq 0 (
    echo Failed to update user PATH. Please check manually.
    pause
    exit /b
)
echo Environment variables updated successfully for current user.

:: Cleanup: Remove installer file
if exist %PYTHON_INSTALLER% (
    del /f %PYTHON_INSTALLER%
    echo Cleaned up installer file.
)

:: Finish
echo Python setup is complete. You can now use Python.
pause
