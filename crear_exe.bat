@echo off
echo ==========================================
echo    Creando Ejecutable (.exe) - Modo Seguro
echo ==========================================
echo Solucionando error de rutas largas (Windows Long Path)...
echo.

REM 1. Definir ruta temporal corta para el entorno
set "TEMP_DIR=%TEMP%\build_renamer_temp"
set "CURRENT_DIR=%CD%"

echo Directrio de trabajo temporal: %TEMP_DIR%

if exist "%TEMP_DIR%" (
    echo Limpiando archivos temporales previos...
    rmdir /s /q "%TEMP_DIR%"
)
mkdir "%TEMP_DIR%"

REM 2. Copiar archivos necesarios a la carpeta temporal
echo Copiando archivos del proyecto...
copy "app.py" "%TEMP_DIR%\" >nul
copy "renamer.py" "%TEMP_DIR%\" >nul
copy "run_app.py" "%TEMP_DIR%\" >nul
copy "requirements.txt" "%TEMP_DIR%\" >nul

REM 3. Crear entorno virtual en la carpeta temporal (ruta corta)
echo.
echo Creando entorno virtual temporal...
py -m venv "%TEMP_DIR%\venv"

REM 4. Activar e instalar
echo Activando entorno e instalando librerias...
call "%TEMP_DIR%\venv\Scripts\activate"
py -m pip install --upgrade pip
pip install -r "%TEMP_DIR%\requirements.txt"
pip install pyinstaller

REM 5. Generar EXE
echo.
echo Generando ejecutable (esto tomara unos minutos)...
cd /d "%TEMP_DIR%"

pyinstaller --noconfirm --onefile --windowed ^
    --name "NumeradorArchivos" ^
    --add-data "app.py;." ^
    --add-data "renamer.py;." ^
    --hidden-import "pandas" ^
    --hidden-import "openpyxl" ^
    --collect-all "streamlit" ^
    --collect-all "pandas" ^
    --copy-metadata "streamlit" ^
    --copy-metadata "click" ^
    --copy-metadata "requests" ^
    --copy-metadata "packaging" ^
    run_app.py

REM 6. Mover el resultado a la carpeta original
echo.
echo Moviendo ejecutable a la carpeta de origen...
cd /d "%CURRENT_DIR%"
if not exist "dist" mkdir "dist"

move /Y "%TEMP_DIR%\dist\NumeradorArchivos.exe" "dist\NumeradorArchivos.exe"

REM 7. Limpieza
echo Limpiando archivos temporales...
rmdir /s /q "%TEMP_DIR%"

echo.
echo ==========================================
echo    PROCESO TERMINADO CON EXITO
echo ==========================================
echo El archivo se encuentra en: dist\NumeradorArchivos.exe
pause
