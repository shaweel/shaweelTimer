@echo off
setlocal enabledelayedexpansion

set "RED=[31m"
set "GREEN=[32m"
set "CYAN=[36m"
set "RESET=[0m"

echo %CYAN%--------------------------------%RESET%
echo %CYAN%Currently in start.bat%RESET%
echo %CYAN%--------------------------------%RESET%

where python3.14 >nul 2>&1
if errorlevel 1 (
    echo %RED%Install %CYAN%python3.14%RED% first.%RESET%
    exit /b
)
echo %CYAN%python3.14%GREEN% is installed. Good.%RESET%

if not exist ".venv\" (
    echo %CYAN%venv %RED%doesn't exist, %GREEN%creating.%RESET%
    python3.14 -m venv .venv
) else (
    echo %CYAN%venv %GREEN%exists. Good.%RESET%
)

.venv\Scripts\python -m pip list --outdated | findstr /i "pip" >nul 2>&1
if not errorlevel 1 (
    echo %CYAN%pip %RED%is outdated, %GREEN%updating.%RESET%
    .venv\Scripts\python -m pip install --upgrade pip
) else (
    echo %CYAN%pip %GREEN%is up to date. Good.%RESET%
)

.venv\Scripts\python -c "import gi" >nul 2>&1
if errorlevel 1 (
    echo %CYAN%PyGObject %RED%isn't installed in venv, %GREEN%installing.%RESET%
    .venv\Scripts\python -m pip install PyGObject
) else (
    echo %CYAN%PyGObject %GREEN%is installed in venv. Good.%RESET%
)

.venv\Scripts\python -m pip list --outdated | findstr /i "PyGObject" >nul 2>&1
if not errorlevel 1 (
    echo %CYAN%PyGObject %RED%is outdated, %GREEN%updating.%RESET%
    .venv\Scripts\python -m pip install --upgrade PyGObject
) else (
    echo %CYAN%PyGObject %GREEN%is up to date. Good.%RESET%
)

echo %GREEN%Everything should be ready. Running %CYAN%main.py.%RESET%
.venv\Scripts\python main.py