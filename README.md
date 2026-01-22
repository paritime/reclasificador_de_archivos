# Reclasificador_de_archivos
Pequeña aplicación desarrollada en python,para reclasificación de archivos en windows, con interfaz en streamlit.

Esta aplicación permite renombrar archivos masivamente basándose en un listado de Excel, o limpiar nombres de archivos eliminando prefijos numéricos. Es ideal para organizar documentos de forma automatizada.

## 🚀 Características

- **Numeración basada en Excel**: Asigna nombres a archivos en una carpeta siguiendo el orden y los nombres definidos en un archivo Excel.
- **Limpieza de nombres**: Elimina numeraciones anteriores o caracteres al inicio de los nombres de archivo.
- **Interfaz Gráfica**: Construida con Streamlit para un uso fácil e intuitivo.
- **Validación y Previsualización**: Muestra cómo quedarán los nombres antes de aplicar los cambios.

## 📋 Requisitos

Para ejecutar este proyecto en tu propia máquina, necesitas:

1.  **Python 3.8 o superior**: [Descargar aquí](https://www.python.org/downloads/).
2.  **Git** (opcional, para clonar el repositorio).

## 🛠️ Instalación

1.  **Clona este repositorio** o descarga los archivos en una carpeta.
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd "APP PARA NUMERAR ARCHIVOS"
    ```

2.  **Crea un entorno virtual** (recomendado para no afectar tu instalación global de Python):
    ```bash
    # En Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Instala las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Ejecución

Para iniciar la aplicación, ejecuta el siguiente comando en tu terminal dentro de la carpeta del proyecto:

```bash
streamlit run app.py
```

Esto abrirá la aplicación en tu navegador web predeterminado (usualmente en `http://localhost:8501`).

Alternativamente, puedes ejecutar el script lanzador:
```bash
python run_app.py
```

## ⚙️ Configuración y Uso

### 1. Numerar Archivos (Pestaña "Numerar Archivos")

Esta función toma los archivos de una carpeta y los renombra uno por uno según las filas de un Excel.

**Parámetros:**
- **Ruta de la Carpeta**: La ruta completa en tu PC donde están los archivos a renombrar (ej. `C:\Documentos\MisArchivos`).
- **Archivo Excel**: Sube un archivo `.xlsx`.
    - **Formato del Excel**: La aplicación leerá la **primera columna** de la primera hoja. Cada fila se usará como el nuevo prefijo/nombre para el archivo correspondiente.
- **Orden de los archivos originales**:
    - *Alfabético (A-Z)*: Ordena los archivos existentes por nombre antes de asignarles el nuevo nombre del Excel.
    - *Por Fecha*: Útil si quieres que el primer nombre del Excel se asigne al archivo más antiguo (o más nuevo).

**Identificación de parámetros en el código:**
Si necesitas cambiar cómo se leen los datos, revisa `renamer.py`:
- Función `get_mapping`: Aquí es donde se lee el Excel (`pd.read_excel`). Si tu Excel tiene encabezados o la columna de nombres no es la primera, modifica:
  ```python
  numerals = df.iloc[:, 0].dropna().astype(str).tolist()
  ```
  Cambia `0` por el índice de la columna deseada.

### 2. Limpiar Nombres (Pestaña "Limpiar Nombres")

Elimina prefijos no deseados de los archivos en una carpeta.

**Parámetros:**
- **Ruta de la Carpeta**: Ruta donde están los archivos.
- **Método**:
    - *Automático*: Usa una expresión regular para borrar números, puntos y espacios al inicio (ej. `01. Archivo.pdf` -> `Archivo.pdf`).
    - *Manual*: Borra una cantidad fija de caracteres (`N`) al inicio.

**Identificación de parámetros en el código:**
En `renamer.py`, función `get_cleaning_preview`:
- *Regex Automático*: `r'^[\d\s\.\-_]+'` (Línea ~159). Puedes modificar esta expresión regular si tus archivos tienen un patrón diferente.

## 🤝 Contribuyendo

Si deseas modificar el código:

1.  **Frontend (Interfaz)**: Edita `app.py`. Aquí puedes cambiar textos, colores, disposición de columnas y widgets.
2.  **Backend (Lógica)**: Edita `renamer.py`. Aquí reside la lógica de renombrado, lectura de directorios y procesamiento de Excel.

¡Tus contribuciones son bienvenidas!

