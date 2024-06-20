import pytest
from pytest_testrail.plugin import pytestrail
from api.fixtures.document.document import Document
from api.fixtures.document_version.document_version import DocumentVersion
from api.fixtures.assertions import Assertions
from api.data.constants import ApiVersions


class TestsGetDocumentVersion:
    """Тесты получения актуальной версии документов."""

    @pytest.mark.lp
    @pytestrail.case("C17126051")
    def test_get_information_about_document_version_by_id(self, app, auth):
        """Тест получения информации о версии документа по ее id."""

        # Создание документа с одной версией
        document = app.doc.create_document(
            url_api=ApiVersions.API_V3,
            header=auth,
            data=Document.json_data_for_creating_document_whit_one_version()
        )

        # Создание дополнительной версии уже созданного документа
        document_version = app.doc_ver.create_document_version(
            url_api=DocumentVersion.URL_API_V3_DOCUMENT_VERSION,
            header=auth,
            data=DocumentVersion.for_creating_minor_version(doc_id=document['result']['documentId'])
        )

        # Получение информации о конкретной версии документа по ее id
        info_version = app.doc_ver.get_info_about_document_version(
            header=auth,
            api_version=DocumentVersion.API_V3,
            doc_ver_id=document_version['result']['id']
        )
        Assertions.assert_document_version_information(document=document, document_version=document_version,
                                                       info_version=info_version)

    @pytest.mark.lp
    @pytestrail.case("C19035740")
    def test_get_document_versions_by_document_type_id(self, app, auth, page_size=10):
        """Получение версий документа по фильтру DocumentTypeId."""
        res = app.doc_ver.get_document_versions(
            header=auth,
            api_version=ApiVersions.API_V2,
            query_string=DocumentVersion.URL_FILTER_FOR_GET_DOCUMENT_VERSION_BY_TYPE_ID.format(page_size)
        )
        assert len(res['result']['data']) == page_size
