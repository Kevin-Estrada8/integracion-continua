# Integración continua de servicios Docker

Proyecto académico que valida la comunicación HTTP entre dos contenedores Python mediante Docker Compose y GitHub Actions.

## Descripción general

Este proyecto demuestra cómo comprobar automáticamente que dos servicios aislados en contenedores pueden comunicarse correctamente. Un servicio cliente envía un mensaje JSON a un servidor HTTP en una red privada de Docker; el servidor procesa la solicitud y devuelve una respuesta que el cliente valida.

Características principales:

- Construcción de dos imágenes independientes basadas en Python 3.12 Alpine.
- Comunicación entre contenedores a través de una red bridge privada de Docker Compose.
- Endpoint `GET /health` para comprobar la disponibilidad del servidor.
- Endpoint `POST /mensaje` para recibir y responder mensajes JSON.
- Verificación de disponibilidad del servidor antes de iniciar el cliente, mediante un health check y `depends_on`.
- Reintentos del cliente ante fallos transitorios de conexión.
- Flujo de integración continua en GitHub Actions al enviar cambios o abrir pull requests hacia `main`.

## Stack tecnológico

- **Lenguaje:** Python 3.12.
- **Contenedores y orquestación:** Docker, Docker Compose y la imagen `python:3.12-alpine`.
- **Base de datos:** No utiliza base de datos.
- **Librerías clave:** módulos de la biblioteca estándar de Python: `http.server`, `json`, `time`, `urllib.request` y `urllib.error`.
- **Integración continua:** GitHub Actions (`.github/workflows/ci.yml`).

## Estructura del repositorio

```text
.
├── contenedor_uno/
│   ├── Dockerfile       # Imagen del cliente que envía y valida el mensaje
│   └── app.py           # Solicitud HTTP POST al segundo servicio
├── contenedor_dos/
│   ├── Dockerfile       # Imagen del servidor HTTP
│   └── app.py           # Endpoints /health y /mensaje
├── .github/
│   └── workflows/
│       └── ci.yml       # Construcción y prueba automatizadas en GitHub Actions
├── docker-compose.yml   # Servicios, red, health check y orden de inicio
└── README.md            # Documentación del proyecto
```

## Requisitos previos

- Git.
- Docker Desktop (Windows o macOS) o Docker Engine (Linux), iniciado y operativo.
- Docker Compose v2, disponible como el subcomando `docker compose`.
- Conexión a Internet durante la primera construcción para descargar `python:3.12-alpine`.

No es necesario instalar Python en el sistema anfitrión: las aplicaciones se ejecutan dentro de las imágenes Docker. El proyecto no requiere archivos `.env` ni configuración externa.

## Guía de instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/Kevin-Estrada8/integracion-continua.git
cd integracion-continua
```

Sustituye `<https://github.com/Kevin-Estrada8/integracion-continua.git>` por la URL del repositorio proporcionada para el proyecto.

### 2. Comprobar Docker Compose

```bash
docker compose version
```

### 3. Validar la configuración

```bash
docker compose config
```

### 4. Construir y ejecutar la prueba de comunicación

```bash
docker compose up --build --abort-on-container-exit --exit-code-from contenedor_uno
```

Compose construye ambos servicios, espera a que `contenedor_dos` pase su health check y ejecuta el cliente `contenedor_uno`. La ejecución es satisfactoria si el cliente recibe una respuesta con estado `exitoso` e imprime `PRUEBA DE COMUNICACION EXITOSA`; un fallo de comunicación produce un código de salida distinto de cero.

El servidor atiende en el puerto `8000` dentro de la red privada de Compose. No se publica un puerto en el host, por lo que sus endpoints no están expuestos directamente fuera de esa red.

### 5. Limpiar los contenedores

Después de una ejecución interactiva, elimina los recursos creados con:

```bash
docker compose down --volumes --remove-orphans
```

## Pruebas y verificación

El repositorio no incluye una suite de pruebas unitarias independiente. La prueba de integración consiste en ejecutar el cliente contra el servidor mediante Docker Compose:

```bash
docker compose up --build --abort-on-container-exit --exit-code-from contenedor_uno
```

GitHub Actions ejecuta automáticamente `docker compose config` y esta prueba de comunicación en cada `push` y `pull_request` dirigido a la rama `main`. El flujo limpia los contenedores al finalizar, incluso si la prueba falla.

## Créditos y autoría

- **Integrantes:** [Completar con los nombres de los integrantes]
- **Asignatura:** [Completar con el nombre de la asignatura]
- **Institución:** [Completar con el nombre de la institución, si corresponde]
