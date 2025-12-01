# =========================
#     MindCare AI Backend
#         FastAPI
# =========================

FROM python:3.11-slim

# Evita buffering no log do Render
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o projeto
COPY . .

# Porta usada pelo Render
EXPOSE 8000

# CMD de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
