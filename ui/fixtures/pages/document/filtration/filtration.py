import logging
from selenium.webdriver.common.by import By
from ui.fixtures.pages.base_page import BasePage

logger = logging.getLogger("Electronic Archive")


class FiltrationPage(BasePage):
    """Страница поиска - фильтрация документов https://electronicarchive-frontend-afds.dev.akbars.ru/document/search"""

    # Поля ввода данных
    FIELD_DATE_FROM = (By.XPATH, "//span[text()='От:']//following::input")  # Ввод даты документа "от"
    FIELD_DATE_TO = (By.XPATH, "//span[text()='До:']//following::input")  # Ввод даты документа "до"

    DATES_MODIFIED = (By.XPATH, "//tbody[@class='MuiTableBody-root']/tr/td[3]/span")  # Дата изменения

    def entering_date_for_filtering_documents(self, date_from="01.01.2023", date_to="01.12.2023"):
        """
        Ввод даты 'от' и 'до' для фильтрации документов в поиске по дате изменения.
        :param date_from: Дата "от" для фильтрации документов;
        :param date_to: Дата "да" для фильтрации документов;
        """
        self.element_is_enabled(locator=self.FIELD_DATE_FROM)  # Ожидание появления элемента
        self.send_keys(locator=self.FIELD_DATE_FROM, value=date_from)  # Ввод даты изменения документа "от"
        self.click(locator=self.FIELD_DATE_TO)  # Клик в поле "до", чтобы исчезла всплывашка поля "от"
        self.send_keys(locator=self.FIELD_DATE_TO, value=date_to)  # Ввод даты изменения документа "до"

    def assert_document_sorting_by_data(self, year="2023"):
        """
        Проверка сортировки документов в результатах поиска по дате.
        :param year: Для проверки, что в результатах поиска найдены документы только с этим годом.
        """
        self.element_is_enabled(locator=self.DATES_MODIFIED)  # Ожидание появления элемента
        for date in self.get_texts(locator=self.DATES_MODIFIED):
            assert year in date
