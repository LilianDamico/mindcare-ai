# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import correto das rotas
from app.interacoes_routes import router as interacoes_router
from app.status_routes import router as status_router

app = FastAPI(title="MindCare IA API")

# =======================
#  CORS (liberado para uso público)
# =======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sua Vercel consome aqui
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================
#  REGISTRO DE ROTAS
# =======================
app.include_router(interacoes_router)  # /interacoes/{medicamento}
app.include_router(status_router)      # /status

# =======================
#  ROTA PRINCIPAL
# =======================
@app.get("/", tags=["Sistema"])
def root():
    return {
        "status": "MindCare AI rodando 💥",
        "online": True
    }
