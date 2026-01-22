@echo off
echo ==========================================
echo    Creando Ejecutable (.exe)
echo ==========================================

if not exist "venv\Scripts\activate.bat" (
    echo Error: Primero ejecuta 'iniciar_app.bat' para configurar el entorno.
    pause
    exit /b
)

call venv\Scripts\activate

echo Instalando PyInstaller...
pip install pyinstaller

echo Generando ejecutable...
echo Esto puede tardar unos minutos.

pyinstaller --noconfirm --onefile --windowed ^
    --name "NumeradorArchivos" ^
    --add-data "renamer.py;." ^
    --hidden-import "pandas" ^
    --hidden-import "openpyxl" ^
    --collect-all "streamlit" ^
    --collect-all "pandas" ^
    --copy-metadata "streamlit" ^
    --copy-metadata "click" ^
    --copy-metadata "scipy" ^
    --copy-metadata "regex" ^
    --copy-metadata "sacremoses" ^
    --copy-metadata "requests" ^
    --copy-metadata "packaging" ^
    --copy-metadata "filelock" ^
    --copy-metadata "numpy" ^
    app.py

echo ==========================================
echo    PROCESO TERMINADO
echo ==========================================
echo El ejecutable se encuentra en la carpeta 'dist'.
pause
