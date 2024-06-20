import pytest
from pytest_testrail.plugin import pytestrail
from ui.fixtures.pages.document.documents import DocumentsPage


class TestViewingDocuments:
    """
    Тесты для проверки отображение документов и их файлов
    https://electronicarchive-frontend-afds.dev.akbars.ru/document
    """

    @pytest.mark.lp
    @pytestrail.case("C19039637")
    def test_display_last_uploaded_document_version_file(self, app, create_document_with_different_extensions):
        """Тест успешного отображение(скачивание) последнего загруженного файла версии документа."""
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data=create_document_with_different_extensions)
        app.document.open_document()
        app.document.assertion_display_preview_file()

    @pytest.mark.lp
    @pytestrail.case("C18863178")
    @pytest.mark.xfail(reason="Возможно падение из-за невозможности прикрепления более 1 файла к документу.")
    def test_display_last_uploaded_4_files_with_different_extensions(self, app, create_document_with_4_files):
        """
        Тест отображение в карточке документа ранее загруженных файлов с разными расширениями в режиме предпросмотра.
        :param create_document_with_4_files: Фикстура создания документа с 4 файлами разных расширений.
        """
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data=create_document_with_4_files)
        app.document.open_document()
        app.document.assertion_display_of_4_files_previews()

    @pytest.mark.lp
    @pytestrail.case("C18862852")
    def test_display_files_with_different_extensions(self, app, create_document_with_different_extensions):
        """Тест отображения в карточке документа файлов с разными расширениями в режиме предпросмотра при их загрузке"""
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data=create_document_with_different_extensions)
        app.document.open_document()
        for file_name in ["upload_file.pdf", "upload_file.jpeg", "upload_file.jpg", "upload_file.png"]:
            app.document.upload_file(file_name=file_name)
