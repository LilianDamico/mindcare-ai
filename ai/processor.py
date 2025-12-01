from ai.model import gerar_resposta

def analisar_interacoes(texto_bula: str):
    prompt = f"""
    Você é um farmacêutico clínico especialista em interações medicamentosas.
    Analise a bula abaixo e responda com estrutura objetiva, em MARKDOWN.

    BULA:
    {texto_bula}

    Responda com o seguinte formato:

    ## 💊 Interações Medicamentosas Principais
    - ...

    ## 🧬 Mecanismos
    - Como ocorre a interação?

    ## ⚠ Riscos Clínicos
    - Quais efeitos adversos podem ocorrer?

    ## 🔄 Recomendações para o Profissional
    - condutas — dose, substituição, monitoramento

    ## 🧾 Conclusão
    - Resumo final de segurança

    """
    resposta = gerar_resposta(prompt)
    return resposta.strip()
