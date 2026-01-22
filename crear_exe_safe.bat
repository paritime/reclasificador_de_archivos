@echo off
echo ==========================================
echo    Creando Ejecutable (Modo Seguro)
echo ==========================================

REM Define a unique temporary path for the environment
set "TEMP_VENV=%TEMP%\venv_renamer_build"

echo Usando entorno temporal en: %TEMP_VENV%

REM Clean up previous run if it exists
if exist "%TEMP_VENV%" (
    echo Limpiando entorno anterior...
    rmdir /s /q "%TEMP_VENV%"
)

echo Creando entorno virtual temporal...
py -m venv "%TEMP_VENV%"

echo Activando entorno...
call "%TEMP_VENV%\Scripts\activate"

echo Actualizando pip...
python -m pip install --upgrade pip

echo Instalando dependencias necesarias para el build...
pip install pyinstaller pandas openpyxl streamlit

echo Ejecutando pruebas de logica...
python test_cleaning_logic.py
if %errorlevel% neq 0 (
    echo Eliminando entorno temporal...
    call deactivate
    rmdir /s /q "%TEMP_VENV%"
    echo Error en las pruebas. Abortando.
    pause
    exit /b 1
)

echo Generando ejecutable...
echo Esto puede tardar unos minutos...

pyinstaller --noconfirm --onedir --windowed ^
    --name "NumeradorArchivos" ^
    --add-data "renamer.py;." ^
    --add-data "app.py;." ^
    --hidden-import "pandas" ^
    --hidden-import "openpyxl" ^
    --collect-all "streamlit" ^
    --collect-all "pandas" ^
    --copy-metadata "streamlit" ^
    --copy-metadata "click" ^
    --copy-metadata "requests" ^
    --copy-metadata "packaging" ^
    --copy-metadata "numpy" ^
    run_app.py

echo ==========================================
echo    LIMPIEZA
echo ==========================================
echo Desactivando entorno...
call deactivate

echo Eliminando entorno temporal (opcional, para ahorrar espacio)...
rmdir /s /q "%TEMP_VENV%"

echo ==========================================
echo PROCESO TERMINADO
echo ==========================================
echo La aplicacion ha sido creada en carpeta (modo onedir).
echo Ejecuta: dist\NumeradorArchivos\NumeradorArchivos.exe
pause
