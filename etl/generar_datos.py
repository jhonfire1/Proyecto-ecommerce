import os
import random
from datetime import datetime

import pandas as pd
from faker import Faker
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / "docker" / ".env"



load_dotenv(env_path)



# =====================================================
# CONFIGURACIÓN
# =====================================================

N_CLIENTES = 10000
N_PRODUCTOS = 5000
N_BODEGAS = 2000
N_VENTAS = 50000

fake = Faker("es_ES")

PAISES = ['Chile', 'Perú', 'Colombia']

TASAS_CAMBIO = {
    'Chile': 940.0,
    'Perú': 3.75,
    'Colombia': 4000.0
}

CATEGORIAS = [
    'Electrónica',
    'Vestuario',
    'Hogar',
    'Deportes',
    'Juguetes'
]

CANALES = ['Web', 'App']

OPERADORES = [
    'Blue Express',
    'DHL',
    'Servientrega',
    'Olva Courier'
]

print("🚀 Iniciando generación de datos sintéticos...")

# =====================================================
# CLIENTES
# =====================================================

clientes = []

for i in range(1, N_CLIENTES + 1):

    pais = random.choice(PAISES)

    genero = random.choices(
        ['Masculino', 'Femenino', 'No binario', None],
        weights=[42, 42, 11, 5]
    )[0]

    perfil = random.choices(
        ['Tecno', 'Ofertas', 'Inactivo'],
        weights=[35, 45, 20]
    )[0]

    clientes.append({
        "id_usuario": i,
        "pais": pais,
        "fecha_registro": fake.date_time_between(
            start_date='-3y',
            end_date='now'
        ),
        "genero": genero,
        "email": f"user_{i}_anon@ecommerce.com",
        "_perfil_oculto": perfil
    })

df_clientes = pd.DataFrame(clientes)

print(f"✅ Clientes: {len(df_clientes):,}")

# =====================================================
# PRODUCTOS
# =====================================================

marcas_por_categoria = {
    'Electrónica': ['Samsung', 'Apple', 'Sony', 'Xiaomi'],
    'Vestuario': ['Nike', 'Adidas', 'Zara', 'H&M'],
    'Hogar': ['IKEA', 'CIC', 'Rosen', 'Philips'],
    'Deportes': ['Wilson', 'Spalding', 'Decathlon'],
    'Juguetes': ['Lego', 'Mattel', 'Hasbro']
}

productos = []

for i in range(1, N_PRODUCTOS + 1):

    categoria = random.choice(CATEGORIAS)

    marca = random.choice(
        marcas_por_categoria[categoria]
    )

    if categoria == 'Electrónica':
        precio_usd = round(
            random.uniform(100, 1500),
            2
        )

    elif categoria == 'Vestuario':
        precio_usd = round(
            random.uniform(15, 120),
            2
        )

    else:
        precio_usd = round(
            random.uniform(10, 500),
            2
        )

    productos.append({
        "id_producto": i,
        "nombre": f"{categoria} {marca} {fake.bothify('??##')}",
        "categoria": categoria,
        "marca": marca,
        "precio_base_usd": precio_usd
    })

df_productos = pd.DataFrame(productos)

print(f"✅ Productos: {len(df_productos):,}")

# =====================================================
# BODEGAS
# =====================================================

ciudades_por_pais = {
    'Chile': [
        'Santiago',
        'Valparaíso',
        'Concepción'
    ],
    'Perú': [
        'Lima',
        'Arequipa',
        'Trujillo'
    ],
    'Colombia': [
        'Bogotá',
        'Medellín',
        'Cali'
    ]
}

bodegas = []

for i in range(1, N_BODEGAS + 1):

    pais = random.choice(PAISES)

    ciudad = random.choice(
        ciudades_por_pais[pais]
    )

    operador = random.choice(OPERADORES)

    bodegas.append({
        "id_bodega": i,
        "pais_ciudad": f"{pais} - {ciudad}",
        "capacidad_almacenamiento": random.randint(
            5000,
            50000
        ),
        "operador_logistico": operador,
        "_pais_oculto": pais,
        "_operador_oculto": operador
    })

df_bodegas = pd.DataFrame(bodegas)

print(f"✅ Bodegas: {len(df_bodegas):,}")

# =====================================================
# VENTAS
# =====================================================

