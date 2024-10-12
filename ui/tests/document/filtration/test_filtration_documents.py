from pytest_testrail.plugin import pytestrail
from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.filtration.filtration import FiltrationPage


class TestFiltrationDocuments:
    """
    Тесты для фильтрации документов в поиске***
    """

    @pytestrail.case("C20012198")
    def test_filtration_documents_by_date(self, app, login_user):
        """Фильтрация документов по дате."""
        app.filter.select_filters()
        app.filter.entering_date_for_filtering_documents()
        app.filter.go_to_document_type()
        app.filter.select_document_type(doc_type=FiltrationPage.DOCUMENT_TYPE_EA_123)
        app.filter.add_document_types(added_doc_type=FiltrationPage.SELECTED_DOCUMENT_TYPE,
                                      doc_type_name=DocumentNotice.DOCUMENT_TYPE_EA_123)
        app.filter.document_search()
        app.filter.assert_document_sorting_by_data()
