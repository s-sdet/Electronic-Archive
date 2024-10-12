import pytest
from pytest_testrail.plugin import pytestrail
from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.filtration.filtration import FiltrationPage


class TestUploadFiles:
    """
    Тесты для загрузки файлов и инструкций***
    """

    @pytest.mark.lp
    @pytestrail.case("C15000420")
    def test_upload_file_in_document(self, app, create_document):
        """Тест загрузка файла из карточки документа."""
        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=create_document)
        app.document.document_open()
        app.document.upload_file(file_name=DocumentNotice.FILE_NAME_PNG)
