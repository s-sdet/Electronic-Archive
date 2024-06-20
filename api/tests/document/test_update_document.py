import pytest
from pytest_testrail.plugin import pytestrail
from api.fixtures.document.document import Document
from api.fixtures.document_type.document_type import DocumentType
from api.data.constants import ApiVersions


class TestsUpdateDocument:
    """Тесты обновления/изменения данных в документах."""

    @pytestrail.case("C20772591")
    @pytest.mark.parametrize("doc_type_name, doc_name, metadata_type, metadata_type_value, new_doc_name",
                             Document.DATA_FOR_UPDATE_DOCUMENT_WITHOUT_FILE_TYPE_AND_METADATA_TYPE)
    def test_update_document_name(self, app, auth, doc_type_name, doc_name, metadata_type, metadata_type_value,
                                  new_doc_name):
        """Тест обновления имени документа содержащее < 64 валидных символов."""
        doc_type = app.doc_type.create_doc_type(url_api=ApiVersions.API_V4, header=auth,
                                                data=DocumentType.data_for_create_document_type_without_metadata_type(
                                                    doc_type_name=doc_type_name))
        doc = app.doc.create_document(header=auth,
                                      data=Document.data_for_creating_document_with_required_metadata_type(
                                          doc_type_id=doc_type["result"]["id"], name=doc_name,
                                          metadata_type=metadata_type, metadata_type_value=metadata_type_value))
        assert "documentId" and "documentVersionId" in doc["result"]
        assert doc["result"]["name"] == doc_name
        renamed_doc = app.doc.update_document(header=auth,
                                              data=Document.data_for_updating_document(
                                                  doc_id=doc["result"]["documentId"], name=new_doc_name,
                                                  metadata_type=metadata_type, metadata_type_value=metadata_type_value))
        assert renamed_doc["result"]["documentId"] == doc["result"]["documentId"]
        assert renamed_doc["result"]["name"] == new_doc_name

    @pytestrail.case("C20772594", "C20772649")
    @pytest.mark.parametrize("doc_type_name, is_required, metadata_type_name, display_name, metadata_type, "
                             "regular_expression, regular_expression_value, doc_name, doc_metadata_type, "
                             "metadata_type_value, new_doc_name, new_metadata_type, new_metadata_type_value",
                             Document.DATA_FOR_CREATE_DOCUMENT_NOT_CONTAINING_METADATA_TYPES)
    def test_update_document_and_metadata_types(
            self, app, auth, doc_type_name, is_required, metadata_type_name, display_name, metadata_type,
            regular_expression, regular_expression_value, doc_name, doc_metadata_type, metadata_type_value,
            new_doc_name, new_metadata_type, new_metadata_type_value):
        """
        Обновление данных документа и типов метаданных:
        "C20772594" - Обновление документа не содержащее типы метаданных;
        "C20772649" - Обновление документа содержащего типы метаданных;
        """
        doc_type = app.doc_type.create_doc_type(
            url_api=ApiVersions.API_V4, header=auth, data=DocumentType.data_to_create_document_type_with_metadata_type(
                doc_type_name=doc_type_name, is_required=is_required, metadata_type_name=metadata_type_name,
                display_name=display_name, metadata_type=metadata_type, regular_expression=regular_expression,
                regular_expression_value=regular_expression_value))
        doc = app.doc.create_document(
            url_api=ApiVersions.API_V4, header=auth,
            data=Document.data_for_creating_document_with_required_metadata_type(
                doc_type_id=doc_type["result"]["id"], name=doc_name, metadata_type=doc_metadata_type,
                metadata_type_value=metadata_type_value))
        assert "documentId" and "documentVersionId" in doc["result"]
        assert doc["result"]["name"] == doc_name
        renamed_doc = app.doc.update_document(
            header=auth, data=Document.data_for_updating_document(
                doc_id=doc["result"]["documentId"], name=new_doc_name, metadata_type=new_metadata_type,
                metadata_type_value=new_metadata_type_value))
        assert renamed_doc["result"]["documentId"] == doc["result"]["documentId"]
        assert renamed_doc["result"]["name"] == new_doc_name
        assert renamed_doc["result"]["documentProperties"][f"{new_metadata_type}"] == new_metadata_type_value

    @pytestrail.case("C20772667", "C20772850")
    @pytest.mark.parametrize(
        "doc_type_name, name_first_system_file, display_name_first_system_file, first_file_type,"
        "name_second_system_file, display_name_second_system_file, second_file_type, regular_expression, expression,"
        "doc_name, first_metadata_type, first_metadata_type_value, second_metadata_type, second_metadata_type_value,"
        "new_first_metadata_type, new_first_metadata_type_value, new_second_metadata_type,"
        "new_second_metadata_type_value",
        DocumentType.DATA_FOR_CREATE_DOCUMENT_TYPE_WITH_TWO_TYPE_METADATA)
    def test_update_document_with_multiple_metadata_types(
            self, app, auth, doc_type_name, name_first_system_file, display_name_first_system_file, first_file_type,
            name_second_system_file, display_name_second_system_file, second_file_type, regular_expression, expression,
            doc_name, first_metadata_type, first_metadata_type_value, second_metadata_type, second_metadata_type_value,
            new_first_metadata_type, new_first_metadata_type_value, new_second_metadata_type,
            new_second_metadata_type_value):
        """
        Тесты обновления документов:
            "C20772667": содержащих несколько типов метаданных;
            "C20772850": с добавлением нового типа метаданных;
        """
        doc_type = app.doc_type.create_doc_type(
            url_api=ApiVersions.API_V4, header=auth,
            data=DocumentType.data_for_create_document_type_with_two_type_metadata(
                doc_type_name=doc_type_name, name_first_system_file=name_first_system_file,
                display_name_first_system_file=display_name_first_system_file, first_file_type=first_file_type,
                name_second_system_file=name_second_system_file,  second_file_type=second_file_type,
                display_name_second_system_file=display_name_second_system_file, regular_expression=regular_expression,
                expression=expression))
        doc = app.doc.create_document(
            url_api=ApiVersions.API_V4, header=auth,
            data=Document.data_for_creating_document_with_multiple_types(
                doc_type_id=doc_type["result"]["id"], name=doc_name, first_metadata_type=first_metadata_type,
                first_metadata_type_value=first_metadata_type_value, second_metadata_type=second_metadata_type,
                second_metadata_type_value=second_metadata_type_value))
        assert "documentId" and "documentVersionId" in doc["result"]
        assert doc["result"]["name"] == doc_name
        renamed_doc = app.doc.update_document(
            header=auth, data=Document.data_for_update_document_with_multiple_types(
                doc_id=doc["result"]["documentId"], name=doc_name, first_metadata_type=new_first_metadata_type,
                first_metadata_type_value=new_first_metadata_type_value, second_metadata_type=new_second_metadata_type,
                second_metadata_type_value=new_second_metadata_type_value))
        assert renamed_doc["result"]["documentId"] == doc["result"]["documentId"]
        assert renamed_doc["result"]["documentProperties"][
                   f"{new_second_metadata_type}"] == new_second_metadata_type_value
