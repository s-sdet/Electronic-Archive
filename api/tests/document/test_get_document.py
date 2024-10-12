import pytest
from pytest_testrail.plugin import pytestrail
from api.fixtures.document.document import Document
from api.fixtures.assertions import Assertions
from api.data.constants import ApiVersions
from api.fixtures.document_type.document_type import DocumentType
from api.fixtures.document_version.document_version import DocumentVersion


class TestsGetDocument:
    """Тесты получения документов, их версий и файлов."""

    @pytestrail.case("C19002657")
    def test_get_document_ist_versions_files_by_document_id(self, app, auth, url_api=ApiVersions.API_V2):
        """API V2.0. Получение документа со списком его версий и файлов по documentId."""

        # Создание типа документа с типом метаданных и без типа файлов
        doc_type = app.doc_type.create_doc_type(url_api=url_api, header=auth,
                                                data=DocumentType.data_for_create_document_type_without_metadata_type())

        # Создание документа и его версии в тестовом Типе документа "CoreTeam"
        document = app.doc.create_document(
            url_api=ApiVersions.API_V2,
            header=auth,
            data=Document.data_for_create_document_and_its_version_in_test_document_type(
                doc_type_id=doc_type["result"]["id"])
        )

        # Создание еще 1 версии в уже созданном документе
        first_doc_ver = app.doc_ver.create_document_version(
            url_api=url_api,
            header=auth,
            data=DocumentVersion.data_for_creating_version_in_created_document(doc_id=document['result']['documentId'])
        )

        # Создание еще 1 версии в уже созданном документе
        second_doc_ver = app.doc_ver.create_document_version(
            url_api=url_api,
            header=auth,
            data=DocumentVersion.data_for_creating_version_in_created_document(doc_id=document['result']['documentId'])
        )

        # Получение информации о документе с указанием его версий и файлов, передав id созданного документа (шаг 1)
        get_doc = app.doc.get_data_by_document_version_id(
            url_api=Document.URL_API_V2_DOCUMENT,
            doc_ver_id=document['result']['documentId']
        )
        Assertions.assert_get_document_ist_versions_files_by_document_id(document=document, first_doc_ver=first_doc_ver,
                                                                         second_doc_ver=second_doc_ver, get_doc=get_doc,
                                                                         create_document_type=doc_type)

    @pytest.mark.lp
    @pytestrail.case("C19034913")
    def test_get_document_versions_by_filters(
            self, app, auth, doc_type_without_file_type, page_size=10, url_api=ApiVersions.API_V2):
        """Получение версий документа по фильтрам."""

        # Создание документа и его версии в тестовом Типе документа "CoreTeam"
        ver_1 = document = app.doc.create_document(
            url_api=url_api, header=auth, data=Document.data_for_create_document_and_its_version_in_test_document_type(
                doc_type_id=doc_type_without_file_type["result"]["id"]))

        # Создание еще 1 версии в уже созданном документе
        ver_2 = app.doc_ver.create_document_version(
            url_api=url_api, header=auth, data=DocumentVersion.data_for_creating_version_in_created_document(
                doc_id=document['result']['documentId']))

        doc_ver = app.doc_ver.get_document_versions(
            header=auth, api_version=url_api,
            query_string=DocumentVersion.URL_FILTER_FOR_GET_DOCUMENT_VERSION_BY_TYPE.format(
                doc_type=doc_type_without_file_type["result"]["id"], page_size=page_size)
        )
        assert doc_ver["result"]["data"][0]["id"] == ver_1["result"]["documentVersionId"]
        assert doc_ver["result"]["data"][1]["id"] == ver_2["result"]["id"]

    @pytestrail.case("C17124307")
    def test_get_documents_by_filter_with_1_related_reason(self, app, auth, page_number=1, page_size=10):
        """Тест получения списка документов с применением фильтра по 1 связанной сущности."""
        res = app.doc.get_documents_by_entities(api_version=ApiVersions.API_V3,
                                                query_string=Document.URL_DOCUMENT_ENTITIES.format(
                                                        Document.CREDIT_DOSSIER, page_number, page_size))
        assert res["result"]["data"][0]["documentEntities"][0]["documentEntityType"] == 1
        assert res["result"]["data"][0]["documentEntities"][0]["entityKey"] == "string"

    @pytestrail.case("C17125098")
    def test_get_document_with_list_ist_versions_and_files_by_document_id(self, app, auth, doc_type_without_file_type,
                                                                          quantity_files=1):
        """Тест получения документа со списком его версий и файлов по documentId."""
        file = app.file.upload_files_in_api_v3(quantity_files=quantity_files)
        doc = app.doc.create_document(data=Document.data_for_creating_document_with_expire_and_source_date(
            doc_type_id=doc_type_without_file_type["result"]["id"], file_id=file["result"]["files"][0]["id"]))
        get_doc = app.doc.get_doc_info_by_doc_id(api_version=ApiVersions.API_V3, doc_id=doc["result"]["documentId"])
        Assertions.assertion_document_version_and_file_information(res=get_doc)

    @pytestrail.case("C21081176", "C21115551")
    def test_get_document_by_id_with_all_versions(self, app, auth, doc_without_properties, api="api/v4.0/"):
        """Тест получения документа по ID со списком всех версий."""
        app.file.upload_files(doc_id=doc_without_properties["result"]["documentId"], file_type_id="", quantity_files=1)
        doc = app.doc.get_doc_info_by_doc_id(doc_id=doc_without_properties["result"]["documentId"], api_version=api)
        Assertions.assert_get_document_by_id_with_all_versions(res=doc)

    @pytestrail.case("C21081178")
    def test_get_document_by_id_version(self, app, auth, doc_without_properties, api="api/v4.0/"):
        """Тест получения документа по ID версии."""
        update_doc = app.doc.update_document(
            data=app.doc.data_for_updating_document(
                doc_id=doc_without_properties["result"]["documentId"], name="Обновленный документ", metadata_type=None,
                metadata_type_value=None))
        get_doc = app.doc.get_doc_info_by_doc_id(doc_id=update_doc["result"]["documentId"], api_version=api)
        assert "versions" in get_doc["result"]
        assert "isActual" not in get_doc["result"]

        get_version = app.doc.get_document_by_version_id(url_api=api, ver_id=get_doc["result"]["versions"][0]["id"])
        assert "documentTypeId" in get_version["result"]
        assert "files" in get_version["result"]
        assert "documentEntities" not in get_version["result"]
