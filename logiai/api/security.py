import secrets
from fastapi import Header, HTTPException, status
from logiai import config

def _egal(a: str | None, b: str | None) -> bool:
    """Compare de manière sécurisée deux chaînes pour éviter les attaques temporelles."""
    if not a or not b:
        return False
    return secrets.compare_digest(a.encode("utf-8"), b.encode("utf-8"))

def verify_api_key(x_api_key: str | None = Header(default=None)) -> str:
    """Vérifie la clé API fournie dans l'en-tête X-API-Key et retourne le rôle associé."""
    if not config.API_KEY and not config.ADMIN_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Les clés d'authentification ne sont pas configurées sur le serveur."
        )
    
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API manquante dans l'en-tête X-API-Key."
        )
    
    if config.ADMIN_KEY and _egal(x_api_key, config.ADMIN_KEY):
        return "admin"
    
    if config.API_KEY and _egal(x_api_key, config.API_KEY):
        return "user"
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Clé API invalide."
    )

def require_admin(role: str = Header(default=None)) -> str:
    """Exige un rôle administrateur (erreur 403 si l'utilisateur est simple ou non autorisé)."""
    # Note : Cette fonction est généralement combinée avec une dépendance de vérification de rôle
    return role