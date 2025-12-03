# app/interacoes_routes.py
# ===========================================
# Interações Medicamentosas - MindCare AI
# ANVISA + OpenFDA + IA Médica
# ===========================================

from fastapi import APIRouter
from services.interactions_engine import gerar_relatorio

router = APIRouter(
    prefix="/interacoes",
    tags=["💊 Interações Medicamentosas"]
)

@router.get("/{medicamento}")
async def verificar_interacoes(medicamento: str):
    """
    🔍 Consulta completa de análise medicamentosa:
    1. Busca ANVISA
    2. Busca FDA
    3. Fusão dos dados
    4. IA gera relatório clínico útil
    """
    resultado = gerar_relatorio(medicamento)
    
    return {
        "medicamento": medicamento.upper(),
        "fonte_principal": "ANVISA + OpenFDA",
        "relatorio_clinico": resultado
    }
