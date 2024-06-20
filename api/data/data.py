from dataclasses import dataclass


@dataclass
class AuthorizeIS4:
    """Данные для авторизации в IS4."""
    client_id = "individuals_electronic_archive"
    redirect_uri = "***"
    response_type = "code"
    scope = "***"
    state = "***"
    nonce = "***"
    code_challenge = "***"
    code_challenge_method = "***"
    response_mode = "***"


@dataclass
class Auth:
    """Данные для получения токена."""
    client_id = "individuals_electronic_archive"
    grant_type = "authorization_code"
    code_verifier = "***"
    scope = "****"
    redirect_uri = "***"
    login = ""
    password = ""
    client_secret_key = ""
