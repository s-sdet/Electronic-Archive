import pytest
from pytest_testrail.plugin import pytestrail
from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.documents import DocumentsPage


class TestDownloadDocuments:
    """
    Тесты для скачивания документов, файлов, инструкций
    https://electronicarchive-frontend-afds.dev.akbars.ru/document
    """

    @pytest.mark.lp
    @pytestrail.case("C15000414")
    def test_download_file_in_document_card(self, app, login_user, create_document_with_png_file):
        """
        Тест скачивания файла в карточке документа.
        :param create_document_with_png_file: Фикстура создания документа с файлом в статусе неактуальный.
        """
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data=create_document_with_png_file)
        app.document.open_document()
        app.document.download_file()

    @pytest.mark.lp
    @pytestrail.case("C17606436")
    def test_download_more_20_documents(self, app, login_user):
        """Негативный тест проверки отображение ошибки при скачивании >20 документов с прикрепленными файлами."""
        app.document.add_document_type(document_type=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123,
                                       document_type_locator=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123,
                                       document_type_name=DocumentNotice.DOCUMENT_TYPE_EA_123)
        app.document.document_search()
        app.document.select_40_documents()
        app.document.download_documents()

