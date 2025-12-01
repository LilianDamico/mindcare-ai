# ===========================================
# services/knowledge_harvester.py
# "Caçador" de fontes extras de informação
# para complementar ANVISA + OpenFDA (MindCare)
#
# Integração com PubMed (NCBI E-utilities)
# ===========================================

from typing import List
import os
import requests
import xml.etree.ElementTree as ET

PUBMED_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def _get_pubmed_api_params() -> dict:
    """
    Alguns parâmetros opcionais recomendados pelo NCBI:
      - email: para identificação do cliente
      - tool: nome da aplicação
    Podem ser configurados via variável de ambiente, mas não são obrigatórios.
    """
    email = os.getenv("PUBMED_EMAIL", "")
    tool = os.getenv("PUBMED_TOOL", "mindcare-ai")

    params = {}
    if email:
        params["email"] = email
    if tool:
        params["tool"] = tool

    return params


def buscar_pubmed_resumos(medicamento: str, max_artigos: int = 3) -> List[str]:
    """
    Busca artigos no PubMed relacionados ao medicamento e retorna
    uma lista de textos estruturados contendo título + resumo.

    Estratégia de busca:
      - nome do medicamento no título/resumo
      - combinando com termos de interações, efeitos adversos, etc.

    Exemplo de query:
      "sibutramine[Title/Abstract] AND (drug interactions OR adverse effects)"

    O retorno é uma lista de strings que serão concatenadas no contexto
    usado pelo LLM no motor de interações.
    """

    textos: List[str] = []

    try:
        # -------------------------
        # 1) ESEARCH - obter IDs
        # -------------------------
        base_params = _get_pubmed_api_params()

        term = (
            f'{medicamento}[Title/Abstract] AND '
            f'(drug interactions OR adverse effects OR safety OR toxicity)'
        )

        esearch_params = {
            "db": "pubmed",
            "retmode": "json",
            "retmax": str(max_artigos),
            "term": term,
        }
        esearch_params.update(base_params)

        esearch_resp = requests.get(PUBMED_ESEARCH_URL, params=esearch_params, timeout=10)
        esearch_resp.raise_for_status()
        esearch_json = esearch_resp.json()

        id_list = esearch_json.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return textos  # nenhum artigo encontrado

        # -------------------------
        # 2) EFETCH - buscar detalhes
        # -------------------------
        efetch_params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "xml",
        }
        efetch_params.update(base_params)

        efetch_resp = requests.get(PUBMED_EFETCH_URL, params=efetch_params, timeout=15)
        efetch_resp.raise_for_status()

        root = ET.fromstring(efetch_resp.text)

        for article in root.findall(".//PubmedArticle"):
            article_title_el = article.find(".//ArticleTitle")
            abstract_els = article.findall(".//Abstract/AbstractText")

            title = article_title_el.text if article_title_el is not None else "Título não disponível"

            # Abstract pode vir em vários blocos; juntamos tudo
            abstract_parts = []
            for a in abstract_els:
                # algumas vezes vem em atributo "Label" ou "NlmCategory"
                label = a.attrib.get("Label") or a.attrib.get("NlmCategory")
                text = a.text or ""
                if label:
                    abstract_parts.append(f"{label}: {text}")
                else:
                    abstract_parts.append(text)

            abstract = "\n".join(abstract_parts).strip()

            if not abstract:
                continue  # se não tem resumo, normalmente pouco útil para IA

            texto = f"""
[TEXTO PUBMED]
Título: {title}

Resumo:
{abstract}
"""
            textos.append(texto)

        return textos

    except Exception as e:
        # Em produção você pode logar isso com logger estruturado
        print(f"[PubMed] Erro ao buscar artigos para '{medicamento}': {e}")
        return textos


def buscar_guidelines_clinicas(medicamento: str) -> List[str]:
    """
    Ponto de extensão para diretrizes clínicas / guidelines.

    Por enquanto, deixamos como stub (sem implementação).
    No futuro você pode:
      - ler PDFs convertidos em texto
      - buscar em um banco próprio
      - usar um índice vetorial

    O formato de retorno é o mesmo: lista de blocos de texto.
    """
    # TODO: implementar busca em base própria de guidelines, se desejar.
    return []


def coletar_fontes_extras(medicamento: str) -> List[str]:
    """
    Orquestra a coleta ativa:
      - Literatura (PubMed / artigos científicos)
      - Guidelines / consensos (quando implementado)

    Retorna uma lista de blocos de texto para serem concatenados
    no contexto mandado ao LLM.
    """
    textos: List[str] = []

    textos_pubmed = buscar_pubmed_resumos(medicamento)
    textos_guidelines = buscar_guidelines_clinicas(medicamento)

    textos.extend(textos_pubmed)
    textos.extend(textos_guidelines)

    # filtra vazios, só por garantia
    textos = [t for t in textos if t and t.strip()]

    return textos
