@echo off
cd /d %~dp0

echo Activating venv...
call venv\Scripts\activate

echo Starting FastAPI...
start cmd /k "uvicorn backend.app.main:app --reload"

timeout /t 3

echo Starting Streamlit...
start cmd /k "streamlit run frontend/streamlit_app.py"

echo.
echo Project is running!
echo FastAPI: http://127.0.0.1:8000/docs
echo Streamlit: http://localhost:8501
pause