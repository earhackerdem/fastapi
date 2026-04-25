set shell := ["bash", "-cu"]

project_dir := `pwd`

# Configura el entorno virtual e instala dependencias
setup:
    python3 -m venv .venv
    . .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && pip install "fastapi[standard]==0.136.1"

# Levanta la API en modo desarrollo
up:
    . .venv/bin/activate && fastapi dev main.py

# Detiene procesos comunes de desarrollo
down:
    pkill -f "fastapi dev main.py" || true
    pkill -f "uvicorn main:app --reload" || true

# Limpia caches y artefactos locales del proyecto
clean:
    rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache .hypothesis .coverage .cache
    find . -type d -name "__pycache__" -prune -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Reinicia el entorno local (limpia e instala dependencias)
reset:
    just clean
    just setup
