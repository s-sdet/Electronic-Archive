import pytest
from pytest_testrail.plugin import pytestrail
from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.documents import DocumentsPage


class TestCreateDocuments:
    """
    Тесты для создания документов
    https://electronicarchive-frontend-afds.dev.akbars.ru/document/create
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
    def test_create_document_with_file_and_metadata(self, app, login_user, random_document_data):
        """Тест сохранения документа и его версии с файлом и метаданными."""
        app.document.open_form_to_create_document()
        app.document.data_entry_to_create_document(
            doc_type=DocumentsPage.SELECT_DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS, document_data=random_document_data)
        app.document.selection_file_type(type_name=DocumentsPage.FILE_TYPE_DIFFERENT_EXTENSIONS)
        app.document.add_file_for_document(file_name="upload_file.pdf")
        app.document.document_create()

        # После создания документа выполняется его поиск с нужным типом документа(с которым был создан)
        app.document.add_document_type(
            document_type=DocumentsPage.SELECT_DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS,
            document_type_locator=DocumentsPage.SELECT_DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS,
            document_type_name=DocumentNotice.DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS)
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data=random_document_data)
        app.document.document_search()
        app.document.assertion_document_found(document_data=random_document_data)

    @pytest.mark.lp
    @pytestrail.case("C19119794")
    def test_create_document_with_file_and_additional_metadata(self, app, login_user, random_document_data):
        """Тест сохранения документа и его версии с файлом, метаданными и дополнительными метаданными."""
        app.document.open_form_to_create_document()
        app.document.data_entry_to_create_document(
            doc_type=DocumentsPage.SELECT_DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS, document_data=random_document_data)
        app.document.selection_file_type(type_name=DocumentsPage.FILE_TYPE_DIFFERENT_EXTENSIONS)
        app.document.additional_metadata_entry_to_create_document()
        app.document.add_file_for_document(file_name="upload_file.pdf")
        app.document.document_create()

        # После создания документа выполняется его поиск с нужным типом документа(с которым был создан)
        app.document.add_document_type(
            document_type=DocumentsPage.SELECT_DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS,
            document_type_locator=DocumentsPage.SELECT_DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS,
            document_type_name=DocumentNotice.DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS)
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data=random_document_data)
        app.document.document_search()
        app.document.assertion_document_found(document_data=random_document_data)
