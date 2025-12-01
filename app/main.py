# app/main.py
from fastapi import FastAPI
from app.interacoes_routes import router as interacoes_router
from app.status_routes import router as status_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MindCare IA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # libera frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROTAS REGISTRADAS AQUI
app.include_router(interacoes_router)              # 👇 agora carrega!
app.include_router(status_router, prefix="/status")


@app.get("/")
def root():
    return {"status": "MindCare AI rodando 🎉"}
