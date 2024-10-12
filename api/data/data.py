from dataclasses import dataclass


@dataclass
class AuthorizeIS4:
    """Данные для авторизации в IS4."""
    client_id = "***"
    redirect_uri = "***"
    response_type = "***"
    scope = "***"
    state = "***"
    nonce = "***"
    code_challenge = "***"
    code_challenge_method = "***"
    response_mode = "***"


@dataclass
class Auth:
    """Данные для получения токена."""
    client_id = "***"
    grant_type = "***"
    code_verifier = "***"
    scope = "***"
    redirect_uri = "***"
    login = ""
    password = ""
    client_secret_key = ""
