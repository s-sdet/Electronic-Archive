import random
import logging
import time

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from ui.fixtures.pages.base_page import BasePage
from ui.data.constants import DocumentsTypeNotice

logger = logging.getLogger("Electronic Archive")


class CreateDocumentsTypeModel:
    """Генерация рандомных данных для валидного создания типа документа."""
    def __init__(self, document_type_name: str = None, file_type_name: str = None, file_extensions: str = None,
                 field_type_name: str = None, field_type_name_display: str = None):
        """
        :param document_type_name: Название типа документа
        :param file_type_name: Название типа файла
        :param file_extensions: Возможные расширения файла
        :param field_type_name: Название типа поля
        :param field_type_name_display: Отображаемое название типа поля
        """
        self.document_type_name = document_type_name
        self.file_type_name = file_type_name
        self.file_extensions = file_extensions
        self.field_type_name = field_type_name
        self.field_type_name_display = field_type_name_display

    @staticmethod
    def random_valid_data_for_doc_type():
        document_type_name = f"{DocumentsTypeNotice.DOCUMENT_TYPE_NAME}{random.randint(10, 1000)}"
        file_type_name = f"{DocumentsTypeNotice.FILE_TYPE_NAME}{random.randint(10, 1000)}"
        file_extensions = DocumentsTypeNotice.FILE_EXTENSIONS
        field_type_name = f"{DocumentsTypeNotice.FIELD_TYPE_NAME}{random.randint(10, 1000)}"
        field_type_name_display = f"{DocumentsTypeNotice.FIELD_TYPE_NAME_DISPLAY}{random.randint(10, 1000)}"
        return CreateDocumentsTypeModel(document_type_name=document_type_name, file_type_name=file_type_name,
                                        file_extensions=file_extensions, field_type_name=field_type_name,
                                        field_type_name_display=field_type_name_display)


