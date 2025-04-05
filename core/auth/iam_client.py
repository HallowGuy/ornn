
import os

def get_current_user():
    """
    Simule la récupération d'un utilisateur depuis le module IAM d'Intalio.
    Dans une future version, cette fonction pourra interroger l'API IAM sécurisée.
    """
    return {
        "username": os.getenv("ORNN_USER", "utilisateur_demo"),
        "email": os.getenv("ORNN_EMAIL", "demo@intalio.com"),
        "roles": os.getenv("ORNN_ROLES", "ROLE_ANALYSTE,ROLE_VIEWER").split(","),
        "groups": os.getenv("ORNN_GROUPS", "FRANCE").split(","),
        "authenticated": True
    }

def is_authorized(required_roles):
    """
    Vérifie si l'utilisateur courant possède au moins un des rôles requis.
    """
    user = get_current_user()
    return any(role in user['roles'] for role in required_roles)
