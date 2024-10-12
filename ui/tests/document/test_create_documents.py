import pytest
from pytest_testrail.plugin import pytestrail
from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.documents import DocumentsPage
from ui.fixtures.pages.document.filtration.filtration import FiltrationPage


class TestCreateDocuments:
    """
    Тесты для создания документов***
    """

    def test_create_document(self, app, login_user, random_document_data):
        """
        Валидный тест создания документа с заполнением всех метаданных и значений.
        :param random_document_data: Рандомные генерируемые значения для создаваемого документа.
        """
        app.document.open_form_to_create_document()
        app.document.data_entry_to_create_document(document_data=random_document_data,
                                                   doc_type=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123)
        app.document.document_create()

    @pytestrail.case("C14331653")
    def test_create_document_without_specifying_file_type(self, app, login_user):
        """Тест создания документа без указания типа файла (обязательный) и без файла."""
        app.document.open_form_to_create_document()
        app.document.create_document_without_data(locator_document_type=DocumentsPage.SELECT_DOCUMENT_REQUIRED_TYPE,
                                                  locator_error_required_field=DocumentsPage.ERROR_REQUIRED_FIELD)

    @pytest.mark.lp
    @pytestrail.case("C14642394")
    def test_create_document_with_file_extension_allowed(self, app, login_user):
        """
        Тест создания документа с файлом разрешённого расширения, с выбором типа документа, типа файла,
        с загрузкой файла, без заполнения метаданных.
        """
        app.document.open_form_to_create_document()
        app.document.selection_document_type_in_folder(folder_name=DocumentsPage.FOLDER_DOCUMENT_TYPE_EA,
                                                       type_name=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_PASSPORT_RF)
        app.document.selection_file_type(type_name=DocumentsPage.FILE_TYPE_DOCUMENT_SCAN)
        app.document.add_file_for_document(file_name=DocumentNotice.FILE_NAME_PNG)
        app.document.document_create()

    @pytest.mark.lp
    @pytestrail.case("C19119785")
    def test_create_document_with_file_and_metadata(self, app, create_document_with_pdf_file):
        """Тест сохранения документа и его версии с файлом и метаданными."""
        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=create_document_with_pdf_file)
        app.document.assertion_document_found(locator=FiltrationPage.DATA_IN_SEARCH_RESULT["OKZ_NUMBER"],
                                              document_data=create_document_with_pdf_file)
        app.document.assertion_document_type_found(locator=FiltrationPage.DATA_IN_SEARCH_RESULT["DOC_TYPE"],
                                                   document_type=DocumentNotice.DOCUMENT_TYPE_EA_123)

    @pytest.mark.lp
    @pytestrail.case("C19119794")
    def test_create_document_with_file_and_additional_metadata(self, app, create_document_with_different_extensions):
        """Тест сохранения документа и его версии с файлом, метаданными и дополнительными метаданными."""
        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=create_document_with_different_extensions)
        app.document.assertion_document_found(locator=FiltrationPage.DATA_IN_SEARCH_RESULT["OKZ_NUMBER"],
                                              document_data=create_document_with_different_extensions)
        app.document.assertion_document_type_found(locator=FiltrationPage.DATA_IN_SEARCH_RESULT["DOC_TYPE"],
                                                   document_type=DocumentNotice.DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS)

    @pytestrail.case("C14968869")
    def test_assertion_document_creation_date(self, app, create_document_with_all_fields, document_creation_date):
        """Тест проверки даты создания документа."""
        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=create_document_with_all_fields)
        app.document.get_document_modification_date()
        assert app.document.get_document_modification_date() == document_creation_date
