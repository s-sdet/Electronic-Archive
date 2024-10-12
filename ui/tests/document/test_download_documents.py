import pytest
from pytest_testrail.plugin import pytestrail
from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.filtration.filtration import FiltrationPage


class TestDownloadDocuments:
    """
    Тесты для скачивания документов, файлов, инструкций***
    """

    @pytest.mark.lp
    @pytestrail.case("C15000414")
    def test_download_file_in_document_card(self, app, create_document_with_png_file):
        """
        Тест скачивания файла в карточке документа.
        :param create_document_with_png_file: Фикстура создания документа с файлом в статусе неактуальный.
        """
        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=create_document_with_png_file)
        app.document.document_open()
        app.document.download_file()

    @pytest.mark.lp
    @pytestrail.case("C17606436")
    @pytest.mark.xfail(reason="Падает из-за невозможности выбрать более 20 документов на фронте. Баг: LP-2691")
    def test_download_more_20_documents(self, app, login_user):
        """Негативный тест проверки отображение ошибки при скачивании >20 документов с прикрепленными файлами."""
        app.filter.add_document_type(doc_type=FiltrationPage.DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS,
                                     added_doc_type=FiltrationPage.SELECTED_DOCUMENT_TYPE,
                                     doc_type_name=DocumentNotice.DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS)
        app.filter.document_search()
        app.document.select_40_documents()
        app.document.download_documents()
