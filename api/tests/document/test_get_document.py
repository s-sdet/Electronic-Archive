import pytest
from pytest_testrail.plugin import pytestrail
from api.fixtures.document.document import Document
from api.fixtures.assertions import Assertions
from api.data.constants import ApiVersions, DocumentNotice
from api.fixtures.document_version.document_version import DocumentVersion


class TestsGetDocument:
    """Тесты получения документов, их версий и файлов."""

    @pytestrail.case("C19002657")
    def test_get_document_ist_versions_files_by_document_id(self, app, auth):
        """API V2.0. Получение документа со списком его версий и файлов по documentId."""

        # Создание документа и его версии в тестовом Типе документа "CoreTeam"
        document = app.doc.create_document(
            url_api=ApiVersions.API_V2,
            header=auth,
            data=Document.data_for_create_document_and_its_version_in_test_document_type()
        )

        # Создание еще 1 версии в уже созданном документе
        first_doc_ver = app.doc_ver.create_document_version(
            url_api=DocumentVersion.URL_API_V2_DOCUMENT_VERSION,
            header=auth,
            data=DocumentVersion.data_for_creating_version_in_created_document(doc_id=document['result']['documentId'])
        )

        # Создание еще 1 версии в уже созданном документе
        second_doc_ver = app.doc_ver.create_document_version(
            url_api=DocumentVersion.URL_API_V2_DOCUMENT_VERSION,
            header=auth,
            data=DocumentVersion.data_for_creating_version_in_created_document(doc_id=document['result']['documentId'])
        )

        # Получение информации о документе с указанием его версий и файлов, передав id созданного документа (шаг 1)
        get_doc = app.doc.get_data_by_document_version_id(
            url_api=Document.URL_API_V2_DOCUMENT,
            doc_ver_id=document['result']['documentId']
        )
        Assertions.assert_get_document_ist_versions_files_by_document_id(document=document, first_doc_ver=first_doc_ver,
                                                                         second_doc_ver=second_doc_ver, get_doc=get_doc)

    @pytest.mark.lp
    @pytestrail.case("C19034913")
    def test_get_document_versions_by_filters(self, app, auth, page_size=10):
        """Получение версий документа по фильтрам."""

        # Создание документа и его версии в тестовом Типе документа "CoreTeam"
        document = app.doc.create_document(
            url_api=ApiVersions.API_V2,
            header=auth,
            data=Document.data_for_create_document_and_its_version_in_test_document_type()
        )

        # Создание еще 1 версии в уже созданном документе
        app.doc_ver.create_document_version(
            url_api=DocumentVersion.URL_API_V2_DOCUMENT_VERSION,
            header=auth,
            data=DocumentVersion.data_for_creating_version_in_created_document(doc_id=document['result']['documentId'])
        )

        app.doc_ver.get_document_versions(
            header=auth,
            api_version=ApiVersions.API_V2,
            query_string=DocumentVersion.URL_FILTER_FOR_GET_DOCUMENT_VERSION_BY_TYPE.format(page_size)
        )

    @pytestrail.case("C17124307")
    def test_get_documents_by_filter_with_1_related_reason(self, app, auth, page_number=1, page_size=10):
        """Тест получения списка документов с применением фильтра по 1 связанной сущности."""
        res = app.doc.get_documents_by_entities(api_version=ApiVersions.API_V3,
                                                query_string=Document.URL_DOCUMENT_ENTITIES.format(
                                                        Document.CREDIT_DOSSIER, page_number, page_size))
        assert res["result"]["data"][0]["documentEntities"][0]["documentEntityType"] == 1
        assert res["result"]["data"][0]["documentEntities"][0]["entityKey"] == "string"

    @pytestrail.case("C17125098")
    def test_get_document_with_list_ist_versions_and_files_by_document_id(self, app, auth):
        """Тест получения документа со списком его версий и файлов по documentId."""
        res = app.doc.get_doc_info_by_doc_id(api_version=ApiVersions.API_V3,
                                             doc_id=DocumentNotice.DOC_ID)
        Assertions.assertion_document_version_and_file_information(res=res)
