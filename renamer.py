import os
import pandas as pd
import shutil
import re
import time

def get_files_in_directory(directory_path, sort_method='name'):
    """
    Returns a sorted list of files in the directory.
    Ignores hidden files and directories.
    sort_method: 'name', 'date_asc', 'date_desc'
    """
    try:
        # Get all entries
        with os.scandir(directory_path) as entries:
            files = [e for e in entries if e.is_file()]
            
        # Filter hidden/temp
        files = [f for f in files if not f.name.startswith('~$') and not f.name.startswith('.')]
        
        # Sort
        if sort_method == 'name':
            files.sort(key=lambda f: f.name.lower())
        elif sort_method == 'date_asc':
            files.sort(key=lambda f: f.stat().st_mtime)
        elif sort_method == 'date_desc':
            files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            
        return [f.name for f in files]
    except Exception as e:
        raise Exception(f"Error accessing directory: {e}")

def get_mapping(directory_path, excel_file, sort_method='name'):
    """
    Returns a list of dictionaries with the proposed renaming mapping.
    """
    try:
        df = pd.read_excel(excel_file, dtype=str)
    except Exception as e:
        raise Exception(f"Error reading Excel file: {e}")

    files = get_files_in_directory(directory_path, sort_method)
    
    if len(files) == 0:
        return {"status": "error", "message": "No files found in the directory."}
    
    numerals = df.iloc[:, 0].dropna().astype(str).tolist()
    
    mapping = []
    
    for i, file_name in enumerate(files):
        item = {
            "Original": file_name,
            "Nuevo Nombre": "",
            "Estado": "Pendiente"
        }
        
        if i < len(numerals):
            numeral = numerals[i].strip()
            # Clean numeral
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                numeral = numeral.replace(char, '_')
                
            name, ext = os.path.splitext(file_name)
            new_name = f"{numeral} - {name}{ext}"
            item["Nuevo Nombre"] = new_name
        else:
            item["Estado"] = "Sin Numeral (No se cambiará)"
            
        mapping.append(item)
        
    return {"status": "success", "mapping": mapping, "files_count": len(files), "numerals_count": len(numerals)}

def rename_files(directory_path, excel_file, sort_method='name', dry_run=False):
    """
    Renames files in directory_path based on the first column of excel_file.
    Returns a log of changes.
    """
    # Get mapping first
    mapping_result = get_mapping(directory_path, excel_file, sort_method)
    
    if mapping_result["status"] == "error":
        return mapping_result

    mapping = mapping_result["mapping"]
    full_log = []
    count = 0
    errors = 0
    
    full_log.append(f"Iniciando proceso. Archivos: {mapping_result['files_count']}, Numerales: {mapping_result['numerals_count']}")

    for item in mapping:
        old_name = item["Original"]
        new_name = item["Nuevo Nombre"]
        
        if not new_name:
            full_log.append(f"Saltado: '{old_name}' (Sin numeral asignado)")
            continue
            
        old_path = os.path.join(directory_path, old_name)
        new_path = os.path.join(directory_path, new_name)
        
        if old_path == new_path:
            full_log.append(f"Saltado: {old_name} (Ya tiene el nombre correcto)")
            continue

        if dry_run:
            full_log.append(f"Simulacion: Renombrar '{old_name}' a '{new_name}'")
        else:
            try:
                os.rename(old_path, new_path)
                full_log.append(f"Exito: '{old_name}' -> '{new_name}'")
                count += 1
            except Exception as e:
                full_log.append(f"Error '{old_name}': {e}")
                errors += 1
                
    return {
        "status": "success",
        "renamed_count": count,
        "error_count": errors,
        "log": full_log
    }

def get_cleaning_preview(directory_path, method, params=None):
    """
    Generates a preview of file renaming for cleaning purposes.
    method: 'remove_n' or 'auto_pattern'
    params: dict, e.g., {'n': 5}
    """
    try:
        if not os.path.exists(directory_path):
             return {"status": "error", "message": "Directorio no encontrado."}

        files = get_files_in_directory(directory_path, sort_method='name')
        if not files:
             return {"status": "error", "message": "No hay archivos en el directorio."}

        mapping = []
        seen_names = {} # To handle collisions: new_name -> count

        for file_name in files:
            original_name = file_name
            name_root, ext = os.path.splitext(file_name)
            new_name_root = name_root

            if method == 'remove_n':
                n = params.get('n', 0)
                if len(name_root) > n:
                    new_name_root = name_root[n:].strip()
                else:
                    new_name_root = name_root # Safety: don't make empty if too short

            elif method == 'auto_pattern':
                # Remove leading numbers, spaces, dots, dashes
                # Regex: ^[\d\s\.\-_]+
                # Example: "01. File" -> "File", "1 - File" -> "File"
                new_name_root = re.sub(r'^[\d\s\.\-_]+', '', name_root).strip()
            
            # Safety: If empty name results, revert to original or placeholder
            if not new_name_root:
                new_name_root = "SinNombre"

            new_full_name = f"{new_name_root}{ext}"
            
            # Handle Collisions (e.g. 01.File.txt and 02.File.txt -> File.txt)
            if new_full_name in seen_names:
                seen_names[new_full_name] += 1
                count = seen_names[new_full_name]
                new_full_name = f"{new_name_root}_{count}{ext}"
            else:
                seen_names[new_full_name] = 0

            item = {
                "Original": original_name,
                "Nuevo Nombre": new_full_name,
                "Estado": "Listo" if original_name != new_full_name else "Sin Cambios"
            }
            mapping.append(item)

        return {"status": "success", "mapping": mapping, "files_count": len(files)}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def execute_cleaning(directory_path, mapping_data):
    """
    Executes the renaming based on the preview mapping.
    """
    log = []
    renamed_count = 0
    error_count = 0
    
    log.append(f"Iniciando limpieza en: {directory_path}")
    
    for item in mapping_data:
        old_name = item["Original"]
        new_name = item["Nuevo Nombre"]
        
        if old_name == new_name:
            continue
            
        old_path = os.path.join(directory_path, old_name)
        new_path = os.path.join(directory_path, new_name)
        
        try:
            if os.path.exists(new_path):
                log.append(f"Error: Destino ya existe '{new_name}'. Saltado.")
                error_count += 1
                continue
                
            os.rename(old_path, new_path)
            log.append(f"Renombrado: '{old_name}' -> '{new_name}'")
            renamed_count += 1
        except Exception as e:
            log.append(f"Error al renombrar '{old_name}': {e}")
            error_count += 1
            
    return {
        "status": "success",
        "renamed_count": renamed_count,
        "error_count": error_count,
        "log": log
    }
