# ============================
#   BUILD STAGE (dependencies)
# ============================
FROM python:3.11-slim AS builder

WORKDIR /app

# Previne cache infinito no Docker
ENV PIP_NO_CACHE_DIR=1

# Instala dependências de build (necessárias pro pdfplumber + bs4)
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instala libs usando wheels para reduzir tamanho final
RUN pip install --upgrade pip wheel \
    && pip wheel --wheel-dir=/wheels -r requirements.txt


# ============================
#   RUNTIME STAGE (Produção)
# ============================
FROM python:3.11-slim

WORKDIR /app

# Variáveis EXP (seguras para container)
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# Instala apenas runtime libs — imagem MUITO MENOR
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir /wheels/*

# Copia aplicação
COPY . .

# ============================
#  HEALTHCHECK (modo PRO)
# ============================
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD curl -f http://localhost:${PORT}/status || exit 1

# ============================
#  START COMMAND (GUNICORN 🔥)
# ============================
CMD ["bash", "-c", "gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:${PORT} --workers 2 --timeout 120"]
