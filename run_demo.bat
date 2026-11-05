@echo off
setlocal
cd /d "%~dp0"

if not exist venv (
    python -m venv venv
    if errorlevel 1 (
        echo Could not create virtual environment. Check that Python is installed.
        pause
        exit /b 1
    )
)

call venv\Scripts\activate
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
)

start "WebGuard Practice Lab" cmd /k "cd /d ""%~dp0"" && call venv\Scripts\activate && python practice_lab.py"
start "WebGuard Server" cmd /k "cd /d ""%~dp0"" && call venv\Scripts\activate && python app.py"

timeout /t 3 >nul
start "" http://127.0.0.1:5000
echo.
echo WebGuard is running at http://127.0.0.1:5000
echo Keep the server and practice-lab windows open while using the demo.
echo Close those windows or press Ctrl+C in them to stop the services.
pause
