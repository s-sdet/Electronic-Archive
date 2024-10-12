import pytest
from pytest_testrail.plugin import pytestrail
from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.sorting.sorting import SortingPage


class TestSortingDocuments:
    """
    Тесты для сортировки документов в поиске***
    """

    @pytestrail.case("C19875714")
    @pytest.mark.skip(reason="Переведен в статус Obsolete")
    def test_sorting_documents_by_date(self, app, login_user):
        """Сортировка документов по дате."""
        app.filter.add_document_type(doc_type=SortingPage.DOCUMENT_TYPE_EA_123,
                                     added_doc_type=SortingPage.SELECTED_DOCUMENT_TYPE,
                                     doc_type_name=DocumentNotice.DOCUMENT_TYPE_EA_123)
        app.filter.document_search()
        app.sort.assert_document_sorting_by_ascending_order(date_locator=SortingPage.DATES_MODIFIED)
        app.sort.assert_document_sorting_by_descending_order(date_locator=SortingPage.DATES_MODIFIED)
