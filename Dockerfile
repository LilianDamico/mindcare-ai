FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# garante permissão
RUN chmod +x start.sh

# Render ignora EXPOSE fixo, então NÃO coloque EXPOSE 10000
CMD ["bash", "start.sh"]
