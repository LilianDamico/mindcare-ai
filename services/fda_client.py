import requests

BASE_URL = "https://api.fda.gov/drug/label.json"

def buscar_fda(medicamento: str):
    query = f"{BASE_URL}?search={medicamento}&limit=1"

    try:
        res = requests.get(query).json()
        if "results" not in res:
            return None

        data = res["results"][0]

        return {
            "interacoes": data.get("drug_interactions"),
            "advertencias": data.get("warnings"),
            "contraindicacoes": data.get("contraindications"),
            "reacoes_adversas": data.get("adverse_reactions"),
            "posologia": data.get("dosage_and_administration"),
            "gravidez": data.get("pregnancy"),
            "pediatria": data.get("pediatric_use"),
            "idosos": data.get("geriatric_use"),
        }

    except Exception:
        return None
