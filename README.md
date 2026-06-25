# Plataforma Analítica E-Commerce Regional 📊

## 1. Descripción del Proyecto
Este proyecto consiste en una solución analítica unificada de extremo a extremo (*end-to-end*) diseñada para integrar, limpiar y analizar datos fragmentados de operaciones de retail digital en **Chile, Perú y Colombia**. 

A través de un pipeline automatizado, la plataforma consolida datos de múltiples fuentes aisladas para resolver ineficiencias logísticas y comerciales, alimentando tres dashboards interactivos especializados y desplegando modelos predictivos y de segmentación en tiempo real.

---

## 2. Requisitos Previos
Antes de levantar la plataforma, asegúrate de tener instalado lo siguiente en tu sistema:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (con soporte para WSL2 si estás en Windows).
* [Python 3.12](https://www.python.org/downloads/) o superior (para ejecución de scripts de utilidades locales).

---

## 3. Instrucciones de Clonación e Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DE_TU_REPOSITORIO_GITHUB>
    cd proyecto-ecommerce
    ```

2.  **Configurar las Variables de Entorno (`.env`):**
    Crea un archivo llamado `.env` dentro de la carpeta `docker/` (este archivo está excluido en `.gitignore` por seguridad). Copia y pega la siguiente configuración rellenando con tus credenciales:
    ```env
    POSTGRES_USER=tu_usuario
    POSTGRES_PASSWORD=tu_contraseña_segura
    POSTGRES_DB=ecommerce_db
    POSTGRES_HOST=ecommerce_postgres
    POSTGRES_PORT=5432
    ```

---

## 4. Despliegue de la Plataforma (Comando Exacto) 🚀

De acuerdo con el orden de levantamiento obligatorio, ejecuta el siguiente comando desde la carpeta donde se encuentra tu configuración multiservicio:

```bash
cd docker
docker compose up --build
