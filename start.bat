@echo off
for /f "delims=" %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"

set "RED=%ESC%[31m"
set "GREEN=%ESC%[32m"
set "CYAN=%ESC%[36m"
set "RESET=%ESC%[0m"
set "APOS='"

echo %CYAN%--------------------------------%RESET%
echo %CYAN%Currently in start.bat%RESET%
echo %CYAN%--------------------------------%RESET%

reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\MSYS2" >nul 2>&1if errorlevel 1 (
	echo %CYAN%MSYS2%RED% isn%APOS%t installed. %GREEN%Installing using %CYAN%winget.%RESET%
	winget install MSYS2.MSYS2
) else (
	echo %CYAN%MSYS2 %GREEN%is installed. Good.%RESET%
)

echo %GREEN%Installing %CYAN%dependencies...%RESET%
C:\msys64\usr\bin\bash -lc "pacman -S --noconfirm --needed mingw-w64-x86_64-python-gobject mingw-w64-x86_64-gtk4 mingw-w64-x86_64-libadwaita"
echo %GREEN%Everything should be ready. Running %CYAN%main.py.%RESET%
C:\msys64\usr\bin\bash -lc "cd '%~dp0' && /mingw64/bin/python main.py"
pause