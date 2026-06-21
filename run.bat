@echo off
cd /d %~dp0

echo Checking virtual environment...

IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv

    call venv\Scripts\activate

    echo Installing dependencies...
    pip install -r requirements.txt
) ELSE (
    echo Using existing virtual environment...
    call venv\Scripts\activate
)

echo Starting FastAPI...
start cmd /k "uvicorn backend.app.main:app --reload"

timeout /t 3 > nul

echo Starting Streamlit...
start cmd /k "streamlit run frontend/streamlit_app.py"

echo.
echo Project is running!
echo FastAPI: http://127.0.0.1:8000/docs
echo Streamlit: http://localhost:8501

pause