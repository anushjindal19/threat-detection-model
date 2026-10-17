@echo off
REM ============================================================
REM  setup.bat
REM  One-click local environment setup for the
REM  Lightweight Cybersecurity Threat Detector project.
REM
REM  What this script does, in plain English:
REM    1. Checks whether Git is installed. If not, it tells you
REM       where to download it (it cannot safely install Git
REM       silently without your confirmation).
REM    2. Checks whether Python is installed. If not, it tries
REM       to install it using "winget" (built into Windows 10/11).
REM    3. Creates a "virtual environment" folder called .venv —
REM       this is just an isolated folder that keeps this
REM       project's Python packages separate from everything
REM       else on your PC.
REM    4. Installs every package listed in requirements.txt
REM       into that virtual environment.
REM    5. Initializes this folder as a Git repository (if it
REM       isn't one already) and makes a first commit.
REM
REM  You do NOT need any of this to use Google Colab — Colab
REM  runs in the browser and needs nothing installed locally.
REM  This script is for running things on YOUR OWN PC later
REM  (e.g. the resource-benchmarking stage), and so Git works
REM  from this folder.
REM
REM  How to run this file:
REM    Double-click it in File Explorer, OR open a terminal in
REM    this folder and type:  setup.bat
REM ============================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ================================================
echo  Lightweight Cybersecurity Threat Detector setup
echo ================================================
echo.

REM ---------------------------------------------------------
REM 1. Check for Git
REM ---------------------------------------------------------
echo [1/5] Checking for Git...
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo   Git was NOT found on this PC.
    echo   Please install it manually from the official site:
    echo       https://git-scm.com/downloads
    echo   During install, the default options are fine for beginners.
    echo   After installing, close this window and run setup.bat again.
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%v in ('git --version') do echo   Found: %%v
)

REM ---------------------------------------------------------
REM 2. Check for Python
REM ---------------------------------------------------------
echo.
echo [2/5] Checking for Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo   Python was NOT found. Attempting to install it with winget...
    winget --version >nul 2>nul
    if %errorlevel% neq 0 (
        echo.
        echo   winget is not available either. Please install Python manually:
        echo       https://www.python.org/downloads/
        echo   IMPORTANT: on the first install screen, tick the box that says
        echo   "Add python.exe to PATH" before clicking Install.
        echo   After installing, close this window and run setup.bat again.
        echo.
        pause
        exit /b 1
    )
    winget install --id Python.Python.3.11 -e --source winget
    echo   Python installed. Please CLOSE this window and re-run setup.bat
    echo   so Windows picks up the new PATH.
    pause
    exit /b 0
) else (
    for /f "tokens=*" %%v in ('python --version') do echo   Found: %%v
)

REM ---------------------------------------------------------
REM 3. Create the virtual environment
REM ---------------------------------------------------------
echo.
echo [3/5] Creating virtual environment in .venv ...
if exist ".venv\Scripts\python.exe" (
    echo   .venv already exists — skipping creation.
) else (
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo   ERROR: Failed to create the virtual environment. See message above.
        pause
        exit /b 1
    )
    echo   Created .venv
)

REM ---------------------------------------------------------
REM 4. Install requirements
REM ---------------------------------------------------------
echo.
echo [4/5] Installing packages from requirements.txt ...
call ".venv\Scripts\python.exe" -m pip install --upgrade pip
call ".venv\Scripts\python.exe" -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo   ERROR: pip install failed. Scroll up to see which package failed.
    pause
    exit /b 1
)
echo   All packages installed successfully.

REM ---------------------------------------------------------
REM 5. Initialize Git repository
REM ---------------------------------------------------------
echo.
echo [5/5] Setting up the local Git repository...
if exist ".git" (
    echo   This folder is already a Git repository — skipping "git init".
) else (
    git init
    git add .
    git commit -m "Initial project setup: folder structure, guides, requirements"
    echo   Git repository created with a first commit.
)

echo.
echo ================================================
echo  Setup complete!
echo ================================================
echo.
echo  Next steps (see SETUP_GUIDE.md for full detail):
echo    1. Create an empty repository on https://github.com/new
echo       (do NOT check "Add a README" — this folder already has one)
echo    2. Copy the repository URL GitHub gives you, then run:
echo         git remote add origin PASTE_URL_HERE
echo         git branch -M main
echo         git push -u origin main
echo    3. Open Google Colab (https://colab.research.google.com) and
echo       open notebooks/01_dataset_exploration.ipynb from GitHub.
echo.
echo  To use the virtual environment later in a terminal, run:
echo         .venv\Scripts\activate
echo.
pause
