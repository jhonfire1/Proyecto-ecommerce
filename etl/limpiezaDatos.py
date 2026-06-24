import pandas as pd
import logging
from datetime import datetime
import os

# Configuración de logging profesional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def aplicar_transformaciones(ruta_entrada: str, ruta_salida: str) -> None:
    try:
        logging.info(f"Iniciando transformación. Cargando datos desde {ruta_entrada}")
        df = pd.read_csv(ruta_entrada)
        filas_iniciales = len(df)

        # 1. Eliminar filas duplicadas
        df = df.drop_duplicates()
        logging.info("Duplicados eliminados.")

        # 2. Eliminar columnas redundantes (Defensa preventiva)
        # Si durante tu merge quedaron columnas como id_usuario_y, las eliminamos
        columnas_redundantes = [col for col in df.columns if col.endswith('_y') or col.endswith('_x')]
        if columnas_redundantes:
            df = df.drop(columns=columnas_redundantes)
            logging.info(f"Columnas redundantes eliminadas: {columnas_redundantes}")

        # 3. Tratar valores nulos
        if 'genero' in df.columns:
            df['genero'] = df['genero'].fillna('No Especificado')
        logging.info("Valores nulos tratados.")

        # 4. Estandarizar texto (mayúsculas, tildes, UTF-8)
        columnas_texto = ['pais', 'categoria', 'marca', 'genero', 'nombre']
        for col in columnas_texto:
            if col in df.columns:
                # Convertir a string, quitar espacios, formato Título y remover tildes
                df[col] = df[col].astype(str).str.strip().str.title()
                df[col] = df[col].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        logging.info("Texto estandarizado (sin tildes, formato Título).")

        # 5. Validar que los países sean únicamente Chile, Perú o Colombia
        # Ojo: Como quitamos tildes arriba, 'Perú' ahora es 'Peru'
        paises_permitidos = ['Chile', 'Peru', 'Colombia']
        df = df[df['pais'].isin(paises_permitidos)]
        logging.info("Validación estricta de países aplicada.")

        # 6. Convertir precios locales a USD usando tasas de cambio
        # Las llaves del diccionario ahora van sin tilde por la estandarización previa
        tasas_cambio = {
            'Chile': 0.0011,      
            'Peru': 0.27,         
            'Colombia': 0.00026   
        }
        df['precio_final_usd'] = df.apply(
            lambda row: row['precio_final_local'] * tasas_cambio.get(row['pais'], 1), 
            axis=1
        ).round(2)
        logging.info("Precios convertidos a USD.")

        # 7. Normalizar fechas (ISO 8601) y Validar fechas futuras
        fecha_actual = pd.Timestamp.now()
        columnas_fecha = ['fecha_hora', 'fecha_registro']
        for col in columnas_fecha:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        # Filtrar fechas futuras en la transacción
        df = df[df['fecha_hora'] <= fecha_actual]
        
        # Aplicar formato ISO 8601
        for col in columnas_fecha:
            if col in df.columns:
                df[col] = df[col].dt.strftime('%Y-%m-%dT%H:%M:%S')
        logging.info("Fechas normalizadas a ISO 8601 y fechas futuras eliminadas.")

        # 8. Validar rangos lógicos (precios, cantidades)
        df = df[(df['precio_final_usd'] > 0) & (df['cantidad'] > 0)]
        # Validar que los días de demora no sean negativos
        if 'dias_demora_real' in df.columns:
            df = df[df['dias_demora_real'] >= 0]
        logging.info("Validación de rangos lógicos aplicada.")

        # 9. Guardar archivo transformado
        # Asegurar codificación UTF-8 al exportar
        df.to_csv(ruta_salida, index=False, encoding='utf-8')
        
        filas_finales = len(df)
        logging.info(f"Transformación exitosa. Filas: {filas_iniciales} -> {filas_finales}")
        logging.info(f"Archivo guardado en: {ruta_salida}")

    except Exception as e:
        logging.error(f"Error crítico durante la transformación: {str(e)}")
        raise

if __name__ == "__main__":
    RUTA_RAW = "../data/consolidado_raw.csv"
    RUTA_CLEAN = "../data/consolidado_transformado.csv"
    aplicar_transformaciones(RUTA_RAW, RUTA_CLEAN)