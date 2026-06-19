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

for nombre, config in ENDPOINTS.items():

    print(f"\n📥 Extrayendo {nombre}...")

    respuesta = requests.get(config["url"])

    if respuesta.status_code != 200:
        print(
            f"❌ Error en {nombre}: "
            f"{respuesta.status_code}"
        )
        continue

    datos = respuesta.json()

    print(
        f"✅ Registros obtenidos: "
        f"{len(datos):,}"
    )

    df = pd.DataFrame(datos)

    df.to_csv(
        config["archivo"],
        index=False
    )

    print(
        f"💾 CSV generado: "
        f"{config['archivo']}"
    )

print("\n🎉 Pipeline ETL finalizado correctamente")