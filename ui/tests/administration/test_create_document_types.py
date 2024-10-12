import pytest
from pytest_testrail.plugin import pytestrail
from ui.fixtures.pages.administration.document_types import CreateDocumentsTypeModel


class TestDocumentsType:
    """
    Тесты для типов документов***
    """

    @pytest.mark.lp
    @pytestrail.case("C14969027")
    def test_create_document_type(self, app, go_to_admin_panel):
        """Тест создания нового типа документа."""
        data = CreateDocumentsTypeModel.random_valid_data_for_doc_type()
        app.doc_type.open_form_doc_type_create()
        app.doc_type.data_entry_doc_type(data=data)
        app.doc_type.data_entry_file_types(data=data)
        app.doc_type.data_entry_metadata_type(data=data)
        app.doc_type.creation_type()
