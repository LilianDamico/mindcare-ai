from openai import OpenAI
from core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def gerar_resposta(medicamento: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é uma IA especialista em interações medicamentosas baseadas em ANVISA."},
            {"role": "user", "content": f"Liste interações medicamentosas do medicamento: {medicamento}"}
        ]
    )
    return response.choices[0].message.content
