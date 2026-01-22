import streamlit as st
import os
import renamer
import pandas as pd

st.set_page_config(page_title="Gestor de Archivos", page_icon="📂", layout="wide")

st.title("📂 Gestor de Archivos Masivo")

tab1, tab2 = st.tabs(["🔢 Numerar Archivos", "🧹 Limpiar Nombres"])

# ==========================================
# TAB 1: NUMERAR
# ==========================================
with tab1:
    st.header("Numerar Archivos desde Excel")
    st.markdown("""
    Asigna nombres a los archivos de una carpeta basándose en un Excel.
    """)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_dir = st.text_input("Ruta de la Carpeta (Numerar)", placeholder=r"C:\Usuarios\Documentos\MiCarpeta", key="num_dir")
    
    with col2:
        uploaded_file = st.file_uploader("Cargar Excel", type=["xlsx", "xls"], key="num_file")

    if uploaded_file and target_dir:
        st.subheader("Configuración")
        
        sort_option = st.radio(
            "Orden de los archivos originales:",
            ["Alfabético (A-Z)", "Por Fecha (Más antiguo primero)", "Por Fecha (Más nuevo primero)"],
            key="sort_opt"
        )
        
        sort_method = 'name'
        if "Más antiguo" in sort_option:
            sort_method = 'date_asc'
        elif "Más nuevo" in sort_option:
            sort_method = 'date_desc'

        if os.path.isdir(target_dir):
            st.divider()
            st.subheader("Vista Previa")
            
            try:
                uploaded_file.seek(0)
                result = renamer.get_mapping(target_dir, uploaded_file, sort_method)
                
                if result["status"] == "success":
                    c1, c2 = st.columns(2)
                    c1.metric("Archivos", result["files_count"])
                    c2.metric("Filas Excel", result["numerals_count"])
                    
                    df_preview = pd.DataFrame(result["mapping"])
                    st.dataframe(df_preview, use_container_width=True, height=300)
                    
                    st.warning("⚠️ Verifica que el orden coincida antes de ejecutar.")

                    if st.button("✅ Ejecutar Numeración", type="primary", use_container_width=True, key="btn_num"):
                        with st.spinner("Procesando..."):
                            uploaded_file.seek(0)
                            final = renamer.rename_files(target_dir, uploaded_file, sort_method)
                        
                        if final["status"] == "success":
                            st.success(f"Renombrados: {final['renamed_count']}")
                            if final['renamed_count'] > 0:
                                st.balloons()
                            with st.expander("Ver Detalles"):
                                for line in final["log"]:
                                    st.text(line)
                        else:
                            st.error(final.get("message"))
                else:
                    st.error(result.get("message"))
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Carpeta no encontrada.")

# ==========================================
# TAB 2: LIMPIAR
# ==========================================
with tab2:
    st.header("Limpiar Nombres de Archivos")
    st.markdown("""
    Elimina números o caracteres al inicio de los nombres de archivo en una carpeta.
    **Útil para deshacer numeraciones anteriores.**
    """)
    
    st.divider()
    
    clean_dir = st.text_input("Ruta de la Carpeta a Limpiar", placeholder=r"C:\Usuarios\Documentos\MiCarpeta", key="clean_dir")
    
    if clean_dir:
        if os.path.isdir(clean_dir):
            st.subheader("Configuración")
            
            method_label = st.radio(
                "Método de Limpieza",
                ["Automático (Eliminar números y símbolos iniciales)", "Manual (Eliminar N primeros caracteres)"],
                key="clean_method"
            )
            
            clean_method_code = 'auto_pattern'
            params = {}
            
            if "Manual" in method_label:
                clean_method_code = 'remove_n'
                n_chars = st.number_input("Cantidad de caracteres a borrar", min_value=1, value=3, step=1)
                params['n'] = n_chars
                st.info(f"Se borrarán los primeros {n_chars} caracteres de cada nombre.")
            else:
                st.info("Se borrarán números, espacios, puntos y guiones al inicio (ej: '01. Foto' -> 'Foto').")
            
            st.divider()
            st.subheader("Vista Previa")
            
            preview = renamer.get_cleaning_preview(clean_dir, clean_method_code, params)
            
            if preview["status"] == "success":
                df_clean = pd.DataFrame(preview["mapping"])
                
                # Highlight changes style?
                st.dataframe(df_clean, use_container_width=True, height=300)
                
                st.warning("⚠️ Esta acción modificará los nombres de los archivos reales.")
                
                col_act1, col_act2 = st.columns([1, 2])
                with col_act1:
                    if st.button("🚨 Ejecutar Limpieza", type="primary", use_container_width=True, key="btn_clean"):
                        with st.spinner("Limpiando nombres..."):
                            res = renamer.execute_cleaning(clean_dir, preview["mapping"])
                        
                        if res["status"] == "success":
                            st.success(f"Listo. Renombrados: {res['renamed_count']}")
                            if res['renamed_count'] > 0:
                                st.balloons()
                            with st.expander("Ver Detalles"):
                                for line in res["log"]:
                                    st.text(line)
                        else:
                            st.error("Ocurrió un error en la ejecución.")
            else:
                st.error(preview["message"])
        else:
            st.warning("La carpeta no existe.")
