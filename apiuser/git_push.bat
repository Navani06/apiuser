@echo off

echo.
echo ========================================
echo    Git Setup Script -- User API
echo ========================================
echo.

echo [1] Initializing Git repository...
git init

echo.
echo [2] Setting default branch to main...
git branch -M main

echo.
echo [3] Staging all files...
git add .

echo.
echo [4] Creating first commit...
git commit -m "Initial commit: User API with FastAPI and SQLite"

echo.
echo ========================================
echo   Now link your GitHub repository
echo ========================================
echo.
echo  Go to: https://github.com/new
echo  - Repository name: user-api
echo  - Visibility: Public
echo  - Do NOT tick README or .gitignore
echo  - Click Create repository
echo.

set /p REPO_URL="Paste your GitHub repo URL here: "

if "%REPO_URL%"=="" (
    echo No URL entered. Exiting.
    exit /b 1
)

echo.
echo [5] Adding remote origin...
git remote add origin %REPO_URL%

echo.
echo [6] Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo  Done! Your code is now on GitHub.
echo  Visit: %REPO_URL%
echo ========================================
echo.
pause
