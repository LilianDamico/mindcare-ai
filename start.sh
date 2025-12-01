#!/bin/bash
echo "🚀 Iniciando MindCare AI no Render..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
