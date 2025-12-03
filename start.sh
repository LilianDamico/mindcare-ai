#!/bin/bash

echo "🚀 Iniciando MindCare AI (Modo Premium) no Render..."


if [ -z "$PORT" ]; then
  echo "❌ ERRO: Variável \$PORT não definida!"
  exit 1
fi

exec gunicorn app.main:app \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --log-level info
