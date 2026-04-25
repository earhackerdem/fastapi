# Curso FastAPI Project

API construida con FastAPI y SQLModel para gestionar clientes, junto con endpoints de ejemplo para hora por pais, transacciones e invoices.

## Requisitos

- Python 3.10 o superior
- `pip`

## Setup del proyecto

Desde la raiz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install "fastapi[standard]==0.136.1"
```

## Ejecutar en desarrollo

```bash
fastapi dev main.py
```

Alternativa con Uvicorn:

```bash
uvicorn main:app --reload
```

Con `just`:

```bash
just setup
just up
```

## Comandos de mantenimiento (Just)

```bash
just down    # detiene procesos de desarrollo
just clean   # limpia caches y artefactos locales
just reset   # ejecuta clean + setup
```

## Documentacion interactiva

Con la app corriendo:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoints principales

- `GET /` - mensaje de prueba
- `GET /time/{iso_code}` - hora por codigo de pais (ej. `CO`, `MX`)
- `POST /customers` - crear customer
- `GET /customers` - listar customers
- `GET /customers/{id}` - obtener customer por id
- `PATCH /customers/{id}` - actualizar parcialmente un customer
- `DELETE /customers/{id}` - eliminar customer
- `POST /transactions` - endpoint de ejemplo
- `POST /invoices` - endpoint de ejemplo

## Ejemplo rapido (PATCH)

```bash
curl -X PATCH \
  'http://127.0.0.1:8000/customers/2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Pablo"
}'
```

## Notas

- Si usas Linux/macOS, activa con `source .venv/bin/activate`.
- Si usas Windows (PowerShell), activa con `.\.venv\Scripts\Activate.ps1`.

