
import os
from dotenv import load_dotenv
from pathlib import Path

# Charger les variables depuis .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    # Informations sur l'utilisateur simulé
    USERNAME = os.getenv("ORNN_USER", "utilisateur_demo")
    EMAIL = os.getenv("ORNN_EMAIL", "demo@intalio.com")
    ROLES = os.getenv("ORNN_ROLES", "ROLE_ANALYSTE").split(",")
    GROUPS = os.getenv("ORNN_GROUPS", "FRANCE").split(",")

    # Paramètres d'import/export
    INPUT_PATH = os.getenv("ORNN_INPUT_PATH", "data/input_examples/")
    OUTPUT_PATH = os.getenv("ORNN_OUTPUT_PATH", "data/output_examples/")

    # Configuration API externe (placeholder pour plus tard)
    API_BASE_URL = os.getenv("ORNN_API_BASE_URL", "http://localhost:8000")
    TIMEOUT = int(os.getenv("ORNN_API_TIMEOUT", "10"))

    # Autres paramètres globaux
    DEBUG = os.getenv("ORNN_DEBUG", "false").lower() == "true"

settings = Settings()
