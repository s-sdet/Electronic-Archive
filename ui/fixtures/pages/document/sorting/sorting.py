import logging
from selenium.webdriver.common.by import By
from ui.fixtures.pages.base_page import BasePage
from ui.data.constants import DocumentNotice

logger = logging.getLogger("Electronic Archive")


class SortingPage(BasePage):
    """Страница поиска - сортировка документов https://electronicarchive-frontend-afds.dev.akbars.ru/document/search"""

    # Ссылки
    LINK_SEARCH_DOCUMENT = (By.XPATH, "//a[contains(text(), 'Хранилище документов')]")  # Ссылка на поиск документов

    # Кнопки
    BUTTON_ADD_DOCUMENT_TYPE = (By.XPATH, "//span[contains(text(), 'Добавить тип документа')]")  # Добавить тип док-та
    BUTTON_SELECT = (By.XPATH, "//span[contains(text(), 'Выбрать')]")  # Выбрать
    BUTTON_SEARCH = (By.XPATH, "//span[contains(text(), 'Найти')]")  # Найти

    # Заголовки окон и форм
    TITLE_DOCUMENT_TYPE_SELECTION_WINDOW = (By.XPATH, "//div[@class='Dialog-Header']/h4")  # Окно выбора типа документа

    # Заголовки столбцов в таблице результатов поиска
    COLUMN_DATE_MODIFIED = (By.XPATH, "//div[contains(text(), 'Дата изменения')]")  # заголовок столбца "дата изменения"
    SEARCH_RESULT = (By.XPATH, "//h2[contains(text(), 'Результат поиска')]")  # Заголовок окна результатов поиска

    DATES_MODIFIED = (By.XPATH, "//tbody[@class='MuiTableBody-root']/tr/td[3]/span")  # Дата изменения

    def go_to_doc_search(self):
        """Переход в раздел поиска документов"""
        self.click(locator=self.LINK_SEARCH_DOCUMENT)

    def select_two_document_types(self, document_type):
        """
        Добавление типа документа для поиска;
        :param document_type: тип документа;
        """
        self.element_is_enabled(locator=self.BUTTON_ADD_DOCUMENT_TYPE)  # Ожидание появления элемента
        self.click(locator=self.BUTTON_ADD_DOCUMENT_TYPE)  # Клик по кнопке "Добавить тип документа"
        self.assertion_window_opening()
        self.click(locator=document_type)  # Выбор нужного типа документа из списка

    def add_document_types(self, document_type_locator, document_type):
        """
        Добавление типа документа для поиска;
        :param document_type_locator: локатора типа документа;
        :param document_type: название типа документа.
        """
        self.click(locator=self.BUTTON_SELECT)  # Клик по кнопке "Выбрать"
        self.assertion_document_selection(document_type_locator=document_type_locator, document_type=document_type)

    def assertion_window_opening(self):
        """Проверка и логирование успешного открытия окна выбора типа документа."""
        self.element_is_enabled(locator=self.TITLE_DOCUMENT_TYPE_SELECTION_WINDOW)  # Ожидание появления элемента
        logger.info(f"Заголовок окна: {self.get_text(locator=self.TITLE_DOCUMENT_TYPE_SELECTION_WINDOW)}")
        assert self.get_text(
            locator=self.TITLE_DOCUMENT_TYPE_SELECTION_WINDOW) == DocumentNotice.TITLE_DOCUMENT_TYPE_SELECTION_WINDOW

    def assertion_document_selection(self, document_type_locator=None, document_type=None):
        """
        Проверка и логирование успешного выбора типа документа;
        :param document_type_locator: локатора типа документа;
        :param document_type: название типа документа.
        """
        logger.info(f"Выбран тип документа: {document_type_locator}")
        # Проверка, что выбрался нужный документ
        self.element_is_enabled(locator=document_type_locator)  # Ожидание появления элемента
        assert self.get_text(locator=document_type_locator) == document_type

    def document_search(self):
        """Поиск документа с уже выбранным типом документа."""
        self.click(locator=self.BUTTON_SEARCH)  # Клик по кнопке "Найти" для поиска документов
        self.assertion_go_to_search_page()

    def assertion_go_to_search_page(self):
        """Проверка и логирование успешного перехода на страницу поиска документа."""
        logger.info(f"Заголовок окна: {self.get_text(locator=self.SEARCH_RESULT)}")
        # Проверка, что произошел переход на страницу результатов поиска документа
        assert self.get_text(locator=self.SEARCH_RESULT) == DocumentNotice.SEARCH_RESULT

    def sort_by_date(self):
        """Сортировка документов по дате."""
        self.element_is_enabled(locator=self.COLUMN_DATE_MODIFIED)  # Ожидание элемента
        self.click(locator=self.COLUMN_DATE_MODIFIED)

    def assert_document_sorting_by_ascending_order(self, date_locator=None):
        """Проверка сортировки документов в результатах поиска по возрастанию."""
        self.element_is_enabled(locator=date_locator)  # Ожидание элемента
        logger.info(f"Список дат: {self.get_texts(locator=date_locator)}")
        unsorted_list = self.get_texts(locator=date_locator)  # Получение списка дат
        self.sort_by_date()
        self.element_is_enabled(locator=date_locator)  # Ожидание элемента
        logger.info(f"Список дат по возрастанию: {self.get_texts(locator=date_locator)}")
        sorted_list = self.get_texts(locator=date_locator)  # Получение списка дат
        assert unsorted_list != sorted_list

    def assert_document_sorting_by_descending_order(self, date_locator=None):
        """Проверка сортировки документов в результатах поиска по убыванию."""
        self.element_is_enabled(locator=date_locator)  # Ожидание элемента
        logger.info(f"Список дат по возрастанию: {self.get_texts(locator=date_locator)}")
        unsorted_list = self.get_texts(locator=date_locator)  # Получение списка дат
        self.sort_by_date()
        self.element_is_enabled(locator=date_locator)  # Ожидание элемента
        logger.info(f"Список дат по убыванию: {self.get_texts(locator=date_locator)}")
        sorted_list = self.get_texts(locator=date_locator)  # Получение списка дат
        assert unsorted_list != sorted_list
