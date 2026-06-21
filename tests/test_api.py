from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

# =====================================================
# ROOT
# =====================================================

def test_root():
    respuesta = client.get("/")

    assert respuesta.status_code == 200
    assert "mensaje" in respuesta.json()


# =====================================================
# ENDPOINTS GENERALES
# =====================================================

def test_obtener_clientes():
    respuesta = client.get("/clientes")

    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)
    assert len(respuesta.json()) > 0


def test_obtener_productos():
    respuesta = client.get("/productos")

    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)
    assert len(respuesta.json()) > 0


def test_obtener_bodegas():
    respuesta = client.get("/bodegas")

    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)
    assert len(respuesta.json()) > 0


# =====================================================
# VENTAS
# =====================================================

def test_obtener_venta_existente():
    respuesta = client.get("/ventas/1")

    assert respuesta.status_code == 200
    assert respuesta.json()["id_transaccion"] == 1


def test_obtener_venta_no_existente():
    respuesta = client.get("/ventas/999999")

    assert respuesta.status_code == 404


# =====================================================
# CLIENTES
# =====================================================

def test_obtener_cliente_existente():
    respuesta = client.get("/clientes/1")

    assert respuesta.status_code == 200
    assert respuesta.json()["id_usuario"] == 1


def test_obtener_cliente_no_existente():
    respuesta = client.get("/clientes/999999")

    assert respuesta.status_code == 404


# =====================================================
# PRODUCTOS
# =====================================================

def test_obtener_producto_existente():
    respuesta = client.get("/productos/1")

    assert respuesta.status_code == 200
    assert respuesta.json()["id_producto"] == 1


def test_obtener_producto_no_existente():
    respuesta = client.get("/productos/999999")

    assert respuesta.status_code == 404


# =====================================================
# BODEGAS
# =====================================================

def test_obtener_bodega_existente():
    respuesta = client.get("/bodegas/1")

    assert respuesta.status_code == 200
    assert respuesta.json()["id_bodega"] == 1


def test_obtener_bodega_no_existente():
    respuesta = client.get("/bodegas/999999")

    assert respuesta.status_code == 404