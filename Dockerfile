# ===========================
# 📌 BASE PYTHON SLIM
# ===========================
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

# ===========================
# 📦 INSTALL REQUIREMENTS FIRST (cache otimizado)
# ===========================
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ===========================
# 📁 COPY PROJECT FILES
# ===========================
COPY . .

# ===========================
# 🔥 APP CONFIG
# ===========================
ENV PORT=8000

# deixamos o EXPOSE apenas documental
EXPOSE $PORT

# HEALTHCHECK → Render pode usar isso para restart automático
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD wget -qO- http://localhost:$PORT/ || exit 1

# ===========================
# 🚀 START COMMAND (PRODUCTION)
# ===========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
