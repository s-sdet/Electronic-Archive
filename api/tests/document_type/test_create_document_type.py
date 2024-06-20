import pytest
from pytest_testrail.plugin import pytestrail
from api.data.constants import ValidationNotice
from api.fixtures.assertions import Assertions
from api.fixtures.document_type.document_type import DocumentType


class TestsCreateDocumentType:
    """Тесты создания типов документов."""

    @pytestrail.case("C20838718", "C20838720", "C20838721")
    @pytest.mark.parametrize("doc_type_name, system_file_name, allowed_extensions, extensions",
                             DocumentType.VALID_DATA_FOR_DOC_TYPE)
    def test_valid_check_field_extensions_for_file_type(self, app, auth, doc_type_name, system_file_name,
                                                        allowed_extensions, extensions):
        """
        Валидные тесты для проверки поля "Возможные расширения" при передаче:
            "C20838718": пустого поля "Возможные расширения" для типа файла;
            "C20838720": в поле "Возможные расширения" None для типа файла;
            "C20838721": не передавая поле "Возможные расширения" для типа файла;
        """
        res = app.doc_type.create_doc_type(header=auth, data=DocumentType.data_for_create_document_type_with_metadata(
            doc_type_name=doc_type_name, system_file_name=system_file_name, allowed_extensions=allowed_extensions,
            extensions=extensions
        ))
        assert "id" in res["result"]

    @pytestrail.case("C18005506")
    @pytest.mark.parametrize("doc_type_name, system_file_name, allowed_extensions, extensions",
                             DocumentType.INVALID_DATA_FOR_DOC_TYPE)
    def test_invalid_check_field_extensions_for_file_type(self, app, auth, doc_type_name, system_file_name,
                                                          allowed_extensions, extensions):
        """
        Невалидные тесты для проверки поля "Возможные расширения" при передаче:
            "C18005506": в поле "Возможные расширения" для типа файла повторяющиеся расширения;
        """
        res = app.doc_type.create_doc_type(
            response=400, header=auth, data=DocumentType.data_for_create_document_type_with_metadata(
                doc_type_name=doc_type_name, system_file_name=system_file_name, allowed_extensions=allowed_extensions,
                extensions=extensions
            ))
        assert res["errorDetails"]["fileTypes[0].allowedExtensions"][0] == ValidationNotice.ERROR_EXTENSIONS_DUPLICATED
