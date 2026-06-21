import os
import pandas as pd
import requests

# ==========================================
# CONFIGURACIÓN ENDPOINTS
# ==========================================

ENDPOINTS = {
    "clientes": {
        "url": "http://127.0.0.1:8000/clientes",
        "archivo": "data/clientes_usuarios_raw.csv"
    },
    "productos": {
        "url": "http://127.0.0.1:8000/productos",
        "archivo": "data/catalogo_productos_raw.csv"
    },
    "bodegas": {
        "url": "http://127.0.0.1:8000/bodegas",
        "archivo": "data/operaciones_bodegas_raw.csv"
    },
    "ventas": {
        "url": "http://127.0.0.1:8000/ventas",
        "archivo": "data/monitoreo_ventas_logistica_raw.csv"
    }
}

# ==========================================
# EXTRACCIÓN
# ==========================================

def extraer_datos(url):
    """
    Extrae datos desde un endpoint de la API.
    """

    respuesta = requests.get(url)

    respuesta.raise_for_status()

    return respuesta.json()


# ==========================================
# TRANSFORMACIÓN
# ==========================================

def transformar_datos(datos_crudos):
    """
    Convierte los datos JSON en DataFrame.
    """

    df = pd.DataFrame(datos_crudos)

    return df


# ==========================================
# CARGA
# ==========================================

def cargar_datos(df, ruta_salida):
    """
    Guarda el DataFrame en formato CSV.
    """

    carpeta = os.path.dirname(ruta_salida)

    if carpeta:
        os.makedirs(carpeta, exist_ok=True)

    df.to_csv(
        ruta_salida,
        index=False,
        encoding="utf-8"
    )


# ==========================================
# PIPELINE PRINCIPAL
# ==========================================

def ejecutar_pipeline():

    print("🚀 Iniciando Pipeline ETL...")

    for nombre, config in ENDPOINTS.items():

        print(f"\n📥 Extrayendo {nombre}...")

        try:

            datos_crudos = extraer_datos(
                config["url"]
            )

            print(
                f"✅ Registros obtenidos: "
                f"{len(datos_crudos):,}"
            )

            df = transformar_datos(
                datos_crudos
            )

            cargar_datos(
                df,
                config["archivo"]
            )

            print(
                f"💾 CSV generado: "
                f"{config['archivo']}"
            )

        except requests.exceptions.ConnectionError:

            print(
                f"❌ No se pudo conectar "
                f"al endpoint {nombre}"
            )

        except requests.exceptions.HTTPError as e:

            print(
                f"❌ Error HTTP en {nombre}: "
                f"{e}"
            )

        except Exception as e:

            print(
                f"❌ Error inesperado "
                f"en {nombre}: {e}"
            )

    print("\n🎉 Pipeline ETL finalizado correctamente")


# ==========================================
# PUNTO DE ENTRADA
# ==========================================

if __name__ == "__main__":
    ejecutar_pipeline()