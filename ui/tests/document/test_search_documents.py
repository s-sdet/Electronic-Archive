import pytest
from pytest_testrail.plugin import pytestrail
from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.documents import DocumentsPage


class TestSearchDocuments:
    """
    Тесты для поиска документов на странице поиска документов
    https://electronicarchive-frontend-afds.dev.akbars.ru/document/search
    """

    @pytest.mark.lp
    @pytestrail.case("C14652540")
    def test_document_search_by_document_type(self, app, login_user):
        """Тест поиска документа по типу документа."""
        app.document.add_document_type(document_type=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123,
                                       document_type_locator=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123,
                                       document_type_name=DocumentNotice.DOCUMENT_TYPE_EA_123)
        app.document.document_search()

    @pytest.mark.lp
    @pytestrail.case("C14858547")
    def test_search_document_by_metadata(self, app, login_user, create_document):
        """
        Тест поиска документа по нескольким значениям статических метаданных.
        Поиск документа выполняется после его создания.
        :param create_document: Фикстура создания документа.
        """
        app.document.data_entry_and_search_document(document_data=create_document)

    @pytest.mark.lp
    @pytestrail.case("C17606433")
    def test_search_only_signed_documents(self, app, login_user):
        """Тест поиск только подписанных документов."""
        app.document.add_document_type(document_type=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123,
                                       document_type_locator=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123,
                                       document_type_name=DocumentNotice.DOCUMENT_TYPE_EA_123)
        app.document.select_only_signed_documents()
        app.document.open_document()
        app.document.checking_electronic_signature_of_document()
