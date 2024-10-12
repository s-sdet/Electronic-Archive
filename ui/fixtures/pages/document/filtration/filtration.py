import logging
from selenium.webdriver.common.by import By
from ui.data.constants import FilterNotice, DocumentNotice
from ui.fixtures.pages.base_page import BasePage

logger = logging.getLogger("Electronic Archive")


class FiltrationPage(BasePage):
    """Страница поиска - фильтрация документов ***"""

    # Поля ввода данных
    FIELD_DATE_FROM = (By.XPATH, "//span[text()='От:']//following::input")  # Ввод даты документа "от"
    FIELD_DATE_TO = (By.XPATH, "//span[text()='До:']//following::input")  # Ввод даты документа "до"
    FIELD_DATE_PERIOD = (By.XPATH, "//span[text()='Период изменения']//following::input")  # Поле периода изменения

    # Кнопки
    BUTTON_SELECT_FILTERS = (By.XPATH, "//span[text()='Выбрать фильтры']")  # Кнопка "Выбрать фильтры"
    BUTTON_ADD_DOCUMENT_TYPE = (By.XPATH, "//span[contains(text(), 'Выберите тип документа')]")  # Добавить тип док-та
    BUTTON_ADD_TO_FILTER = (By.XPATH, "//span[contains(text(), 'Добавить в фильтр')]")  # Добавить в фильтр
    BUTTON_APPLY = (By.XPATH, "//span[contains(text(), 'Применить')]")  # Применить

    # Заголовки окон и форм
    TITLE_FILTERS = (By.XPATH, "//h2[@class='Drawer-Title']")  # Заголовок окна фильтров
    TITLE_DOCUMENT_TYPE_SELECTION_WINDOW = (By.XPATH, "//h2[contains(text(), 'Выбор типа документа')]")  # Окно выбора
    TITLE_SEARCH_RESULT = (By.XPATH, "//h2[contains(text(), 'Результат поиска')]")  # Заголовок окна результатов поиска

    # Вкладки
    TAB_DOCUMENT_TYPE = (By.XPATH, "//span[text()='Тип Документа']")  # Вкладка Тип Документа в фильтре

    # Типы документов
    DOCUMENT_TYPE_EA_123 = (By.XPATH, "//span[contains(text(), 'ЭА 123')]//preceding::label[1]")
    DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS = (
        By.XPATH, "//span[text()='Тип документа с разными расширениями']//preceding::label[1]")
    DOCUMENT_TYPE_WITH_2_FIELDS = (
        By.XPATH, "//span[contains(text(), 'Тестовый тип документа с 2 дополнительными полями')]//preceding::label[1]")
    DOCUMENT_TYPE_FOR_SIGN = (By.XPATH, "//span[contains(text(), 'For Sign')]//preceding::label[1]")

    # Ссылки
    LINK_SEARCH_PAGE = (By.XPATH, "//div[@id='root']//nav/div[2]/div")  # Ссылка на поиск документов

    # Чекбокс
    CHECKBOX_ONLY_SIGNED = (By.XPATH, "//span[contains(text(), 'Только подписанные')]")  # Только подписанные

    DATES_MODIFIED = (By.XPATH, "//tbody[@class='TableBody']/tr/td[3]")  # Дата изменения
    SELECTED_DOCUMENT_TYPE = (By.XPATH, "//div[@class='Accordion-SummaryContent']//p")  # Выбранный тип документа

    # Поля метаданных поиска документа через фильтр
    FIELDS_FOR_SEARCH_DOCUMENT = {
        "OKZ_NUMBER":         (By.NAME, "okzRequestNumber"),  # № Заявки
        "ACCOUNT_NUMBER":     (By.NAME, "accountNumber"),  # № счета
        "REFERENCE_NUMBER":   (By.NAME, "applicationId"),  # № обращения
        "CONTRACT_NUMBER":    (By.NAME, "creditContractNumber"),  # № договора
        "CARD_NUMBER":        (By.NAME, "debitCardNumber"),  # ID карты
        "CRM_CLIENT_ID":      (By.NAME, "crmClientId")   # ID клиента
    }

    # Данные и метаданные в результатах поиска документов
    DATA_IN_SEARCH_RESULT = {
        "NAME":             (By.XPATH, "//tbody[@class='TableBody']//td[2]"),  # Название
        "DATE":             (By.XPATH, "//tbody[@class='TableBody']//td[3]"),  # Дата изменения
        "DOC_TYPE":         (By.XPATH, "//tbody[@class='TableBody']//td[4]"),  # Тип документа
        "OKZ_NUMBER":       (By.XPATH, "//tbody[@class='TableBody']//td[5]"),  # № Заявки
        "ACCOUNT_NUMBER":   (By.XPATH, "//tbody[@class='TableBody']//td[6]"),  # № счета
        "REFERENCE_NUMBER": (By.XPATH, "//tbody[@class='TableBody']//td[7]"),  # № обращения
        "CONTRACT_NUMBER":  (By.XPATH, "//tbody[@class='TableBody']//td[8]"),  # № договора
        "CARD_NUMBER":      (By.XPATH, "//tbody[@class='TableBody']//td[9]"),  # ID карты
        "CRM_CLIENT_ID":    (By.XPATH, "//tbody[@class='TableBody']//td[10]")  # ID клиента
    }

    def add_document_type(self, doc_type, added_doc_type, doc_type_name):
        """
        Добавления типа документа в фильтр.
        :param doc_type: Добавляемый тип документа;
        :param added_doc_type: Добавленный тип документа;
        :param doc_type_name: Название типа документа для проверки правильности выбора;
        """
        self.select_filters()
        self.go_to_document_type()
        self.select_document_type(doc_type=doc_type)
        self.add_document_types(added_doc_type=added_doc_type, doc_type_name=doc_type_name)

    def search_document_by_metadata(self, locator, document_data):
        """Поиск документа по метаданным."""
        self.select_filters()
        self.entering_data_for_search_document(locator=locator, document_data=document_data)
        self.document_search()

    def select_filters(self):
        """Выбор фильтров в поиске документов."""
        self.element_is_enabled(locator=self.BUTTON_SELECT_FILTERS)  # Ожидание появления элемента
        self.click(locator=self.BUTTON_SELECT_FILTERS)

        # Проверка открытия окна выбора фильтров
        self.element_is_enabled(locator=self.TITLE_FILTERS)  # Ожидание элемента
        logger.info(f"Заголовок окна: {self.get_text(locator=self.TITLE_FILTERS)}")
        assert self.get_text(locator=self.TITLE_FILTERS) == FilterNotice.TITLE_FILTERS

    def select_only_signed(self):
        """Выбрать только подписанные документы."""
        self.click(locator=self.CHECKBOX_ONLY_SIGNED)  # Клик по чекбоксу "Только подписанные"

    def entering_date_for_filtering_documents(self, date="01.01.202431.12.2024"):
        """
        Ввод даты 'от' и 'до' для фильтрации документов в поиске по дате изменения.
        :param date: Период даты от и до
        """
        self.element_is_enabled(locator=self.FIELD_DATE_PERIOD)  # Ожидание появления элемента
        self.send_keys(locator=self.FIELD_DATE_PERIOD, value=date)  # Ввод периода дат от и до

    def entering_data_for_search_document(self, locator, document_data):
        """
        Ввод данных в поля метаданных фильтра для поиска документа.
        :param locator: Локатор поля для поиска документа.
        :param document_data: Должен принять сгенерированное значение из фикстуры создания документа.
        """
        self.send_keys(locator=locator, value=document_data)  # Ввод значения в поля для поиска документа

    def go_to_document_type(self):
        """Переход на вкладку выбора типа документа."""
        self.element_is_enabled(locator=self.TAB_DOCUMENT_TYPE)  # Ожидание появления элемента
        self.click(locator=self.TAB_DOCUMENT_TYPE)

    def select_document_type(self, doc_type):
        """
        Выбор типа документа для поиска;
        :param doc_type: Добавляемый тип документа;
        """
        self.element_is_enabled(locator=self.BUTTON_ADD_DOCUMENT_TYPE)  # Ожидание появления элемента
        self.click(locator=self.BUTTON_ADD_DOCUMENT_TYPE)  # Клик по кнопке "Добавить тип документа"
        self.assertion_window_opening()
        self.click(locator=doc_type)  # Выбор нужного типа документа из списка

    def assertion_window_opening(self):
        """Проверка и логирование успешного открытия окна выбора типа документа."""
        self.element_is_enabled(locator=self.TITLE_DOCUMENT_TYPE_SELECTION_WINDOW)  # Ожидание появления элемента
        logger.info(f"Заголовок окна: {self.get_text(locator=self.TITLE_DOCUMENT_TYPE_SELECTION_WINDOW)}")
        assert self.get_text(
            locator=self.TITLE_DOCUMENT_TYPE_SELECTION_WINDOW) == DocumentNotice.TITLE_DOCUMENT_TYPE_SELECTION_WINDOW

    def add_document_types(self, added_doc_type, doc_type_name):
        """
        Добавление типа документа для поиска;
        :param added_doc_type: Добавляемый локатор типа документа;
        :param doc_type_name: Название типа документа.
        """
        self.element_is_enabled(locator=self.BUTTON_ADD_TO_FILTER)  # Ожидание появления элемента
        self.click(locator=self.BUTTON_ADD_TO_FILTER)  # Клик по кнопке "Добавить в фильтр"
        self.assertion_document_type_selection(added_doc_type=added_doc_type, doc_type_name=doc_type_name)

    def assertion_document_type_selection(self, added_doc_type=None, doc_type_name=None):
        """
        Проверка и логирование успешного выбора типа документа;
        :param added_doc_type: Добавляемый локатор типа документа;
        :param doc_type_name: Название типа документа.
        """
        logger.info(f"Выбран тип документа: {self.get_text(locator=added_doc_type)}")
        # Проверка, что выбрался нужный документ
        self.element_is_enabled(locator=added_doc_type)  # Ожидание появления элемента
        assert self.get_text(locator=added_doc_type) == doc_type_name

    def document_search(self):
        """Поиск документа с уже выбранным типом документа."""
        self.element_is_enabled(locator=self.BUTTON_APPLY)  # Ожидание элемента
        self.click(locator=self.BUTTON_APPLY)  # Клик по кнопке "Применить" для поиска документов
        self.assertion_go_to_search_page()

    def search_document_by_all_metadata(self, document_data):
        """
        Ввод данных в поля для поиска документа.
        Цикл проходит по всем полям по которым можно найти документ, проверяя корректность данных документа.
        :param document_data: Принимает возвращаемые генерируемые данные из фикстуры создания документа.
        """
        for index, locator in enumerate(self.FIELDS_FOR_SEARCH_DOCUMENT.values(), start=5):
            self.select_filters()
            self.send_keys(locator=locator, value=document_data)  # Ввод значения в поля метаданных для поиска документа
            self.document_search()

            # Проверяем, что значения полей найденного документа равны значениям при создании документа
            table_cell_locator = (By.XPATH, f"//tbody[@class='TableBody']//td[{index}]")
            self.element_is_enabled(locator=table_cell_locator)  # Ожидание элемента
            assert self.get_text(locator=table_cell_locator) == document_data

            # Переход в раздел поиска документов
            self.element_is_enabled(locator=self.LINK_SEARCH_PAGE)  # Ожидание элемента
            self.click(locator=self.LINK_SEARCH_PAGE)

    def assertion_go_to_search_page(self):
        """Проверка и логирование успешного перехода на страницу поиска документа."""
        logger.info(f"Заголовок окна: {self.get_text(locator=self.TITLE_SEARCH_RESULT)}")
        # Проверка, что произошел переход на страницу результатов поиска документа
        assert self.get_text(locator=self.TITLE_SEARCH_RESULT) == DocumentNotice.SEARCH_RESULT

    def assert_document_sorting_by_data(self, year="2024"):
        """
        Проверка сортировки документов в результатах поиска по дате.
        :param year: Для проверки, что в результатах поиска найдены документы только с этим годом.
        """
        self.element_is_enabled(locator=self.DATES_MODIFIED)  # Ожидание появления элемента
        for date in self.get_texts(locator=self.DATES_MODIFIED):
            assert year in date
