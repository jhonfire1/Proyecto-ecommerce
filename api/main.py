from fastapi import FastAPI, HTTPException, status
from sqlalchemy import text

from api.database import engine

app = FastAPI()


@app.get("/")
def root():

    with engine.connect() as conn:

        resultado = conn.execute(
            text("SELECT COUNT(*) FROM clientes_usuarios")
        )

        total_clientes = resultado.scalar()

    return {
        "mensaje": "Conexion exitosa",
        "clientes": total_clientes
    }


@app.get("/clientes")
def obtener_clientes():

    with engine.connect() as conn:

        resultado = conn.execute(
            text("""
                SELECT *
                FROM clientes_usuarios
            """)
        )

        clientes = [
            dict(row._mapping)
            for row in resultado
        ]

    return clientes


@app.get("/productos")
def obtener_productos():

    with engine.connect() as conn:

        resultado = conn.execute(
            text("""
                SELECT *
                FROM catalogo_productos
            """)
        )

        productos = [
            dict(row._mapping)
            for row in resultado
        ]

    return productos


@app.get("/bodegas")
def obtener_bodegas():

    with engine.connect() as conn:

        resultado = conn.execute(
            text("""
                SELECT *
                FROM operaciones_bodegas
            """)
        )

        bodegas = [
            dict(row._mapping)
            for row in resultado
        ]

    return bodegas


@app.get("/ventas")
def obtener_ventas():

    with engine.connect() as conn:

        resultado = conn.execute(
            text("""
                SELECT *
                FROM monitoreo_ventas_logistica
            """)
        )

        ventas = [
            dict(row._mapping)
            for row in resultado
        ]

    return ventas


@app.get("/clientes/{id_usuario}")
def obtener_cliente_por_id(id_usuario: int):

    with engine.connect() as conn:

        resultado = conn.execute(
            text("""
                SELECT *
                FROM clientes_usuarios
                WHERE id_usuario = :id_usuario
            """),
            {"id_usuario": id_usuario}
        )

        cliente = resultado.fetchone()

    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )

    return dict(cliente._mapping)


@app.get("/productos/{id_producto}")
def obtener_producto_por_id(id_producto: int):

    with engine.connect() as conn:

        resultado = conn.execute(
            text("""
                SELECT *
                FROM catalogo_productos
                WHERE id_producto = :id_producto
            """),
            {"id_producto": id_producto}
        )

        producto = resultado.fetchone()

    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return dict(producto._mapping)


@app.get("/bodegas/{id_bodega}")
def obtener_bodega_por_id(id_bodega: int):

    with engine.connect() as conn:

        resultado = conn.execute(
            text("""
                SELECT *
                FROM operaciones_bodegas
                WHERE id_bodega = :id_bodega
            """),
            {"id_bodega": id_bodega}
        )

        bodega = resultado.fetchone()

    if bodega is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bodega no encontrada"
        )

    return dict(bodega._mapping)


@app.get("/ventas/{id_transaccion}")
def obtener_venta_por_id(id_transaccion: int):

    with engine.connect() as conn:

        resultado = conn.execute(
            text("""
                SELECT *
                FROM monitoreo_ventas_logistica
                WHERE id_transaccion = :id_transaccion
            """),
            {"id_transaccion": id_transaccion}
        )

        venta = resultado.fetchone()

    if venta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )

    return dict(venta._mapping)