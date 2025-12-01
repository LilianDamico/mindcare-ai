import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Carrega o arquivo .env manualmente
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

class Settings(BaseSettings):
    OPENAI_API_KEY: str

    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"

settings = Settings()

# DEBUG TEMPORÁRIO — pode remover depois
print("\n🔐 STATUS DA OPENAI KEY:", "OK ✔" if settings.OPENAI_API_KEY else "NÃO ENCONTRADA ❌", "\n")
