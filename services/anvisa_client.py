# services/anvisa_client.py
import requests, pdfplumber, io
from bs4 import BeautifulSoup

BASE_URL = "https://consultas.anvisa.gov.br/api/"


def buscar_bula(medicamento: str) -> str:
    """Baixa a bula real da Anvisa em PDF, extrai todo o texto e retorna a bula completa"""
    # 1) Buscar medicamento no bulário
    url = f"{BASE_URL}consultaMedicamento?nomeProduto={medicamento}"
    r = requests.get(url, timeout=15)

    if r.status_code != 200:
        return "❌ Não foi possível acessar o servidor da ANVISA."

    dados = r.json()
    if not dados or "content" not in dados or len(dados["content"]) == 0:
        return "❌ Nenhum medicamento encontrado na ANVISA."

    medicamento_id = dados["content"][0]["idProduto"]
    
    # 2) Buscar link da bula mais recente
    bula_url = f"{BASE_URL}bulario/{medicamento_id}"
    bula_res = requests.get(bula_url)

    if bula_res.status_code != 200:
        return "❌ Bula não encontrada para este medicamento."

    bula_data = bula_res.json()

    # PDF link
    pdf_link = bula_data.get("urlPdf")
    if not pdf_link:
        return "❌ Não existe PDF para este medicamento."

    # 3) Baixar PDF real
    pdf_bytes = requests.get(pdf_link).content

    # 4) Extrair texto da bula
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        texto = "\n".join(page.extract_text() for page in pdf.pages)

    return texto or "⚠ Não foi possível extrair o texto da bula."
