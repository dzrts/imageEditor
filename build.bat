@echo off
cd /d "%~dp0"

echo ============================================
echo        Building imageEditor Portable EXE
echo ============================================
echo.

REM ====== 1. Create / Update Micromamba Environment ======
if exist ".\.mamba_env\conda-meta" (
    echo Environment already exists, updating packages...
    tools\micromamba.exe update -y --prefix .\.mamba_env --all
) else (
    echo Creating environment...
    tools\micromamba.exe create -y --prefix .\.mamba_env -f environment.yml
)

if %errorlevel% neq 0 (
    echo [ERROR] Micromamba environment creation failed.
    exit /b 1
)


echo.
echo === Environment ready. ===
echo.

REM ====== 2. Install PyInstaller inside the environment ======
tools\micromamba.exe run -p .\.mamba_env pip install pyinstaller

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install PyInstaller.
    exit /b 1
)

echo.
echo === PyInstaller installed. ===
echo.

REM ====== 3. Build executable ======
tools\micromamba.exe run -p .\.mamba_env pyinstaller ^
    src\imageEditor\main.py ^
    --name imageEditor ^
    --clean ^
    --noconsole ^
    --onedir ^
    --additional-hooks-dir pyinstaller

if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller build failed.
    exit /b 1
)

echo.
echo === PyInstaller build OK. ===
echo.

REM ====== 4. Copy OpenImageIO DLLs to dist folder ======
echo Copying required OIIO DLLs...
xcopy /Y /Q ".\.mamba_env\Library\bin\*.dll" "dist\imageEditor\"

echo.
echo ============================================
echo      BUILD COMPLETE - imageEditor.exe READY
echo ============================================
pause
