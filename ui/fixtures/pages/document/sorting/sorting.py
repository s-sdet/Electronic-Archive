import logging
from selenium.webdriver.common.by import By
from ui.fixtures.pages.base_page import BasePage

logger = logging.getLogger("Electronic Archive")


class SortingPage(BasePage):
    """Страница поиска - сортировка документов https://electronicarchive-frontend-afds.dev.akbars.ru/document/search"""

    # Ссылки
    LINK_SEARCH_DOCUMENT = (By.XPATH, "//a[contains(text(), 'Хранилище документов')]")  # Ссылка на поиск документов

    # Кнопки
    BUTTON_ADD_DOCUMENT_TYPE = (By.XPATH, "//span[contains(text(), 'Выберите тип документа')]")  # Добавить тип док-та
    BUTTON_SELECT = (By.XPATH, "//span[contains(text(), 'Выбрать')]")  # Выбрать
    BUTTON_SEARCH = (By.XPATH, "//span[contains(text(), 'Найти')]")  # Найти
    BUTTON_ADD_TO_FILTER = (By.XPATH, "//span[contains(text(), 'Добавить в фильтр')]")  # Добавить в фильтр

    # Заголовки окон и форм
    TITLE_DOCUMENT_TYPE_SELECTION_WINDOW = (By.XPATH, "//h2[contains(text(), 'Выбор типа документа')]")  # Окно выбора

    # Заголовки столбцов в таблице результатов поиска
    COLUMN_DATE_MODIFIED = (By.XPATH, "//div[contains(text(), 'Дата изменения')]")  # заголовок столбца "дата изменения"
    SEARCH_RESULT = (By.XPATH, "//h2[contains(text(), 'Результат поиска')]")  # Заголовок окна результатов поиска

    # Типы документов
    DOCUMENT_TYPE_EA_123 = (By.XPATH, "//span[contains(text(), 'ЭА 123')]//preceding::label[1]")

    DATES_MODIFIED = (By.XPATH, "//tbody[@class='TableBody']/tr/td[3]")  # Дата изменения
    SELECTED_DOCUMENT_TYPE = (By.XPATH, "//div[@class='Accordion-SummaryContent']//p")  # Выбранный тип документа

    def go_to_doc_search(self):
        """Переход в раздел поиска документов"""
        self.click(locator=self.LINK_SEARCH_DOCUMENT)

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
