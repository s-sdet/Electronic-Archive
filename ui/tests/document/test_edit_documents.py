import time
import pytest
from pytest_testrail.plugin import pytestrail
from selenium.webdriver.common.by import By

from ui.data.constants import DocumentNotice
from ui.fixtures.pages.administration.document_types import CreateDocumentsTypeModel
from ui.fixtures.pages.document.documents import DocumentsPage
from ui.fixtures.pages.document.filtration.filtration import FiltrationPage


class TestEditDocuments:
    """
    Тесты для редактирования документов на странице поиска документов***
    """

    @pytest.mark.lp
    @pytestrail.case("C15000418")
    def test_editing_primary_and_secondary_document_metadata(self, app, login_user, random_document_data):
        """
        Тест редактирования основных и дополнительных метаданных документа.
        :param random_document_data: Рандомные генерируемые значения для редактируемого документа.
        """
        app.filter.add_document_type(doc_type=FiltrationPage.DOCUMENT_TYPE_WITH_2_FIELDS,
                                     added_doc_type=FiltrationPage.SELECTED_DOCUMENT_TYPE,
                                     doc_type_name=DocumentNotice.DOCUMENT_TYPE_WITH_2_FIELDS)
        app.filter.document_search()
        app.document.document_open()
        app.document.editing_document(document_data=random_document_data)

    @pytest.mark.lp
    @pytestrail.case("C15000421", "C19119798")
    def test_make_file_in_document_actual(self, app, create_document_with_png_file):
        """
        C15000421: Тест сделать файл актуальным
        C19119798: Тест установки актуальности файла в версии документа
        Тест сделать файл в документе актуальным.
        :param create_document_with_png_file: Фикстура создания документа с файлом в статусе неактуальный.
        """
        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=create_document_with_png_file)
        app.document.document_open()
        app.document.change_file_relevance(locator_button_dropdown_menu=DocumentsPage.LINK_MAKE_FILE_UP_TO_DATE)
        app.document.assertion_file_is_up_to_date()  # Проверка, что файл стал актуальным

    @pytest.mark.lp
    @pytestrail.case("C19119801")
    def test_make_file_in_document_irrelevant(self, app, create_document_with_png_file):
        """
        Тест снятия актуальности файла в версии документа.
        :param create_document_with_png_file: Фикстура создания документа с файлом в статусе неактуальный.
        """
        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=create_document_with_png_file)
        app.document.document_open()

        # Перевод файла документа в статус "Актуальный"
        app.document.change_file_relevance(locator_button_dropdown_menu=DocumentsPage.LINK_MAKE_FILE_UP_TO_DATE)
        app.document.assertion_file_is_up_to_date()  # Проверка, что файл стал актуальным

        # Перевод файла документа в статус "Не актуальный"
        app.document.change_file_relevance(locator_button_dropdown_menu=DocumentsPage.LINK_MAKE_FILE_IRRELEVANT)
        app.document.assertion_file_is_out_of_date()  # Проверка, что файл стал неактуальным

    @pytest.mark.lp
    @pytestrail.case("C15000423")
    def test_make_document_version_up_to_actual(self, app, login_user):
        """Тест сделать вторую версию документа актуальной."""
        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=DocumentNotice.DOCUMENT_WITH_TWO_VERSIONS)
        app.document.document_open()
        app.document.select_document_version()

    @pytest.mark.lp
    @pytestrail.case("C14968870")
    def test_assert_modification_document_date_after_editing(self, app, create_document_with_all_fields):
        """Тест проверки изменения даты после редактирования документа."""
        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=create_document_with_all_fields)
        date_create_doc = app.document.get_document_modification_date()
        app.document.document_open()
        time.sleep(60)  # Минута ожидания необходима, чтобы дата создания документа изменилась на дату редактирования
        app.document.metadata_editing()
        app.document.add_document_date()
        app.document.save_document()
        app.document.go_to_doc_search()
        app.filter.select_filters()
        app.filter.entering_data_for_search_document(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                                     document_data="")
        app.filter.document_search()
        assert app.document.get_document_modification_date() != date_create_doc

    @pytest.mark.lp
    @pytestrail.case("C14968871")
    def test_assert_modification_document_date_after_downloading_file(self, app, create_document_with_all_fields):
        """Тест проверки обновление даты изменения документа после загрузки файла."""
        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=create_document_with_all_fields)
        date_create_doc = app.document.get_document_modification_date()
        app.document.document_open()
        time.sleep(61)  # Минута ожидания необходима, чтобы дата создания документа изменилась на дату редактирования
        app.document.upload_file(file_name="upload_file.png")
        app.document.go_to_doc_search()
        app.filter.select_filters()
        app.filter.entering_data_for_search_document(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                                     document_data="")
        app.filter.document_search()
        assert app.document.get_document_modification_date() != date_create_doc

    @pytestrail.case("C20973423", "C20973424")
    @pytest.mark.parametrize("new_name, notice", DocumentsPage.DATA_FOR_INVALID_DOCUMENT_NAME)
    def test_saving_document_with_invalid_name(self, app, create_document, new_name, notice):
        """
        Невалидные тесты сохранения документа при редактировании после создания:
            "C20973423" - Пустое название;
            "C20973424" - Название более 64 символов;
        """
        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=create_document)
        app.document.document_open()
        app.document.rename_document(new_name=new_name)
        app.document.save_document()
        app.document.assertion_document_is_not_save(notice=notice)

    @pytestrail.case("C20973421", "C21641105")
    @pytest.mark.parametrize("new_name, required", DocumentsPage.DATA_FOR_VALIDATION_DOCUMENT_NAME)
    def test_edit_document_name_with_optional_values_in_properties(self, app, go_to_admin_panel, random_document_data,
                                                                   new_name, required):
        """Тест редактирования названия документа с необязательными значениями в свойствах."""
        data = CreateDocumentsTypeModel.random_valid_data_for_doc_type()
        app.doc_type.open_form_doc_type_create()
        app.doc_type.data_entry_doc_type(data=data)
        app.doc_type.data_entry_file_types(data=data)
        app.doc_type.data_entry_metadata_type(data=data, adding_required=required)
        app.doc_type.creation_type()

        app.document.go_to_doc_create()
        app.document.open_form_to_create_document()
        app.document.add_file_for_document(file_name=DocumentNotice.FILE_NAME_PNG)
        app.document.data_entry_to_create_document(
            doc_type=(By.XPATH, f"//div[contains(text(), '{data.document_type_name}')]"),
            document_data=random_document_data)
        app.document.selection_file_type(type_name=(By.XPATH, f"//div[text()='{data.file_type_name}']"))
        app.document.document_create()

        app.filter.search_document_by_metadata(locator=FiltrationPage.FIELDS_FOR_SEARCH_DOCUMENT["OKZ_NUMBER"],
                                               document_data=random_document_data)
        app.document.document_open()
        app.document.rename_document(new_name=new_name)
        app.document.save_document()
