import pytest
from pytest_testrail.plugin import pytestrail
from ui.fixtures.pages.document.documents import DocumentsPage
from ui.fixtures.pages.document.filtration.filtration import FiltrationPage


class TestValidationDocuments:
    """
    Тесты для валидации документов***
    """

    @pytestrail.case("C18760112")
    @pytest.mark.parametrize("application_number, notice", DocumentsPage.DATA_FOR_VALIDATION_APPLICATION_NUMBER)
    def test_validation_application_number_in_document(self, app, create_document_with_all_fields, application_number,
                                                       notice):
        """Тест валидации поля "№ заявки АС ОКЗ" в документе."""
        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=create_document_with_all_fields)
        app.document.document_open()
        app.document.metadata_editing()
        app.document.add_application_number(application_number=application_number)
        app.document.save_document()
        app.document.assertion_document_save(notice=notice)
