# Modelo Relacional - Proyecto E-commerce

## Entidades

### clientes_usuarios

Almacena la información de los usuarios registrados en la plataforma.

| Campo          | Tipo         |
| -------------- | ------------ |
| id_usuario     | INTEGER      |
| pais           | VARCHAR(20)  |
| fecha_registro | DATE         |
| genero         | VARCHAR(20)  |
| email          | VARCHAR(255) |

---

### catalogo_productos

Registra la oferta de productos disponible en la plataforma.

| Campo           | Tipo          |
| --------------- | ------------- |
| id_producto     | INTEGER       |
| nombre          | VARCHAR(150)  |
| categoria       | VARCHAR(100)  |
| marca           | VARCHAR(100)  |
| precio_base_usd | NUMERIC(10,2) |

---

### operaciones_bodegas

Contiene información sobre las bodegas y operadores logísticos.

| Campo                    | Tipo         |
| ------------------------ | ------------ |
| id_bodega                | INTEGER      |
| pais_ciudad              | VARCHAR(100) |
| capacidad_almacenamiento | INTEGER      |
| operador_logistico       | VARCHAR(100) |

---

### monitoreo_ventas_logistica

Tabla transaccional principal que registra las compras realizadas.

| Campo              | Tipo          |
| ------------------ | ------------- |
| id_transaccion     | BIGINT        |
| fecha_hora         | TIMESTAMP     |
| id_usuario         | INTEGER       |
| id_producto        | INTEGER       |
| id_bodega          | INTEGER       |
| cantidad           | INTEGER       |
| precio_final_local | NUMERIC(12,2) |
| canal_venta        | VARCHAR(20)   |
| clics_previos      | INTEGER       |
| dias_demora_real   | INTEGER       |

---

## Relaciones

### Relación 1

clientes_usuarios.id_usuario → monitoreo_ventas_logistica.id_usuario

Tipo:

1:N

Un usuario puede realizar múltiples compras.

---

### Relación 2

catalogo_productos.id_producto → monitoreo_ventas_logistica.id_producto

Tipo:

1:N

Un producto puede aparecer en múltiples transacciones.

---

### Relación 3

operaciones_bodegas.id_bodega → monitoreo_ventas_logistica.id_bodega

Tipo:

1:N

Una bodega puede despachar múltiples órdenes.

---

## Claves Primarias (PK)

* clientes_usuarios.id_usuario
* catalogo_productos.id_producto
* operaciones_bodegas.id_bodega
* monitoreo_ventas_logistica.id_transaccion

## Claves Foráneas (FK)

* monitoreo_ventas_logistica.id_usuario
* monitoreo_ventas_logistica.id_producto
* monitoreo_ventas_logistica.id_bodega
