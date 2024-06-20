import pytest
from pytest_testrail.plugin import pytestrail


class TestCopyDocumentsType:
    """
    Тесты для копирования типов документов
    https://electronicarchive-frontend-afds.dev.akbars.ru/administration
    """

    @pytest.mark.lp
    @pytestrail.case("C14969030")
    def test_copy_document_type(self, app, create_doc_type):
        """Тест копирования типа документа."""
        app.doc_type.copy_document_type(type_name=create_doc_type)
        app.doc_type.save_copy_document_type()
        app.doc_type.delete_document_type(type_name=create_doc_type)
