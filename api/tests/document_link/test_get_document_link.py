from pytest_testrail.plugin import pytestrail
from api.fixtures.document.document import Document
from api.fixtures.assertions import Assertions
from api.data.constants import ApiVersions
from api.fixtures.document_link.document_link import DocumentLink


class TestsGetDocumentLink:
    """Тесты получения связанных документов с их типами."""

    @pytestrail.case("C17125938")
    def test_get_document_with_list_ist_versions_and_files_by_document_id(
            self, app, auth, doc_type_without_file_type, api=ApiVersions.API_V3):
        """Тест получения связанных документов-родителей с их типами по id документа дочернего."""

        # Создание первого документа
        first_doc = app.doc.create_document(
            url_api=api, header=auth, data=Document.data_for_creating_document_without_properties_and_files(
                doc_type_id=doc_type_without_file_type["result"]["id"]))

        # Создание второго документа
        second_doc = app.doc.create_document(
            url_api=api, header=auth, data=Document.data_for_creating_document_without_properties_and_files(
                doc_type_id=doc_type_without_file_type["result"]["id"]))

        # Создание связи между документами
        document_linking = app.doc_link.document_linking(
            url_api=api, header=auth, data=DocumentLink.data_for_document_linking(
                parent_doc_id=first_doc["result"]["documentId"], child_doc_ids=second_doc["result"]["documentId"]))

        # Получение информации о связанном с ним документе и типа документа для документа-родителя
        get_doc = app.doc_link.get_linked_documents_by_id(
            api_version=api, doc_id=document_linking["result"]["data"][0]["documentId"])
        Assertions.assertion_linked_documents(res=get_doc)
