import logging
from selenium.webdriver.common.by import By
from ui.fixtures.pages.base_page import BasePage
from ui.data.constants import DocumentsTypeNotice

logger = logging.getLogger("Electronic Archive")


class CreatePrecondition(BasePage):
    """Страницы *** для создания сущностей перед прогоном тестов."""

    # Ссылки
    LINK_USER_IN_TAB = (By.XPATH, "//div[@class='sc-bHdvGS ggKXFZ']")  # Ссылка на профиль в верхнем меню
    LINK_TO_ADMIN_PANEL = (By.XPATH, "//span[text()='Администрирование']")  # Ссылка на панель администрирования
    LINK_ADD_GROUPS_AD = (By.XPATH, "//span[text()='Добавить']")  # Ссылка добавить Группы AD

    # Заголовки
    TITLE_ADMIN_PANEL = (By.XPATH, "//h2[text()='Администрирование']")  # Заголовок страницы администрирования
    TITLE_FORM_DOC_TYPE_CREATE = (By.XPATH, "//h2[text()='Создание типа документа']")  # Создание типа документа
    TITLE_ACTION_CONFIRMATION = (By.XPATH, "//div[text()='Подтверждение действий']")  # Заголовок окна подтверждения

    # Кнопки
    BUTTON_CREATE = (By.XPATH, "//span[text()='Создать']")  # Кнопка "Создать"
    BUTTON_CREATE_DOC_TYPE = (By.XPATH, "//span[text()='Тип документа']")  # Кнопка "Тип документа"
    BUTTON_CONFIRM = (By.XPATH, "//span[text()='Подтвердить']")  # Кнопка "Подтвердить"

    # Поля ввода данных
    FILED_DOCUMENT_TYPE_NAME = (By.XPATH, "//input[@name='name']")  # Название типа документа

    # Всплывашки об успешном создании/сохранении сущностей
    SUCCESS_TYPE_CREATE = (By.XPATH, "//div[@id='root']/div/div[2]//span")  # Уведомление успешного создания

    ELEMENT_TO_WAIT_PAGE_TO_LOAD = (By.XPATH, "//div[@class='sc-jnldDj fbeZwT']/div[20]")  # Локатор для ожидания

    def open_admin_panel(self):
        """Переход в панель администрирования."""
        self.click(locator=self.LINK_USER_IN_TAB)  # Клик по профилю в верхнем правом углу
        self.element_is_enabled(locator=self.LINK_TO_ADMIN_PANEL)  # Ожидание элемента
        self.click(locator=self.LINK_TO_ADMIN_PANEL)  # Клик по ссылке "Администрирования"

        # Проверка перехода в панель администрирования
        self.element_is_enabled(locator=self.TITLE_ADMIN_PANEL)  # Ожидание элемента
        assert self.get_text(locator=self.TITLE_ADMIN_PANEL) == DocumentsTypeNotice.TITLE_ADMIN_PANEL

    def open_form_doc_type_create(self):
        """Открытие формы создания типа документа."""
        # Проверка перехода в панель администрирования
        self.element_is_enabled(locator=self.TITLE_ADMIN_PANEL)  # Ожидание загрузки страницы
        assert self.get_text(locator=self.TITLE_ADMIN_PANEL) == DocumentsTypeNotice.TITLE_ADMIN_PANEL

        self.click(locator=self.BUTTON_CREATE)  # Клик по кнопке "Создать"
        self.element_is_enabled(locator=self.BUTTON_CREATE_DOC_TYPE)  # Ожидание элемента
        self.click(locator=self.BUTTON_CREATE_DOC_TYPE)  # Клик по кнопке "Тип документа"

        # Проверка перехода в форму создания типа документа
        self.element_is_enabled(locator=self.TITLE_FORM_DOC_TYPE_CREATE)  # Ожидание элемента
        assert self.get_text(locator=self.TITLE_FORM_DOC_TYPE_CREATE) == DocumentsTypeNotice.TITLE_FORM_DOC_TYPE_CREATE

    def data_entry_doc_type(self, doc_type_name):
        """Заполнение данных в форме названия типа документа."""
        logger.info(f"Название типа документа: {doc_type_name}")
        self.element_is_enabled(locator=self.FILED_DOCUMENT_TYPE_NAME)  # Ожидание элемента
        self.send_keys(locator=self.FILED_DOCUMENT_TYPE_NAME, value=doc_type_name)
        # self.click(locator=self.CHECKBOX_ALLOW_EXTRA_FILE_TYPES)
        # self.click(locator=self.CHECKBOX_ALLOW_EXTRA_PROPERTY_TYPES)

    def creation_type(self):
        """Создание и проверка создания типа файла после заполнения всех полей."""
        self.element_is_enabled(locator=self.BUTTON_CREATE)  # Ожидание элемента
        self.click(locator=self.BUTTON_CREATE)

        # Проверка открытия окна подтверждения
        self.element_is_enabled(locator=self.TITLE_ACTION_CONFIRMATION)  # Ожидание элемента
        logger.info(f"Текст уведомления: {self.get_text(locator=self.TITLE_ACTION_CONFIRMATION)}")
        assert self.get_text(locator=self.TITLE_ACTION_CONFIRMATION) == DocumentsTypeNotice.TITLE_ACTION_CONFIRMATION

        self.click(locator=self.BUTTON_CONFIRM)

        # Проверка появления сообщения об успешном создании
        try:
            self.element_is_enabled(locator=self.SUCCESS_TYPE_CREATE)  # Ожидание элемента
            logger.info(f"Текст уведомления: {self.get_text(locator=self.SUCCESS_TYPE_CREATE)}")
            logger.info(f"Ожидаемый текст уведомления: {DocumentsTypeNotice.SUCCESS_TYPE_CREATE}")
            assert self.get_text(locator=self.SUCCESS_TYPE_CREATE) == DocumentsTypeNotice.SUCCESS_TYPE_CREATE
        except AssertionError:
            logger.info("Такой тип документа уже существует.")
