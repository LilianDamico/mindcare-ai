from fastapi import APIRouter

router = APIRouter(prefix="/status", tags=["🟢 Status"])

@router.get("/")
async def status():
    return {"ok": True, "API": "MindCare AI ativa e operacional"}
