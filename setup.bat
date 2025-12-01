@echo off
REM Employee Task Manager API - Windows Setup Script

echo ========================================
echo Employee Task Manager API - Setup
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Python found
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created. Please update it with your settings.
) else (
    echo .env file already exists
)
echo.

REM Create alembic versions directory
if not exist "alembic\versions" (
    mkdir alembic\versions
    echo Alembic versions directory created
)
echo.

echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Update .env file with your configuration
echo 3. Run migrations: alembic revision --autogenerate -m "Initial migration"
echo 4. Apply migrations: alembic upgrade head
echo 5. Populate sample data: python sample_data.py
echo 6. Populate default_user: python create_default_users.py
echo 7. Start the server: uvicorn main:app --reload
echo.
echo Happy coding!
echo.
pause