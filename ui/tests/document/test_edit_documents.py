import time
import pytest
from pytest_testrail.plugin import pytestrail
from ui.data.constants import DocumentNotice
from ui.fixtures.pages.document.documents import DocumentsPage


class TestEditDocuments:
    """
    Тесты для редактирования документов на странице поиска документов
    https://electronicarchive-frontend-afds.dev.akbars.ru/document/search
    """

    @pytest.mark.lp
    @pytestrail.case("C15000418")
    def test_editing_primary_and_secondary_document_metadata(self, app, login_user, random_document_data):
        """
        Тест редактирования основных и дополнительных метаданных документа.
        :param random_document_data: Рандомные генерируемые значения для редактируемого документа.
        """
        app.document.add_document_type(document_type=DocumentsPage.SELECT_DOCUMENT_TYPE_WITH_2_FIELDS,
                                       document_type_locator=DocumentsPage.SELECT_DOCUMENT_TYPE_WITH_2_FIELDS,
                                       document_type_name=DocumentNotice.DOCUMENT_TYPE_WITH_2_FIELDS)
        app.document.open_document()
        app.document.editing_document(document_data=random_document_data)

    @pytest.mark.lp
    @pytestrail.case("C15000421", "C19119798")
    def test_make_file_in_document_actual(self, app, login_user, create_document_with_png_file):
        """
        C15000421: Тест сделать файл актуальным
        C19119798: Тест установки актуальности файла в версии документа
        Тест сделать файл в документе актуальным.
        :param create_document_with_png_file: Фикстура создания документа с файлом в статусе неактуальный.
        """
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data=create_document_with_png_file)
        app.document.open_document()
        app.document.change_file_relevance(locator_button_dropdown_menu=DocumentsPage.LINK_MAKE_FILE_UP_TO_DATE)
        app.document.assertion_file_is_up_to_date()  # Проверка, что файл стал актуальным

    @pytest.mark.lp
    @pytestrail.case("C19119801")
    def test_make_file_in_document_irrelevant(self, app, login_user, create_document_with_png_file):
        """
        Тест снятия актуальности файла в версии документа.
        :param create_document_with_png_file: Фикстура создания документа с файлом в статусе неактуальный.
        """
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data=create_document_with_png_file)
        app.document.open_document()

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
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data=DocumentNotice.DOCUMENT_WITH_TWO_VERSIONS)
        app.document.open_document()
        app.document.select_document_version()

    @pytest.mark.lp
    @pytestrail.case("C14968870")
    def test_assert_modification_document_date_after_editing(self, app, login_user, create_document_with_all_fields):
        """Тест проверки изменения даты после редактирования документа."""
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data=create_document_with_all_fields)
        app.document.document_search()
        date_create_doc = app.document.get_document_modification_date()
        app.document.document_open()
        time.sleep(60)  # Минута ожидания необходима, чтобы дата создания документа изменилась на дату редактирования
        app.document.metadata_editing()
        app.document.add_document_date()
        app.document.save_document()
        app.document.go_to_doc_search()
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data="")
        app.document.document_search()
        assert app.document.get_document_modification_date() != date_create_doc

    @pytest.mark.lp
    @pytestrail.case("C14968871")
    def test_assert_modification_document_date_after_downloading_file(self, app, login_user,
                                                                      create_document_with_all_fields):
        """Тест проверки обновление даты изменения документа после загрузки файла."""
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data=create_document_with_all_fields)
        app.document.document_search()
        date_create_doc = app.document.get_document_modification_date()
        app.document.document_open()
        time.sleep(60)  # Минута ожидания необходима, чтобы дата создания документа изменилась на дату редактирования
        app.document.upload_file(file_name="upload_file.png")
        app.document.go_to_doc_search()
        app.document.data_entry_for_search_document(locator=DocumentsPage.LOCATORS_METADATA_TO_SEARCH_DOCUMENT["5"],
                                                    document_data="")
        app.document.document_search()
        assert app.document.get_document_modification_date() != date_create_doc
