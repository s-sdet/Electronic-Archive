import pytest
import logging
from requests import request
from api.fixtures.app import App
from api.data.data import Auth
from api.fixtures.document.document import Document
from api.fixtures.document_type.document_type import DocumentType
from api.fixtures.validation.validation import Validation
from api.data.constants import ApiVersions, DocumentTypeNotice, FileNotice

logger = logging.getLogger("Live Plus. Electronic Archive")


def pytest_addoption(parser):
    parser.addoption(
        "--api-url",
        action="store",
        default="***",  # DEV
        # default="***",  # STAGE Kuber
        help="DEV API url",
    )


@pytest.fixture
def app(request):
    url = request.config.getoption('--api-url')
    logger.info(f"Старт API теста, URL: {url}")
    return App(url)


@pytest.fixture(scope="function")
def create_document_type(app, auth, doc_type=DocumentTypeNotice(), file=FileNotice()):
    """Фикстура создания типа документа."""
    res = app.doc_type.create_doc_type(
        url_api=ApiVersions.API_V4,
        header=auth,
        data=Validation.creating_document_type(doc_type_name=doc_type.doc_type_name_latin,
                                               file_name=file.file_type_name_latin)
    )
    return res


@pytest.fixture(scope="function")
def doc_type_without_file_type(app, auth, url_api=ApiVersions.API_V4, doc_type=DocumentTypeNotice()):
    """Фикстура создания типа документа без метаданных."""
    res = app.doc_type.create_doc_type(
        url_api=url_api,
        header=auth,
        data=DocumentType.data_for_create_document_type_without_metadata_type(
            doc_type_name=doc_type.doc_type_name_latin))
    return res


@pytest.fixture(scope="function")
def doc_type_without_file_type_in_v3(app, auth, url_api=ApiVersions.API_V3):
    """Фикстура создания типа документа без метаданных в API v3."""
    res = app.doc_type.create_doc_type(
        url_api=url_api,
        header=auth,
        data=DocumentType.data_for_create_document_type_without_metadata_type())
    return res


@pytest.fixture(scope="function")
def doc_type_with_file_type(app, auth, doc_type=DocumentTypeNotice()):
    """Фикстура создания типа документа с типом файла и без типа метаданных."""
    res = app.doc_type.create_doc_type(
        url_api=ApiVersions.API_V4,
        header=auth,
        data=DocumentType.data_for_create_document_type_with_metadata(
            doc_type_name=doc_type.doc_type_name_latin,
            system_file_name=doc_type.doc_type_name_cyrillic, extensions=[".pdf", ".txt"]))
    return res


@pytest.fixture(scope="function")
def doc_without_properties(app, auth, doc_type_without_file_type):
    """Фикстура создания документа без documentProperties."""
    res = app.doc.create_document(header=auth,
                                  data=Document.data_for_creating_document_with_required_metadata_type(
                                      doc_type_id=doc_type_without_file_type["result"]["id"], name="Тестовый документ",
                                      metadata_type=None, metadata_type_value=None))
    return res


@pytest.fixture(scope="function")
def auth(app):
    """Фикстура авторизации в API v4."""
    headers = {
        'Content-Type': '***',
        'X-LiveSpace-Role': '***',
        'X-Origin': '***'
    }
    return headers


@pytest.fixture(scope="function")
def auth_form_data(app):
    """Фикстура авторизации в API v4."""
    headers = {
        'Content-Type': '***',
        'X-LiveSpace-Role': '***',
        'X-Origin': '***'
    }
    return headers


@pytest.fixture
def token_is4(app):
    """Фикстура получения токена."""
    url_is4 = "***"

    payload = {'client_id': Auth.client_id,
               'grant_type': Auth.grant_type,
               'scope': Auth.scope,
               'code_verifier': Auth.code_verifier,
               'username': Auth.login,
               'password': Auth.password
               }

    request("POST", url=url_is4, data=payload, verify=False)
