import pytest
from pytest_testrail.plugin import pytestrail
from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.filtration.filtration import FiltrationPage


class TestSearchDocuments:
    """
    Тесты для поиска документов на странице поиска документов***
    """

    @pytest.mark.lp
    @pytestrail.case("C14652540")
    def test_document_search_by_document_type(self, app, login_user):
        """Тест поиска документа по типу документа."""
        app.filter.add_document_type(doc_type=FiltrationPage.DOCUMENT_TYPE_EA_123,
                                     added_doc_type=FiltrationPage.SELECTED_DOCUMENT_TYPE,
                                     doc_type_name=DocumentNotice.DOCUMENT_TYPE_EA_123)
        app.filter.document_search()

    @pytest.mark.lp
    @pytestrail.case("C14858547")
    def test_search_document_by_metadata(self, app, create_document):
        """
        Тест поиска документа по нескольким значениям статических метаданных.
        Поиск документа выполняется после его создания.
        :param create_document: Фикстура создания документа.
        """
        app.filter.search_document_by_all_metadata(document_data=create_document)

    @pytest.mark.lp
    @pytestrail.case("C17606433")
    def test_search_only_signed_documents(self, app, login_user):
        """Тест поиск только подписанных документов."""
        app.filter.select_filters()
        app.filter.select_only_signed()
        app.filter.go_to_document_type()
        app.filter.select_document_type(doc_type=FiltrationPage.DOCUMENT_TYPE_FOR_SIGN)
        app.filter.add_document_types(added_doc_type=FiltrationPage.SELECTED_DOCUMENT_TYPE,
                                      doc_type_name=DocumentNotice.DOCUMENT_TYPE_FOR_SIGN)
        app.filter.document_search()
        app.document.document_open()
        app.document.checking_electronic_signature_of_document()
