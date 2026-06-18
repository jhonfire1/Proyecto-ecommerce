-- 1. LIMPIEZA: Eliminar tablas si existen en orden inverso a su creación
-- Esto evita errores de dependencias por llaves foráneas al reiniciar la BD.
DROP TABLE IF EXISTS monitoreo_ventas_logistica;
DROP TABLE IF EXISTS clientes_usuarios;
DROP TABLE IF EXISTS catalogo_productos;
DROP TABLE IF EXISTS operaciones_bodegas;

-- 2. TABLA: clientes_usuarios (Tabla Maestra - Sin FK)
CREATE TABLE clientes_usuarios (
    id_usuario SERIAL PRIMARY KEY,
    pais VARCHAR(50) NOT NULL,
    fecha_registro TIMESTAMP NOT NULL,
    genero VARCHAR(20),
    email VARCHAR(255)
);

-- 3. TABLA: catalogo_productos (Tabla Maestra - Sin FK)
CREATE TABLE catalogo_productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    categoria VARCHAR(100),
    marca VARCHAR(100),
    precio_base_usd NUMERIC(10, 2) NOT NULL
);

-- 4. TABLA: operaciones_bodegas (Tabla Maestra - Sin FK)
CREATE TABLE operaciones_bodegas (
    id_bodega SERIAL PRIMARY KEY,
    pais_ciudad VARCHAR(100) NOT NULL,
    capacidad_almacenamiento INTEGER,
    operador_logistico VARCHAR(100)
);

-- 5. TABLA: monitoreo_ventas_logistica (Tabla Transaccional - Contiene las FK estrictas)
CREATE TABLE monitoreo_ventas_logistica (
    id_transaccion BIGSERIAL PRIMARY KEY,
    fecha_hora TIMESTAMP NOT NULL,
    id_usuario INTEGER NOT NULL REFERENCES clientes_usuarios(id_usuario),
    id_producto INTEGER NOT NULL REFERENCES catalogo_productos(id_producto),
    id_bodega INTEGER NOT NULL REFERENCES operaciones_bodegas(id_bodega),
    cantidad INTEGER NOT NULL,
    precio_final_local NUMERIC(12, 2) NOT NULL,
    canal_venta VARCHAR(50),
    clics_previos INTEGER,
    dias_demora_real INTEGER
);