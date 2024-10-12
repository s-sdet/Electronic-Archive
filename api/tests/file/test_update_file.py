from pytest_testrail.plugin import pytestrail
from api.data.constants import DocumentTypeNotice


class TestsUpdateFiles:
    """Тесты обновления файлов в документах."""

    doc_type = DocumentTypeNotice()

    @pytestrail.case("C20836098")
    def test_update_file_in_doc_without_filetype(self, app, auth, doc_without_properties):
        """Тест обновления файлов в документе без указания FileTypeID."""
        app.file.update_files(doc_id=doc_without_properties["result"]["documentId"], quantity_files=1)

        # Получение информации в API v3.0 по документу созданному в API v4.0
        doc_info = app.doc.get_doc_info_by_doc_id(doc_id=doc_without_properties["result"]["documentId"])
        # Проверка, что ID документа созданного в API v4.0 == ID документа полученного в API v3.0
        assert doc_info["result"]["id"] == doc_without_properties["result"]["documentId"]

    @pytestrail.case("C20836851")
    def test_update_file_in_doc_with_filetype(self, app, auth):
        """Тест обновления файлов в документе c указанием FileTypeID."""
        type_id = app.doc_type.create_doc_type(
            header=auth, data=app.doc_type.data_for_create_document_type_with_metadata(
                extensions=[".jpg", ".pdf", ".png"]))
        get_type_id = app.doc_type.get_file_type_id(doc_type_id=type_id["result"]["id"])
        doc = app.doc.create_document(data=app.doc.data_for_creating_document_without_properties_and_files(
            doc_type_id=type_id["result"]["id"]))
        app.file.update_files(doc_id=doc["result"]["documentId"],
                              file_type_id=get_type_id["result"]["fileTypes"][0]["id"], quantity_files=1)

        # Получение информации в API v3.0 по документу созданному в API v4.0
        doc_info = app.doc.get_doc_info_by_doc_id(doc_id=doc["result"]["documentId"])
        # Проверка, что ID документа созданного в API v4.0 == ID документа полученного в API v3.0
        assert doc_info["result"]["id"] == doc["result"]["documentId"]

    @pytestrail.case("C20836882")
    def test_delete_file_in_doc_with_filetype(self, app, auth, auth_form_data):
        """Тест удаление файлов в документе c указанием FileTypeID."""
        type_id = app.doc_type.create_doc_type(
            header=auth, data=app.doc_type.data_for_create_document_type_with_metadata(
                extensions=[".jpg", ".pdf", ".png"]))
        get_type_id = app.doc_type.get_file_type_id(doc_type_id=type_id["result"]["id"])
        doc = app.doc.create_document(data=app.doc.data_for_creating_document_without_properties_and_files(
            doc_type_id=type_id["result"]["id"]))
        app.file.update_files(
            doc_id=doc["result"]["documentId"], file_type_id=get_type_id["result"]["fileTypes"][0]["id"],
            header=auth_form_data, quantity_files=0)

        # Получение информации в API v3.0 по документу созданному в API v4.0
        doc_info = app.doc.get_doc_info_by_doc_id(doc_id=doc["result"]["documentId"])
        # Проверка, что ID документа созданного в API v4.0 == ID документа полученного в API v3.0
        assert doc_info["result"]["id"] == doc["result"]["documentId"]
