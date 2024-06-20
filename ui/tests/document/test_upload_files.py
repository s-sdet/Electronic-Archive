import pytest
from pytest_testrail.plugin import pytestrail

from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.documents import DocumentsPage


class TestUploadFiles:
    """
    Тесты для загрузки файлов и инструкций
    https://electronicarchive-frontend-afds.dev.akbars.ru/document
    """

    @pytest.mark.lp
    @pytestrail.case("C15000420")
    def test_upload_file_in_document(self, app, login_user, create_document):
        """Тест загрузка файла из карточки документа."""
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data=create_document)
        app.document.open_document()
        app.document.upload_file(file_name=DocumentNotice.FILE_NAME_PNG)
