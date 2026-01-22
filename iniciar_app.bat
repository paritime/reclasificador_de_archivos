@echo off
echo ==========================================
echo    Configurando Numerador de Archivos
echo ==========================================

REM Set encoding to UTF-8 to handle accented paths
set PYTHONUTF8=1

REM Check if venv exists and looks valid (checking for activate script)
if not exist "venv\Scripts\activate.bat" (
    echo Creando entorno virtual...
    py -m venv venv
)

echo Activando entorno virtual...
call venv\Scripts\activate

echo Actualizando pip...
python -m pip install --upgrade pip

echo Instalando dependencias...
pip install -r requirements.txt

echo ==========================================
echo    Iniciando Aplicacion...
echo ==========================================
streamlit run app.py

pause