ventas = []

for i in range(1, N_VENTAS + 1):

    cliente = df_clientes.sample(1).iloc[0]

    producto = df_productos.sample(1).iloc[0]

    bodegas_pais = df_bodegas[
        df_bodegas['_pais_oculto'] == cliente['pais']
    ]

    if len(bodegas_pais) > 0:
        bodega = bodegas_pais.sample(1).iloc[0]
    else:
        bodega = df_bodegas.sample(1).iloc[0]

    perfil = cliente['_perfil_oculto']

    if (
        perfil == 'Tecno'
        and producto['categoria'] == 'Electrónica'
    ):
        clics = random.randint(15, 45)
        cantidad = random.randint(1, 2)
        canal = 'App'
        descuento = random.uniform(0.95, 1.0)

    elif perfil == 'Ofertas':

        clics = random.randint(20, 60)
        cantidad = random.randint(2, 5)
        canal = random.choice(CANALES)
        descuento = random.uniform(0.70, 0.85)

    else:

        clics = random.randint(1, 8)
        cantidad = 1
        canal = 'Web'
        descuento = 1.0

    tasa = TASAS_CAMBIO[cliente['pais']]

    precio_local = (
        producto['precio_base_usd']
        * tasa
        * descuento
        * cantidad
    )

    if any(
        x in bodega['pais_ciudad']
        for x in ['Santiago', 'Lima', 'Bogotá']
    ):
        dias_base = random.randint(1, 3)
    else:
        dias_base = random.randint(3, 6)

    if bodega['_operador_oculto'] == 'DHL':
        dias_base -= 1

    if cantidad > 3:
        dias_base += 2

    dias_demora = max(
        1,
        dias_base + random.randint(-1, 1)
    )

    fecha_tx = fake.date_time_between(
        start_date='-18M',
        end_date='now'
    )

    ventas.append({
        "id_transaccion": i,
        "fecha_hora": fecha_tx,
        "id_usuario": int(cliente["id_usuario"]),
        "id_producto": int(producto["id_producto"]),
        "id_bodega": int(bodega["id_bodega"]),
        "cantidad": cantidad,
        "precio_final_local": round(
            precio_local,
            2
        ),
        "canal_venta": canal,
        "clics_previos": clics,
        "dias_demora_real": dias_demora
    })

df_ventas = pd.DataFrame(ventas)

print(f"✅ Ventas: {len(df_ventas):,}")

# =====================================================
# LIMPIEZA COLUMNAS AUXILIARES
# =====================================================

df_clientes.drop(
    columns=['_perfil_oculto'],
    inplace=True
)

df_bodegas.drop(
    columns=[
        '_pais_oculto',
        '_operador_oculto'
    ],
    inplace=True
)

# =====================================================
# CONEXIÓN POSTGRES
# =====================================================

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

print("USER =", DB_USER)
print("DB =", DB_NAME)
print("HOST =", DB_HOST)
print("PORT =", DB_PORT)

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("🔌 Conectando a PostgreSQL...")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("✅ PostgreSQL conectado correctamente")
print(
    f"postgresql://{DB_USER}:****@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# =====================================================
# LIMPIAR TABLAS
# =====================================================

with engine.begin() as conn:
    conn.execute(text("""
        TRUNCATE TABLE
            monitoreo_ventas_logistica,
            clientes_usuarios,
            catalogo_productos,
            operaciones_bodegas
        RESTART IDENTITY CASCADE;
    """))

print("🧹 Tablas limpiadas.")

# =====================================================
# INSERTAR DATOS
# =====================================================

print("📥 Insertando clientes...")
df_clientes.to_sql(
    "clientes_usuarios",
    engine,
    if_exists="append",
    index=False
)

print("📥 Insertando productos...")
df_productos.to_sql(
    "catalogo_productos",
    engine,
    if_exists="append",
    index=False
)

print("📥 Insertando bodegas...")
df_bodegas.to_sql(
    "operaciones_bodegas",
    engine,
    if_exists="append",
    index=False
)

print("📥 Insertando ventas...")
df_ventas.to_sql(
    "monitoreo_ventas_logistica",
    engine,
    if_exists="append",
    index=False
)

print("🎉 Base de datos poblada correctamente.")
print("🚀 Lista para FastAPI y Swagger.")