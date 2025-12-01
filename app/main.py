from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.interacoes_routes import router as interacoes_router
from app.status_routes import router as status_router

app = FastAPI(title="MindCare IA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROTAS
app.include_router(interacoes_router, prefix="/interacoes", tags=["Interações Medicamentosas"])
app.include_router(status_router,    prefix="/status",      tags=["Status / Infra"])


@app.get("/", tags=["Sistema"])
def root():
    return {"status": "MindCare AI rodando 🎉", "online": True}
