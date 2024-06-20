from pytest_testrail.plugin import pytestrail
from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.documents import DocumentsPage
from ui.fixtures.pages.document.sorting.sorting import SortingPage


class TestSortingDocuments:
    """
    Тесты для сортировки документов в поиске
    https://electronicarchive-frontend-afds.dev.akbars.ru/document/search
    """

    @pytestrail.case("C19875714")
    def test_sorting_documents_by_date(self, app, login_user):
        """Сортировка документов по дате."""
        app.document.go_to_doc_search()
        app.sort.select_two_document_types(document_type=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123)
        app.sort.add_document_types(document_type_locator=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123,
                                    document_type=DocumentNotice.DOCUMENT_TYPE_EA_123)
        app.document.document_search()
        app.sort.assert_document_sorting_by_ascending_order(date_locator=SortingPage.DATES_MODIFIED)
        app.sort.assert_document_sorting_by_descending_order(date_locator=SortingPage.DATES_MODIFIED)