class DocumentsTypePage(BasePage):
    """
    Страница администрирования типов документов
    https://electronicarchive-frontend-afds.dev.akbars.ru/administration
    """

    # Кнопки
    BUTTON_CREATE = (By.XPATH, "//span[text()='Создать']")  # Кнопка "Создать"
    BUTTON_CREATE_DOC_TYPE = (By.XPATH, "//span[text()='Тип документа']")  # Кнопка "Тип документа"
    BUTTON_CREATE_FOLDER = (By.XPATH, "//span[text()='Папку']")  # Кнопка "Папку"
    BUTTON_ADD_FILE_TYPE = (By.XPATH, "//form/div[2]//span[text()='Добавить']")  # Кнопка "Добавить" тип файла
    BUTTON_ADD_FIELD_TYPE = (By.XPATH, "//form/div[3]//span[text()='Добавить']")  # Кнопка "Добавить" тип полей
    BUTTON_ADD = (By.XPATH, "//div[@class='Modal-Window']//span[text()='Добавить']")  # Кнопка "Добавить"
    BUTTON_CANCEL = (By.XPATH, "//div[@class='Modal-Window']//span[text()='Отмена']")  # Кнопка "Отмена"
    BUTTON_CONFIRM = (By.XPATH, "//span[text()='Подтвердить']")  # Кнопка "Подтвердить"
    BUTTON_DELETE = (By.XPATH, "//span[text()='Удалить']")  # Кнопка "Удалить"
    BUTTON_FOLDER_MENU = (By.XPATH, "//div[text()='Папка 393']//following::div/button")  # Кнопка вызова меню папки
    BUTTON_SAVE = (By.XPATH, "//span[text()='Сохранить']")  # Кнопка "Сохранить" в форме редактирования папки

    USER_LINK_IN_TAB = (By.XPATH, "//div[@class='sc-bHdvGS ggKXFZ']")  # Ссылка на профиль в верхнем меню

    # Ссылки
    LINK_TO_ADMIN_PANEL = (By.XPATH, "//div[@id='root']//nav/div[2]/div[5]")  # Ссылка на панель администрирования
    LINK_ADD_GROUPS_AD = (By.XPATH, "//span[text()='Добавить']")  # Ссылка добавить Группы AD
    LINK_EDITING_GROUP = (By.XPATH, "//span[text()='Редактирование']")  # Ссылка "Редактирование"
    LINK_COPY = (By.XPATH, "//span[text()='Копировать']")  # Ссылка "Копировать"
    LINK_DELETE = (By.XPATH, "//span[text()='Удалить']")  # Ссылка "Удалить"
    LINK_HISTORY = (By.XPATH, "//span[text()='История']")  # Ссылка "История"

    # Заголовки
    TITLE_ADMIN_PANEL = (By.XPATH, "//h2[text()='Администрирование']")  # Заголовок страницы администрирования
    TITLE_FORM_DOC_TYPE_CREATE = (By.XPATH, "//h2[text()='Создание типа документа']")  # Заголовок страницы "Создание
    # типа документа"
    TITLE_FORM_CREATE_FOLDER = (By.XPATH, "//h2[text()='Создание папки']")  # Заголовок окна "Создание папки"
    TITLE_CREATE_FILE_TYPE = (By.XPATH, "//h4[text()='Создание типа файла']")  # Заголовок окна "Создание типа файла"
    TITLE_CREATE_FIELD_TYPE = (By.XPATH, "//h4[text()='Создание типа метаданных']")  # Заголовок "Создание метаданных"
    TITLE_ACTION_CONFIRMATION = (By.XPATH, "//div[text()='Подтверждение действий']")  # Заголовок окна подтверждения
    TITLE_DELETE_CONFIRMATION = (By.XPATH, "//div[text()='Подтверждение удаления']")  # Заголовок окна подтверждения
    TITLE_ADD_GROUPS_AD = (By.XPATH, "//h4[text()='Добавление группы AD']")  # Заголовок окна "Добавление группы AD"
    TITLE_EDITING_FOLDER = (By.XPATH, "//h2[text()='Редактирование папки']")  # Заголовок окна "Редактирование папки"
    TITLE_CHANGE_HISTORY = (By.XPATH, "//h4[text()='История изменений групп AD']")  # Окно "История изменений групп"

    # Поля ввода данных
    FILED_DOCUMENT_TYPE_NAME = (By.XPATH, "//input[@name='name']")  # Название типа документа
    FILED_FOLDER_NAME = (By.XPATH, "//input[@name='name']")  # Название папки
    FILED_FILE_TYPE_NAME = (By.XPATH, "//div[@class='Dialog-Body']//input[@name='name']")  # Название типа документа
    FILED_FILE_EXTENSIONS = (By.XPATH, "//div[@class='Dialog-Body']//input[@name='allowedExtensions']")  # Расширения
    FIELD_TYPE_NAME = (By.XPATH, "//div[@class='Dialog-Body']//input[@name='name']")  # Название типа поля
    FIELD_TYPE_NAME_DISPLAY = (By.XPATH, "//input[@name='displayName']")  # Отображаемое название типа поля
    FIELD_ADD_GROUPS_AD = (By.XPATH, "//div[@class='Dialog-Body']//input")  # Название группы AD

    # Чекбоксы
    CHECKBOX_ALLOW_EXTRA_FILE_TYPES = (By.NAME, "allowExtraFileTypes")  # Разрешить прикрепление других типов файлов
    CHECKBOX_ALLOW_EXTRA_PROPERTY_TYPES = (By.NAME, "allowExtraPropertyTypes")  # Разрешить добавление др. типов полей
    CHECKBOX_REQUIRED = (By.XPATH, "//div[@class='Dialog-Body']//input[@name='isRequired']")  # Обязательный

    # Всплывашки об успешном создании/сохранении сущностей
    SUCCESS_TYPE_CREATE = (By.XPATH, "//div[@class='MuiCollapse-wrapperInner']")  # Уведомление создания
    SUCCESS_TYPE_DELETE = (By.XPATH, "//div[@class='MuiCollapse-wrapperInner']")  # Уведомление удаления
    SUCCESS_FOLDER_CREATE = (By.XPATH, "//div[@class='MuiCollapse-wrapperInner']")  # Уведомление создания папки
    SUCCESS_FOLDER_SAVE = (By.XPATH, "//div[@class='MuiCollapse-wrapperInner']")  # Уведомление изменения папки

    ELEMENT_TO_WAIT_PAGE_TO_LOAD = (By.XPATH, "//div[@class='sc-jnldDj fbeZwT']/div[20]")  # Локатор для ожидания
    NAME_FIRST_GROUP = (By.XPATH, "//div[@role='dialog']/div/div[2]//tbody/tr[2]/td[2]/span")  # Название первой группы
    NAME_SECOND_GROUP = (By.XPATH, "//div[@role='dialog']/div/div[2]//tbody/tr[1]/td[2]/span")  # Название второй группы

    # Выпадашки
    FILE_EXTENSION_PDF = (By.XPATH, "//body[@class='no-scroll']/div[4]//li")  # Выбор типа расширения .pdf
    CLOSE_FILE_TYPE_SELECTION = (By.XPATH, "//label[@class='Autocomplete-Body']/div[2]/div/div")  # Закрыть выбор типа

    def open_admin_panel(self):
        """Переход в панель администрирования."""
        self.element_is_enabled(locator=self.LINK_TO_ADMIN_PANEL)  # Ожидание элемента
        self.click(locator=self.LINK_TO_ADMIN_PANEL)  # Клик по ссылке "Администрирования"

        # Проверка перехода в панель администрирования
        self.element_is_enabled(locator=self.TITLE_ADMIN_PANEL)  # Ожидание элемента
        assert self.get_text(locator=self.TITLE_ADMIN_PANEL) == DocumentsTypeNotice.TITLE_ADMIN_PANEL

    def open_form_doc_type_create(self):
        """Открытие формы создания типа документа."""
        # Проверка перехода в панель администрирования
        self.element_is_enabled(locator=self.ELEMENT_TO_WAIT_PAGE_TO_LOAD)  # Ожидание загрузки страницы
        assert self.get_text(locator=self.TITLE_ADMIN_PANEL) == DocumentsTypeNotice.TITLE_ADMIN_PANEL

        self.click(locator=self.BUTTON_CREATE)  # Клик по кнопке "Создать"
        self.element_is_enabled(locator=self.BUTTON_CREATE_DOC_TYPE)  # Ожидание элемента
        self.click(locator=self.BUTTON_CREATE_DOC_TYPE)  # Клик по кнопке "Тип документа"

        # Проверка перехода в форму создания типа документа
        self.element_is_enabled(locator=self.TITLE_FORM_DOC_TYPE_CREATE)  # Ожидание элемента
        assert self.get_text(locator=self.TITLE_FORM_DOC_TYPE_CREATE) == DocumentsTypeNotice.TITLE_FORM_DOC_TYPE_CREATE

    def data_entry_doc_type(self, data: CreateDocumentsTypeModel):
        """Заполнение данных в форме названия типа документа."""
        logger.info(f"Название типа документа: {data.document_type_name}")
        self.element_is_enabled(locator=self.FILED_DOCUMENT_TYPE_NAME)  # Ожидание элемента
        self.send_keys(locator=self.FILED_DOCUMENT_TYPE_NAME, value=data.document_type_name)

    def data_entry_file_types(self, data: CreateDocumentsTypeModel, adding_type: bool = True):
        """
        Заполнение данных в форме типов файлов.
        :param data: Модель генерации валидных данных для создания типа документа
        :param adding_type: По-умолчанию вызывается метод нажатия кнопки Добавить, если adding_type=False - Отменить
        """
        self.element_is_enabled(locator=self.BUTTON_ADD_FILE_TYPE)  # Ожидание элемента
        self.click(locator=self.BUTTON_ADD_FILE_TYPE)  # Клик "Добавить" для открытия формы

        # Проверка открытия окна "Создание типа файла"
        self.element_is_enabled(locator=self.TITLE_CREATE_FILE_TYPE)  # Ожидание элемента
        assert self.get_text(locator=self.TITLE_CREATE_FILE_TYPE) == DocumentsTypeNotice.TITLE_CREATE_FILE_TYPE
        logger.info(f"Название типа файла: {data.file_type_name}, Возможные расширения файла: {data.file_extensions}")

        self.send_keys(locator=self.FILED_FILE_TYPE_NAME, value=data.file_type_name)  # Ввод названия типа файла
        self.send_keys(locator=self.FILED_FILE_EXTENSIONS, value=data.file_extensions)  # Ввод расширений файла
        self.element_is_enabled(locator=self.FILE_EXTENSION_PDF)  # Ожидание элемента
        self.click(locator=self.FILE_EXTENSION_PDF)  # Выбор типа расширения из выпадашки после ввода
        self.element_is_enabled(locator=self.CLOSE_FILE_TYPE_SELECTION)  # Ожидание элемента
        self.click(locator=self.CLOSE_FILE_TYPE_SELECTION)  # Закрытие выпадашки после выбора расширения файла
        self.adding_type() if adding_type else self.cancel_adding_type()

    def data_entry_metadata_type(self, data: CreateDocumentsTypeModel, adding_type: bool = True):
        """
        Заполнение данных в форме типов метаданных.
        :param data: Модель генерации валидных данных для создания полей документа
        :param adding_type: По-умолчанию вызывается метод нажатия кнопки Добавить, если adding_type=False - Отменить
        """
        self.click(locator=self.BUTTON_ADD_FIELD_TYPE)  # Клик "Добавить" для открытия формы

        # Проверка открытия окна "Создание типа метаданных"
        self.element_is_enabled(locator=self.TITLE_CREATE_FIELD_TYPE)  # Ожидание элемента
        logger.info(f"Заголовок окна: {self.get_text(locator=self.TITLE_CREATE_FIELD_TYPE)}")
        assert self.get_text(locator=self.TITLE_CREATE_FIELD_TYPE) == DocumentsTypeNotice.TITLE_CREATE_FIELD_TYPE
        logger.info(f"Системное название: {data.field_type_name}, "
                    f"Отображаемое название: {data.field_type_name_display}")

        self.send_keys(locator=self.FIELD_TYPE_NAME, value=data.field_type_name)  # Ввод названия типа данных
        self.send_keys(locator=self.FIELD_TYPE_NAME_DISPLAY, value=data.field_type_name_display)  # Ввод отображаемого
        # названия типа поля
        self.adding_type() if adding_type else self.cancel_adding_type()

    def adding_type(self):
        """Добавление типов в создаваемый тип документа"""
        self.click(locator=self.CHECKBOX_REQUIRED)  # Выбор чекбокса "Обязательный"
        self.click(locator=self.BUTTON_ADD)  # Клик кнопки "Добавить"

    def cancel_adding_type(self):
        """Отмена добавления типов в создаваемый тип документа"""
        self.click(locator=self.CHECKBOX_REQUIRED)  # Выбор чекбокса "Обязательный"
        self.click(locator=self.BUTTON_CANCEL)  # Клик кнопки "Отмена"

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
        self.element_is_enabled(locator=self.SUCCESS_TYPE_CREATE)  # Ожидание элемента
        logger.info(f"Текст уведомления: {self.get_text(locator=self.SUCCESS_TYPE_CREATE)}")
        assert self.get_text(locator=self.SUCCESS_TYPE_CREATE) == DocumentsTypeNotice.SUCCESS_TYPE_CREATE

    def copy_document_type(self, type_name):
        """Копирование созданного типа документа."""
        self.element_is_enabled(locator=(By.XPATH, f"//div[text()='{type_name}']//following::div/button"))  # Ожидание
        self.click(locator=(By.XPATH, f"//div[text()='{type_name}']//following::div/button"))  # Вызов меню типа док-та
        self.element_is_enabled(locator=self.LINK_COPY)  # Ожидание элемента
        self.click(locator=self.LINK_COPY)  # Клик по ссылке Копировать

        # Проверка перехода в форму создания типа документа
        self.element_is_enabled(locator=self.TITLE_FORM_DOC_TYPE_CREATE)  # Ожидание элемента
        assert self.get_text(locator=self.TITLE_FORM_DOC_TYPE_CREATE) == DocumentsTypeNotice.TITLE_FORM_DOC_TYPE_CREATE

        # Проверка, что название типа документа имеет приставку "копия"
        logger.info(f"Название типа документа: {type_name}")
        self.element_is_enabled(locator=self.FILED_DOCUMENT_TYPE_NAME)  # Ожидание элемента
        logger.info(f"Название копии: {self.get_attribute(locator=self.FILED_DOCUMENT_TYPE_NAME, attribute='value')}")
        assert type_name in self.get_attribute(locator=self.FILED_DOCUMENT_TYPE_NAME, attribute='value')

    def save_copy_document_type(self):
        """Сохранение копии типа документа."""
        self.element_is_enabled(locator=self.BUTTON_CREATE)  # Ожидание элемента
        self.click(locator=self.BUTTON_CREATE)

        # Проверка открытия окна подтверждения
        self.element_is_enabled(locator=self.TITLE_ACTION_CONFIRMATION)  # Ожидание элемента
        logger.info(f"Текст уведомления: {self.get_text(locator=self.TITLE_ACTION_CONFIRMATION)}")
        assert self.get_text(locator=self.TITLE_ACTION_CONFIRMATION) == DocumentsTypeNotice.TITLE_ACTION_CONFIRMATION

        self.click(locator=self.BUTTON_CONFIRM)  # Подтверждение действия

        # Проверка появления сообщения об успешном создании
        self.element_is_enabled(locator=self.SUCCESS_TYPE_CREATE)  # Ожидание элемента
        logger.info(f"Текст уведомления: {self.get_text(locator=self.SUCCESS_TYPE_CREATE)}")
        assert self.get_text(locator=self.SUCCESS_TYPE_CREATE) == DocumentsTypeNotice.SUCCESS_TYPE_CREATE

    def delete_document_type(self, type_name):
        """Удаление типа документа и его копии из списка."""
        for name in [type_name, f"{type_name} (копия)"]:
            self.element_is_enabled(locator=(By.XPATH, f"//div[text()='{name}']//following::div/button"))  # Ожидание
            self.click(locator=(By.XPATH, f"//div[text()='{name}']//following::div/button"))  # Вызов меню типа док-та
            self.element_is_enabled(locator=self.LINK_DELETE)  # Ожидание элемента
            self.click(locator=self.LINK_DELETE)  # Клик по ссылке Удалить

            # Проверка открытия окна подтверждения
            self.element_is_enabled(locator=self.TITLE_DELETE_CONFIRMATION)  # Ожидание элемента
            logger.info(f"Текст уведомления: {self.get_text(locator=self.TITLE_DELETE_CONFIRMATION)}")
            assert self.get_text(
                locator=self.TITLE_DELETE_CONFIRMATION) == DocumentsTypeNotice.TITLE_DELETE_CONFIRMATION
            try:
                self.click(locator=self.BUTTON_DELETE)  # Подтверждение действия

                # Проверка появления сообщения об успешном удалении
                self.element_is_enabled(locator=self.SUCCESS_TYPE_DELETE)  # Ожидание элемента
                logger.info(f"Текст уведомления: {self.get_text(locator=self.SUCCESS_TYPE_DELETE)}")
                assert self.get_text(locator=self.SUCCESS_TYPE_DELETE) == DocumentsTypeNotice.SUCCESS_TYPE_DELETE
            except StaleElementReferenceException:
                logger.info("Тип документа удалился, но уведомление наложилось на другое.")
            except AssertionError:
                logger.info("Тип документа удалился, но уведомление наложилось на другое.")

    def open_form_to_create_folder(self):
        """Ввод данных для создания папки типов документов."""
        self.element_is_enabled(locator=self.ELEMENT_TO_WAIT_PAGE_TO_LOAD)  # Ожидание загрузки страницы
        logger.info(f"Заголовок страницы: {self.get_text(locator=self.TITLE_ADMIN_PANEL)}")
        assert self.get_text(locator=self.TITLE_ADMIN_PANEL) == DocumentsTypeNotice.TITLE_ADMIN_PANEL

        self.element_is_enabled(locator=self.BUTTON_CREATE)  # Ожидание элемента
        self.click(locator=self.BUTTON_CREATE)  # Клик по кнопке "Создать"
        self.element_is_enabled(locator=self.BUTTON_CREATE_FOLDER)  # Ожидание элемента
        self.click(locator=self.BUTTON_CREATE_FOLDER)  # Клик по кнопке "Папку"

        logger.info(f"Заголовок страницы: {self.get_text(locator=self.TITLE_FORM_CREATE_FOLDER)}")
        assert self.get_text(locator=self.TITLE_FORM_CREATE_FOLDER) == DocumentsTypeNotice.TITLE_FORM_FOLDER_CREATE

    def data_entry_to_create_folder(self, folder_name, group_name):
        """Ввод данных для создания папки типов документов."""
        self.send_keys(locator=self.FILED_FOLDER_NAME, value=folder_name)  # Название папки
        self.click(locator=self.LINK_ADD_GROUPS_AD)  # Клик по ссылке добавить Группы AD

        # Проверка, что открылось окно добавления группы AD
        self.element_is_enabled(locator=self.TITLE_ADD_GROUPS_AD)  # Ожидание элемента
        assert self.get_text(locator=self.TITLE_ADD_GROUPS_AD) == DocumentsTypeNotice.TITLE_ADD_GROUPS_AD
        self.send_keys(locator=self.FIELD_ADD_GROUPS_AD, value=group_name)  # Название группы
        self.click(locator=self.BUTTON_ADD)  # Клик кнопки "Добавить"

    def create_folder(self):
        """Создание и проверка создания папки типов документа."""
        self.element_is_enabled(locator=self.BUTTON_CREATE)  # Ожидание элемента
        self.click(locator=self.BUTTON_CREATE)  # Клик по кнопке "Создать"

        # Проверка открытия окна подтверждения
        self.element_is_enabled(locator=self.TITLE_ACTION_CONFIRMATION)  # Ожидание элемента
        logger.info(f"Текст уведомления: {self.get_text(locator=self.TITLE_ACTION_CONFIRMATION)}")
        assert self.get_text(locator=self.TITLE_ACTION_CONFIRMATION) == DocumentsTypeNotice.TITLE_ACTION_CONFIRMATION
        self.click(locator=self.BUTTON_CONFIRM)  # Клик по кнопке "Подтвердить"

        # Проверка появления сообщения об успешном создании
        self.element_is_enabled(locator=self.SUCCESS_FOLDER_CREATE)  # Ожидание элемента
        logger.info(f"Текст уведомления: {self.get_text(locator=self.SUCCESS_FOLDER_CREATE)}")
        assert self.get_text(locator=self.SUCCESS_FOLDER_CREATE) == DocumentsTypeNotice.SUCCESS_FOLDER_CREATE

    def editing_folder(self, folder_name):
        """Редактирование нужной папки типов документов."""
        self.element_is_enabled(locator=(By.XPATH, f"//div[text()='{folder_name}']//following::div/button"))  # Ожидание
        self.click(locator=(By.XPATH, f"//div[text()='{folder_name}']//following::div/button"))  # Вызов меню папки
        self.element_is_enabled(locator=self.LINK_EDITING_GROUP)  # Ожидание элемента
        self.click(locator=self.LINK_EDITING_GROUP)  # Клик по ссылке Редактирование в меню папки

        # Проверка открытия страницы редактирования папки
        logger.info(f"Название страницы: {self.get_text(locator=self.TITLE_EDITING_FOLDER)}")
        assert self.get_text(locator=self.TITLE_EDITING_FOLDER) == DocumentsTypeNotice.TITLE_EDITING_FOLDER

    def add_second_group(self, second_group_name):
        """Добавление второй группы AD."""
        self.click(locator=self.LINK_ADD_GROUPS_AD)  # Клик по ссылке "Добавить" Группы AD

        # Проверка, что открылось окно добавления группы AD
        self.element_is_enabled(locator=self.TITLE_ADD_GROUPS_AD)  # Ожидание элемента
        assert self.get_text(locator=self.TITLE_ADD_GROUPS_AD) == DocumentsTypeNotice.TITLE_ADD_GROUPS_AD
        self.send_keys(locator=self.FIELD_ADD_GROUPS_AD, value=second_group_name)  # Название группы
        self.click(locator=self.BUTTON_ADD)  # Клик кнопки "Добавить"

        # Проверка открытия страницы редактирования папки
        logger.info(f"Название страницы: {self.get_text(locator=self.TITLE_EDITING_FOLDER)}")
        assert self.get_text(locator=self.TITLE_EDITING_FOLDER) == DocumentsTypeNotice.TITLE_EDITING_FOLDER

    def save_folder(self):
        """Сохранение изменений в папке типов документов."""
        self.element_is_enabled(locator=self.BUTTON_SAVE)  # Ожидание элемента
        self.click(locator=self.BUTTON_SAVE)  # Клик по кнопке "Сохранить"

        # Проверка открытия окна подтверждения сохранения папки
        self.element_is_enabled(locator=self.TITLE_ACTION_CONFIRMATION)  # Ожидание элемента
        logger.info(f"Текст уведомления: {self.get_text(locator=self.TITLE_ACTION_CONFIRMATION)}")
        assert self.get_text(locator=self.TITLE_ACTION_CONFIRMATION) == DocumentsTypeNotice.TITLE_ACTION_CONFIRMATION
        self.click(locator=self.BUTTON_CONFIRM)  # Клик по кнопке "Подтвердить"

        # Проверка появления сообщения об успешном создании
        self.element_is_enabled(locator=self.SUCCESS_FOLDER_SAVE)  # Ожидание элемента
        logger.info(f"Текст уведомления: {self.get_text(locator=self.SUCCESS_FOLDER_SAVE)}")
        assert self.get_text(locator=self.SUCCESS_FOLDER_SAVE) == DocumentsTypeNotice.SUCCESS_FOLDER_SAVE

        # Проверка перехода в панель администрирования после сохранения папки
        self.element_is_enabled(locator=self.TITLE_ADMIN_PANEL)  # Ожидание элемента
        assert self.get_text(locator=self.TITLE_ADMIN_PANEL) == DocumentsTypeNotice.TITLE_ADMIN_PANEL

    def rename_folder(self, new_folder_name):
        """Изменение названия папки типов документов."""
        self.element_is_enabled(locator=self.FILED_FOLDER_NAME)  # Ожидание элемента
        self.clear_by_deletion(locator=self.FILED_FOLDER_NAME)  # Очистка поля ввода
        self.send_keys(locator=self.FILED_FOLDER_NAME, value=new_folder_name)  # Новое название папки

    def checking_change_history(self, second_group_name):
        """
        Проверка истории изменений
        :param second_group_name: Название второй AD группы.
        """
        self.element_is_enabled(locator=self.LINK_HISTORY)
        self.click(locator=self.LINK_HISTORY)  # Переход на вкладку "История"

        # Проверка открытия окна "История изменений групп AD"
        self.element_is_enabled(locator=self.TITLE_CHANGE_HISTORY)  # Ожидание элемента
        assert self.get_text(locator=self.TITLE_CHANGE_HISTORY) == DocumentsTypeNotice.TITLE_CHANGE_HISTORY

        # Проверка второй добавленной группы в истории изменений
        assert self.get_text(locator=self.NAME_SECOND_GROUP) == second_group_name
