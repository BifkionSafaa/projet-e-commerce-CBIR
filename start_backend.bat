@echo off
echo ========================================
echo   DEMARRAGE BACKEND FLASK
echo ========================================
cd backend
call .venv\Scripts\activate
echo Backend demarre sur http://localhost:5000
python app.py
pause




