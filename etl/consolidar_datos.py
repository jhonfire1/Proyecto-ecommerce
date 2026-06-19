import pandas as pd

print("Iniciando consolidación...")

df_clientes = pd.read_csv("data/clientes_usuarios_raw.csv")
df_productos = pd.read_csv("data/catalogo_productos_raw.csv")
df_bodegas = pd.read_csv("data/operaciones_bodegas_raw.csv")
df_ventas = pd.read_csv("data/monitoreo_ventas_logistica_raw.csv")

print("Clientes:", len(df_clientes))
print("Productos:", len(df_productos))
print("Bodegas:", len(df_bodegas))
print("Ventas:", len(df_ventas))

# ==========================
# VENTAS + CLIENTES
# ==========================

df_consolidado = df_ventas.merge(
    df_clientes,
    on="id_usuario",
    how="left"
)

print("Ventas + Clientes:", len(df_consolidado))

# ==========================
# + PRODUCTOS
# ==========================

df_consolidado = df_consolidado.merge(
    df_productos,
    on="id_producto",
    how="left"
)

print("Ventas + Clientes + Productos:", len(df_consolidado))

# ==========================
# + BODEGAS
# ==========================

df_consolidado = df_consolidado.merge(
    df_bodegas,
    on="id_bodega",
    how="left"
)

print(
    "Ventas + Clientes + Productos + Bodegas:",
    len(df_consolidado)
)

# ==========================
# EXPORTAR CSV CONSOLIDADO
# ==========================

ruta_salida = "data/consolidado_raw.csv"

df_consolidado.to_csv(
    ruta_salida,
    index=False
)

print(f"CSV generado: {ruta_salida}")
print(f"Filas exportadas: {len(df_consolidado):,}")
print(f"Columnas exportadas: {len(df_consolidado.columns)}")