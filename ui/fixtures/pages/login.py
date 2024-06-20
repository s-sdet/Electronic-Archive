import logging
from selenium.webdriver.common.by import By
from ui.fixtures.pages.base_page import BasePage
from ui.data.data import Auth
from ui.data.constants import LoginNotice
from ui.fixtures.pages.document.documents import DocumentsPage

logger = logging.getLogger("Electronic Archive")


class LoginPage(BasePage):
    """
    Страница авторизации https://electronicarchive-frontend-afds.akbars.ru/
    Авторизация осуществляется через https://identity-server-is4.akbars.ru/
    """
    LOGIN_PANEL_TITLE = (By.XPATH, "//h3[text()='Авторизация']")  # Заголовок текста формы авторизации
    TITLE_SEARCH_DOCUMENTS = (By.XPATH, "//h2[contains(text(), 'Поиск документов')]")  # Заголовок раздела
    MOFFICE_TAB = (By.XPATH, "//label[@for='MOFFICE']")  # Вкладка домена авторизации в форме
    USERNAME_FIELD = (By.ID, "UserName")  # Поле ввода логина
    PASSWORD_FIELD = (By.ID, "Password")  # Поле воода пароля
    LOGIN_BUTTON = (By.CLASS_NAME, "login-btn")  # Кнопка Войти
    USER_LINK_IN_TAB = (By.XPATH, "//div[@class='sc-bHdvGS ggKXFZ']/button")  # Ссылка на профиль в верхнем меню
    EXIT_BUTTON_IN_TAB = (By.XPATH, "//span[text()='Выход']")  # Кнопка выхода в верхнем меню
    USER_DATA = (By.XPATH, "//div[@class='sc-ckLhtn dmqLJS']")  # Данные ФИО пользователя в верхнем меню
    USER_LINK_IN_LIVE_SPACE = (By.XPATH, "//div[@id='root']//nav/div[3]")  # Профиль пользователя в панели LiveSpace
    USER_DATA_IN_LIVE_SPACE = (By.XPATH, "//div[@class='ListItemText']")  # Данные пользователя в панели LiveSpace
    EXIT_IN_LIVE_SPACE = (By.XPATH, "//div[@class='ListItemButton MenuItem']/div")  # Кнопка выхода в панели LiveSpace

    # Переход в разделы
    ARCHIVE_LINK = (By.XPATH, "//ul[@class='MuiList-root sc-kskBZP bJJvzu MuiList-padding']/a[1]")  # Хранилище
    ENTITIES_LINK = (By.XPATH, "//ul[@class='MuiList-root sc-kskBZP bJJvzu MuiList-padding']/a[2]")  # Сущности
    INSTRUCTIONS_LINK = (By.XPATH, "//ul[@class='MuiList-root sc-kskBZP bJJvzu MuiList-padding']/a[3]")  # Инструкции

    def open_login_page(self):
        """Открытие страницы авторизации."""
        self.open_page(self.app.url)

        # Проверка, что открылась форма авторизации
        self.element_is_enabled(locator=self.LOGIN_PANEL_TITLE)  # Ожидание элемента
        assert self.get_text(locator=self.LOGIN_PANEL_TITLE) == LoginNotice.LOGIN_FORM_TEXT
        logger.info(f"Заголовок формы авторизации: {self.get_text(locator=self.LOGIN_PANEL_TITLE)}")

    def entry_data_authorization(self):
        """Ввод логина и пароля в форму авторизации."""
        self.click(locator=self.MOFFICE_TAB)  # Переключение вкладки домена авторизации на MOFFICE
        self.send_keys(locator=self.USERNAME_FIELD, value=Auth.login)
        self.send_keys(locator=self.PASSWORD_FIELD, value=Auth.password)
        self.click(locator=self.LOGIN_BUTTON)

        #  Проверка, что после авторизации произошел редирект на страницу поиска документов
        logger.info(f"Заголовок страницы после авторизации: {self.get_text(locator=self.TITLE_SEARCH_DOCUMENTS)}")
        self.element_is_enabled(locator=self.TITLE_SEARCH_DOCUMENTS)  # Ожидание элемента
        assert self.get_text(locator=self.TITLE_SEARCH_DOCUMENTS) == LoginNotice.TITLE_SEARCH_DOCUMENTS

    def click_login_button(self):
        """Клик по кнопке 'Войти' в форме авторизации."""
        self.click(locator=self.LOGIN_BUTTON)

    def go_to_entities(self):
        """Переход в раздел Сущности."""
        self.click(locator=self.ENTITIES_LINK)

    def assertion_opening_search_page(self):
        """Проверка открытия страницы поиска документов."""
        self.element_is_enabled(locator=DocumentsPage.BUTTON_CREATE)  # Ожидание элемента
        logger.info(f"Выполнен переход на страницу: {LoginNotice.URL_DOCUMENT_SEARCH.format(self.app.url)}")
        assert self.get_url() == LoginNotice.URL_DOCUMENT_SEARCH.format(self.app.url)

    def assertion_user_name(self):
        """Проверка, что авторизация произошла под нужным пользователем."""
        self.click(locator=LoginPage.USER_LINK_IN_LIVE_SPACE)
        logger.info(f"ФИО пользователя: {self.get_text(locator=LoginPage.USER_DATA_IN_LIVE_SPACE)}")
        assert self.get_text(locator=LoginPage.USER_DATA_IN_LIVE_SPACE) == LoginNotice.USER_NAME

    def logout_in_tab(self):
        """Логаут из аккаунта через таб."""
        self.element_is_enabled(locator=self.USER_LINK_IN_TAB)  # Ожидание появления элемента
        self.click(locator=self.USER_LINK_IN_TAB)  # Открытие профиля пользователя в верхнем меню
        self.click(locator=self.EXIT_BUTTON_IN_TAB)  # Клик по кнопке выхода из аккаунта

    def logout_from_live_space_panel(self):
        """Логаут из панели LiveSpace"""
        self.element_is_enabled(locator=self.USER_LINK_IN_LIVE_SPACE)  # Ожидание появления элемента
        self.click(locator=self.USER_LINK_IN_LIVE_SPACE)  # Открытие профиля пользователя
        self.click(locator=self.EXIT_IN_LIVE_SPACE)  # Клик по ссылке выхода из аккаунта
        #  Проверка, что после логаута произошел редирект на форму авторизации
        assert self.get_text(locator=LoginPage.LOGIN_PANEL_TITLE) == LoginNotice.LOGIN_FORM_TEXT
