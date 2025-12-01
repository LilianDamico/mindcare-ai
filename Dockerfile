FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 🔥 tornar o script executável
RUN chmod +x start.sh

EXPOSE 10000

CMD ["bash", "start.sh"]
