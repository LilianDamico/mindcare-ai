# ===========================================
# services/interactions_engine.py
# Motor de Interações Medicamentosas
# ANVISA + OpenFDA + Fontes Extras + IA
# ===========================================

from typing import Optional, Dict, Any, List

from services.anvisa_client import buscar_bula
from services.fda_client import buscar_fda
from services.knowledge_harvester import coletar_fontes_extras
from ai.processor import analisar_interacoes


def _montar_contexto_fusao(
    medicamento: str,
    bula_anvisa: Optional[str],
    fda_data: Optional[Dict[str, Any]],
    fontes_extras: List[str],
) -> str:
    """
    Monta um contexto único combinando:
      - Texto da bula da ANVISA (quando disponível)
      - Campos clínicos do OpenFDA (interações, reações, etc.)
      - Textos adicionais de literatura / guidelines (extração ativa)
    """

    # ===== ANVISA =====
    anvisa_section = (
        bula_anvisa
        if bula_anvisa and bula_anvisa.strip()
        else "Nenhum dado relevante encontrado na ANVISA para este medicamento."
    )

    # ===== FDA =====
    if fda_data:
        interacoes = fda_data.get("interacoes") or "Não informado pelo FDA."
        advertencias = fda_data.get("advertencias") or "Não informado pelo FDA."
        contraindicacoes = (
            fda_data.get("contraindicacoes") or "Não informado pelo FDA."
        )
        reacoes_adversas = (
            fda_data.get("reacoes_adversas") or "Não informado pelo FDA."
        )
        posologia = fda_data.get("posologia") or "Não informado pelo FDA."
        gravidez = fda_data.get("gravidez") or "Não informado pelo FDA."
        pediatria = fda_data.get("pediatria") or "Não informado pelo FDA."
        idosos = fda_data.get("idosos") or "Não informado pelo FDA."

        fda_section = f"""
### Dados FDA (EUA) — Possível diferença de nome/composição

- **Interações medicamentosas (FDA):**
{interacoes}

- **Advertências e precauções (FDA):**
{advertencias}

- **Contraindicações (FDA):**
{contraindicacoes}

- **Reações adversas / efeitos colaterais (FDA):**
{reacoes_adversas}

- **Posologia e modo de usar (FDA):**
{posologia}

- **Uso na gravidez (FDA):**
{gravidez}

- **Uso pediátrico (FDA):**
{pediatria}

- **Uso em idosos (FDA):**
{idosos}
"""
    else:
        fda_section = """
### Dados FDA (EUA)

Não foram encontrados registros relevantes no OpenFDA para este medicamento
ou ocorreu alguma falha na obtenção dos dados.
"""

    # ===== FONTES EXTRAS (LITERATURA / GUIDELINES) =====
    if fontes_extras:
        extras_text = "\n\n---\n\n".join(fontes_extras)
        extras_section = f"""
### Fontes adicionais (literatura científica / diretrizes)

Os textos abaixo foram coletados em bases científicas e/ou guidelines.
Eles podem conter descrições de:
- interações medicamentosas
- mecanismos de ação
- efeitos adversos
- recomendações de uso em populações especiais

TEXTOS COLETADOS:

{extras_text}
"""
    else:
        extras_section = """
### Fontes adicionais (literatura científica / diretrizes)

Nenhum texto extra foi coletado para este medicamento
(não foram encontradas referências relevantes ou o coletor ainda
não está configurado para este tipo de busca).
"""

    contexto = f"""
Você é um assistente clínico especializado em farmacologia dentro do sistema MindCare.

Seu objetivo é gerar um RELATÓRIO PROFISSIONAL sobre interações medicamentosas,
riscos clínicos e recomendações de conduta para o medicamento abaixo,
usando SOMENTE as informações presentes neste contexto combinado.

Medicamento pesquisado: {medicamento.upper()}

==================== FONTE 1 — ANVISA (Brasil) ====================

Texto da bula / informações regulatórias brasileiras:
{anvisa_section}

==================== FONTE 2 — OpenFDA (EUA) ====================

{fda_section}

==================== FONTE 3 — LITERATURA / GUIDELINES ====================

{extras_section}

==================== INSTRUÇÕES ====================

1. Compare criticamente os dados da ANVISA, do FDA e das fontes extras.
2. Liste as principais INTERAÇÕES MEDICAMENTOSAS, sempre que possível indicando:
   - medicamento envolvido
   - mecanismo provável da interação
   - consequência clínica (aumento de toxicidade, perda de efeito, etc.)
3. Destaque RISCOS CLÍNICOS importantes (hepatotoxicidade, nefrotoxicidade,
   risco cardiovascular, risco de sangramento, etc.).
4. Dê atenção especial a:
   - gestantes
   - lactantes
   - crianças
   - idosos
   - pacientes com insuficiência renal/hepática
   - pacientes com comorbidades relevantes
   - pacientes em uso de polifarmácia
   - pacientes imunocomprometidos
   - pacientes com doenças crônicas
   - pacientes em uso de medicamentos de alto risco
   - pacientes com histórico de reações adversas graves
   - pacientes em uso de terapias específicas (quimioterapia, imunoterapia, etc.)
   - profissionais de saúde (interações com anestésicos, sedativos, etc.)
   - pacientes com transtornos psiquiátricos
   - pacientes com doenças cardiovasculares
   - pacientes com doenças metabólicas (diabetes, dislipidemias, etc.)
   
5. Quando houver divergência entre fontes, explique brevemente.
6. Nunca invente dados: se algo não estiver claro nas fontes, diga que não há
   informação suficiente.
7. Estruture a saída em Markdown com seções claras, por exemplo:
   - Interações Medicamentosas Principais
   - Mecanismos Prováveis
   - Riscos Clínicos
   - Recomendações para o Profissional
   - Observações sobre Populações Especiais
   - Conclusão

Responda em português, de forma objetiva, técnica e voltada ao profissional de saúde.
"""

    return contexto


def gerar_relatorio(medicamento: str) -> str:
    """
    Pipeline completo:
      1. Busca texto da bula na ANVISA.
      2. Busca dados estruturados no OpenFDA.
      3. Coleta ativa de textos extras (literatura / guidelines).
      4. Monta contexto fusionado.
      5. Envia para o LLM via `analisar_interacoes`.
      6. Retorna o relatório final em Markdown.
    """

    # 1) ANVISA
    bula_anvisa = buscar_bula(medicamento)

    # 2) FDA
    fda_data = buscar_fda(medicamento)

    # 3) Fontes extras (literatura / guidelines)
    fontes_extras = coletar_fontes_extras(medicamento)

    # 4) Monta contexto fusionado
    contexto = _montar_contexto_fusao(
        medicamento=medicamento,
        bula_anvisa=bula_anvisa,
        fda_data=fda_data,
        fontes_extras=fontes_extras,
    )

    # 5) Chama IA para gerar análise
    relatorio_md = analisar_interacoes(contexto)

    return relatorio_md
