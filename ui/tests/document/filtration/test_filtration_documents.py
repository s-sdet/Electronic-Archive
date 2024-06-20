from pytest_testrail.plugin import pytestrail
from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.documents import DocumentsPage


class TestFiltrationDocuments:
    """
    Тесты для фильтрации документов в поиске
    https://electronicarchive-frontend-afds.dev.akbars.ru/document/search
    """

    @pytestrail.case("C20012198")
    def test_filtration_documents_by_date(self, app, login_user):
        """Фмльтрация документов по дате."""
        app.document.go_to_doc_search()
        app.filter.entering_date_for_filtering_documents()
        app.sort.select_two_document_types(document_type=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123)
        app.sort.add_document_types(document_type_locator=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123,
                                    document_type=DocumentNotice.DOCUMENT_TYPE_EA_123)
        app.document.document_search()
        app.filter.assert_document_sorting_by_data()
