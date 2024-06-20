import pytest
import logging
from requests import request
from api.fixtures.app import App
from api.data.data import Auth
from api.fixtures.validation.validation import Validation
from api.data.constants import ApiVersions, DocumentTypeNotice

logger = logging.getLogger("Live Plus. Electronic Archive")


def pytest_addoption(parser):
    parser.addoption(
        "--api-url",
        action="store",
        default="https://documentservice-afds.dev.akbars.ru/",
        help="DEV API url",
    )


@pytest.fixture
def app(request):
    url = request.config.getoption('--api-url')
    logger.info(f"Start API tests Electronic Archive, url is {url}")
    return App(url)


@pytest.fixture(scope="function")
def create_document_type(app, auth):
    """Фикстура создания типа документа."""
    res = app.doc_type.create_doc_type(
        url_api=ApiVersions.API_V4,
        header=auth,
        data=Validation.creating_document_type(doc_type_name=DocumentTypeNotice.NAME_LATIN,
                                               file_name=DocumentTypeNotice.FILE_TYPE_NAME_LATIN)
    )
    return res


@pytest.fixture(scope="function")
def auth(app):
    """Фикстура авторизации в API v4."""
    headers = {
        'Content-Type': 'application/json',
        'X-LiveSpace-Role': 'AFDS-Document-Storage-Administrator-EA',
        'X-Origin': '.'
    }
    return headers


@pytest.fixture
def token_is4(app):
    """Фикстура получения токена."""
    url_is4 = "https://identity-server-is4.dev.akbars.ru/connect/userinfo"

    payload = {'client_id': Auth.client_id,
               'grant_type': Auth.grant_type,
               'scope': Auth.scope,
               'code_verifier': Auth.code_verifier,
               'username': Auth.login,
               'password': Auth.password
               }

    request("POST", url=url_is4, data=payload, verify=False)
