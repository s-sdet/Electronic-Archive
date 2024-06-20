import datetime
import os
import logging
import time
from pathlib import Path
from datetime import date
from selenium.webdriver.common.by import By
from ui.fixtures.pages.base_page import BasePage
from ui.data.constants import DocumentNotice

logger = logging.getLogger("Electronic Archive")


def download_wait(directory, timeout=20, expected_count_files=None):
    """
    Ожидание загрузки файла с заданным таймаутом.
    Метод считает кол-во файлов в нужной директории и в заданном таймауте проверяет пока кол-во не станет больше.
    :param directory: Папка в которую будет загружен файл.
    :param timeout: Время ожидания.
    :param expected_count_files: int, по умолчанию None. Если оно задано - дождаться ожидаемого кол-ва.
    """
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        files = str(Path(os.getcwd(), directory))  # Получаем список, содержащий имена файлов в папке
        if expected_count_files and len(files) != expected_count_files:
            dl_wait = True
        for file_name in files:
            if file_name.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds


def assertion_downloaded_file_in_directory(directory, file_name):
    """Метод проверки и логирования, что скачанный файл находится в нужной директории."""
    files = os.listdir(directory)
    logger.info(f"Список файлов: {files}")
    # assert file_name in files


def deleting_png_files(directory):
    """Метод удаления файлов в папке."""
    for f in os.listdir(directory):
        if not f.endswith(".png"):
            continue
        os.remove(os.path.join(directory, f))


class DocumentsPage(BasePage):
    """Страница поиска документов https://electronicarchive-frontend-afds.dev.akbars.ru/document/search"""

    # Папки типов документов
    FOLDER_DOCUMENT_TYPE_EA = (By.XPATH, "//div[text()='ЭА']")

    # Типы документов
    SELECT_DOCUMENT_TYPE_WITH_2_FIELDS = (
        By.XPATH, "//div[contains(text(), 'Тестовый тип документа с 2 дополнительными полями')]")
    SELECT_DOCUMENT_TYPE_EA_123 = (By.XPATH, "//div[contains(text(), 'ЭА 123')]")
    SELECT_DOCUMENT_REQUIRED_TYPE = (By.XPATH, "//div[contains(text(), 'Для автотестов')]")
    SELECT_DOCUMENT_TYPE_EA_PASSPORT_RF = (By.XPATH, "//div[text()='ЭА Паспорт гражданина РФ ']")
    SELECT_DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS = (By.XPATH, "//div[text()='Тип документа с разными расширениями']")
    SELECT_DOCUMENT_TYPE_WITH_ALL_FIELD_TYPES = (By.XPATH, "//div[text()='Тип документа со всеми Типами полей']")

    # Типы файла
    FIELD_FILE_TYPE = (By.XPATH, "//div[@id='mui-component-select-fileTypeId']")  # Поле выбора типа файла
    FILE_TYPE_DOCUMENT_SCAN = (By.XPATH, "//div[text()='Скан документа']")  # Тип документа "Скан документа"
    FILE_TYPE_DIFFERENT_EXTENSIONS = (By.XPATH, "//div[text()='Разные расширения']")  # Тип файла "Разные расширения"

    # Кнопки
    BUTTON_CREATE = (By.XPATH, "//span[contains(text(), 'Создать документ')]")  # Создать документ
    BUTTON_SELECT = (By.XPATH, "//span[contains(text(), 'Выбрать')]")  # Выбрать
    BUTTON_SEARCH = (By.XPATH, "//span[contains(text(), 'Найти')]")  # Найти
    BUTTON_ACTIONS = (By.XPATH, "//div[@class='sc-hNDKOd iAUITB']/button")  # Действия
    BUTTON_DOCUMENT_VERSION_ACTUAL = (By.XPATH, "//li[contains(text(), 'Сделать версию документа актуальной')]")
    BUTTON_UPLOAD = (By.XPATH, "//button[@data-testid='save-btn']")  # Загрузить
    BUTTON_DELETE = (By.XPATH, "//span[contains(text(), 'Удалить')]")  # Удалить
    BUTTON_DOWNLOAD = (By.XPATH, "//span[contains(text(), 'Скачать')]")  # Скачать
    BUTTON_SAVE = (By.XPATH, "//span[contains(text(), 'Сохранить')]")  # Сохранить
    BUTTON_ADD_DOCUMENT_TYPE = (By.XPATH, "//span[contains(text(), 'Добавить тип документа')]")  # Добавить тип док-та
    BUTTON_FILE_UPLOAD = (By.XPATH, "//span[contains(text(), 'Нажмите для загрузки файлов')]")  # Добавить файл
    BUTTON_CONFIRM = (By.XPATH, "//span[contains(text(), 'Подтвердить')]")  # Подтвердить
    BUTTON_DOWNLOAD_FILE = (By.XPATH, "//div[@class='sc-hNDKOd iAUITB']//button")  # Скачать файл документа
    BUTTON_NEXT_PAGE = (By.XPATH, "//button[@title='Следующая страница']")  # Следущая страница

    # Выпадающие списки
    DROPDOWN_DOCUMENT_VERSION = (By.XPATH, "//div[contains(text(), 'актуальная')]")  # Выбор версии документа
    DROPDOWN_DOCUMENT_VERSION_1 = (By.XPATH, "//ul[@role='listbox']/li[1]")  # Версия документа 1
    DROPDOWN_DOCUMENT_VERSION_2 = (By.XPATH, "//ul[@role='listbox']/li[2]")  # Версия документа 2
    DROPDOWN_FILE = (By.XPATH, "//div[contains(text(), 'upload_file')]")  # Выбор файла в режиме просмотра документа

    # Ссылки
    LINK_DOCUMENT = (By.XPATH, "//tbody[@class='MuiTableBody-root']//a")  # Ссылка на редактируемый документ
    LINK_SEARCH_DOCUMENT = (By.XPATH, "//div[@id='root']//nav/div[2]/div")  # Ссылка на поиск документов
    LINK_MAKE_FILE_UP_TO_DATE = (By.XPATH, "//li[contains(text(), 'Сделать файл актуальным')]")
    LINK_MAKE_FILE_IRRELEVANT = (By.XPATH, "//li[contains(text(), 'Убрать актуальность файла')]")
    LINK_UPLOAD_FILE = (By.XPATH, "//li[contains(text(), 'Загрузить файл')]")
    LINK_DELETE_FILE = (By.XPATH, "//li[contains(text(), 'Удалить файл')]")

    # Заголовки окон и форм
    TITLE_DOCUMENT_TYPE_SELECTION_WINDOW = (By.XPATH, "//div[@class='Dialog-Header']/h4")  # Заголовок окна выбора типа
    # типа документа
    TITLE_DOCUMENT = (By.XPATH, "//div[@class='sc-dmyDGi dMGFLb']/h2")  # Заголовок редактируемого документа
    TITLE_METADATA_AND_VALUES = (By.XPATH, "//div[contains(text(), 'Метаданные и значения')]")  # Заголовок метаданных
    TITLE_METADATA_EDITING = (By.XPATH, "//div[@class='sc-csKIKE iFKuVk']")  # Заголовок окна редактирования документа
    TITLE_CREATE_DOCUMENT = (By.XPATH, "//h2[@class='sc-guDLRT bRDCyB']")  # Заголовок формы создания документа
    TITLE_UPLOAD_FILE = (By.XPATH, "//div[contains(text(), 'Загрузка файла')]")  # Заголовок формы загрузки файла

    # Вкладки меню в режиме просмотра документа
    ELECTRONIC_SIGNATURE = (By.XPATH, "//span[contains(text(), 'Подписание ЭП')]")  # Подписание ЭП

    # Поля документов в режиме редактирования
    DATE_FIELD = (By.XPATH, "//label[text()='Дата']//following::div/input")  # Дата

    SEARCH_RESULT = (By.XPATH, "//h2[contains(text(), 'Результат поиска')]")  # Заголовок окна результатов поиска
    EDIT_METADATA = (By.XPATH, "//li[contains(text(), 'Редактировать метаданные')]")  # Редактировать метаданные
    METADATA_AND_VALUES = (By.XPATH, "//div[text()='Метаданные и значения']//following::div/div/div[2]")  # Номер док-та
    SELECT_FIELD_DOCUMENT_TYPE = (By.XPATH, "//div[text()='Загрузка файлов']//following::div//input")  # Поле "Тип док."
    SUCCESS_DOCUMENT_CREATE = (By.XPATH, "//div[@class='MuiCollapse-wrapperInner']")  # Уведомление о создании

    INPUT_FILE_UPLOAD = (By.XPATH, "//input[@data-testid='file-input']")
    FILE_NAME_IN_DOCUMENT = (By.XPATH, "//span[@class='sc-iLXwop iAgTML']")
    FILE_NAMES_IN_DOCUMENT = {
        1: (By.XPATH, "//ul[@class='sc-jiaTdC dCEwQM']/li[1]//span"),
        2: (By.XPATH, "//ul[@class='sc-jiaTdC dCEwQM']/li[2]//span"),
        3: (By.XPATH, "//ul[@class='sc-jiaTdC dCEwQM']/li[3]//span"),
        4: (By.XPATH, "//ul[@class='sc-jiaTdC dCEwQM']/li[4]//span")
    }
    FILE_RELEVANCE_STATUS = (By.XPATH, "//div[@class='sc-hNDKOd iAUITB']/div/div[2]")
    ERROR_REQUIRED_FIELD = (By.XPATH, "//form[@class='sc-dQmhJc bBHdrE']//div[2]//p")  # Уведомление обязательное поле
    CHECKBOX_ONLY_SIGNED_DOCUMENTS = (By.NAME, "isSigned")  # Чекбокс "Только подписанные" для поиска документов
    STATUS_ELECTRONIC_SIGNATURE = (By.XPATH, "//span[text()='Подписан']")  # Статус ЭП
    AVAILABLE_EXTENSIONS = (By.XPATH, "//div[contains(text(), 'Доступные расширения')]")  # Предупреждение формата файла
    DOCUMENT_PREVIEW = (By.XPATH, "//img[@alt='Документ']")  # Превью документа
    PDF_DOCUMENT_PREVIEW = (By.XPATH, "//canvas[@class='react-pdf__Page__canvas']")  # Превью PDF документа
    LINES_PER_PAGE = (By.XPATH, "//p[text()='Строк на странице:']")  # Строк на странице
    WAITING_FOR_SEARCH_RESULT = (By.XPATH, "//tbody[@class='MuiTableBody-root']/tr/td[2]/span/a")  # Таблица результатов
    CHECKBOX_SELECT_20_DOCUMENTS = (By.XPATH, "//span[@data-testid='checkbox']/span")  # Выбор 20 документов
    FAILURE_DOWNLOAD_MORE_20_DOCUMENTS = (
        By.XPATH, "//span[text()='Превышено допустимое количество документов (20) для загрузки']")  # Текст ошибки
    FILE_NAME_WHEN_VIEWING_DOCUMENT = (By.XPATH, f"//li[contains(text(), )]")  # Выбор файла в документе

    # Поля метаданных в режиме редактирования документа
    LOCATORS_METADATA = {
        "APPLICATION_NUMBER": (By.XPATH, "//div[@class='sc-crHGWd jETAME']//div[1]//input"),
        "ACCOUNT_NUMBER":     (By.XPATH, "//div[@class='sc-crHGWd jETAME']//div[2]//input"),
        "REFERENCE_NUMBER":   (By.XPATH, "//div[@class='sc-crHGWd jETAME']//div[3]//input"),
        "CONTRACT_NUMBER":    (By.XPATH, "//div[@class='sc-crHGWd jETAME']//div[4]//input"),
        "CLIENT_ID_NUMBER":   (By.XPATH, "//div[@class='sc-crHGWd jETAME']//div[5]//input"),
        "CARD_ID_NUMBER":     (By.XPATH, "//div[@class='sc-crHGWd jETAME']//div[6]//input"),
        "ADDITIONAL_FIELD":   (By.XPATH, "//div[@class='sc-crHGWd jETAME']//div[7]//input"),
        "DIRECTORY":          (By.XPATH, "//div[@class='sc-crHGWd jETAME']//div[8]//input")
    }

    # Поля метаданных в режиме создания документа
    LOCATORS_METADATA_TO_CREATE_DOCUMENT = {
        "APPLICATION_NUMBER": (By.XPATH, "//div[text()='Метаданные и значения']//following::div/div[1]//input"),
        "ACCOUNT_NUMBER":     (By.XPATH, "//div[text()='Метаданные и значения']//following::div/div[2]//input"),
        "REFERENCE_NUMBER":   (By.XPATH, "//div[text()='Метаданные и значения']//following::div/div[3]//input"),
        "CONTRACT_NUMBER":    (By.XPATH, "//div[text()='Метаданные и значения']//following::div/div[4]//input"),
        "CLIENT_ID_NUMBER":   (By.XPATH, "//div[text()='Метаданные и значения']//following::div/div[5]//input"),
        "CARD_ID_NUMBER":     (By.XPATH, "//div[text()='Метаданные и значения']//following::div/div[6]//input")
    }

    # Поля дополнительных метаданных в режиме создания документа
    LOCATORS_ADDITIONAL_METADATA_TO_CREATE_DOCUMENT = {
        "NUMBER":   (By.XPATH, "//div[text()='Метаданные и значения']//following::div/div[7]//input"),
        "DATE":     (By.XPATH, "//div[text()='Метаданные и значения']//following::div/div[8]//input"),
        "STRING":   (By.XPATH, "//div[text()='Метаданные и значения']//following::div/div[9]//input")
    }

    # Поля метаданных в режиме поиска документа.
    LOCATORS_METADATA_TO_SEARCH_DOCUMENT = {
        "5":    (By.XPATH, "//form[@class='sc-brSaZW iUjnAz']/div[2]/div/div[1]//input"),  # Номер заявки
        "6":    (By.XPATH, "//form[@class='sc-brSaZW iUjnAz']/div[2]/div/div[2]//input"),  # Номер счета
        "7":    (By.XPATH, "//form[@class='sc-brSaZW iUjnAz']/div[2]/div/div[3]//input"),  # Номер обращения
        "8":    (By.XPATH, "//form[@class='sc-brSaZW iUjnAz']/div[2]/div/div[4]//input"),  # Номер договора
        "9":    (By.XPATH, "//form[@class='sc-brSaZW iUjnAz']/div[2]/div/div[5]//input"),  # ID клиента CRM
        "10":   (By.XPATH, "//form[@class='sc-brSaZW iUjnAz']/div[2]/div/div[6]//input")   # ID дебетовой карты
    }

    # Данные документов в результатах поиска
    LOCATORS_DOCUMENTS_DATA = {
        "DATE": (By.XPATH, "//tbody[@class='MuiTableBody-root']/tr/td[3]")  # Дата изменения документа
    }

    def go_to_doc_search(self):
        """Переход в раздел поиска документов"""
        self.element_is_enabled(locator=self.LINK_SEARCH_DOCUMENT)  # Ожидание элемента
        self.click(locator=self.LINK_SEARCH_DOCUMENT)

    def add_file_for_document(self, file_name):
        """
        Загрузка файла для создаваемого документа.
        :param file_name: Прикрепляемый файл.
        """
        self.send_keys(locator=self.INPUT_FILE_UPLOAD,
                       value=str(Path(os.getcwd(), "files", file_name)))  # Прикрепление файла
        logger.info(f"Добавляемый файл: {file_name}")
        logger.info(f"Добавленный файл: {self.get_text(locator=self.FILE_NAME_IN_DOCUMENT)}")

        # Проверка, что файл прикрепился к документу
        assert self.get_text(locator=self.FILE_NAME_IN_DOCUMENT) == file_name

    def add_files_for_document(self, file_name, num):
        """
        Загрузка файлов для создаваемого документа.
        :param file_name: Прикрепляемый файл.
        :param num: Локатор добавленного файла
        """
        self.send_keys(locator=self.INPUT_FILE_UPLOAD,
                       value=str(Path(os.getcwd(), "files", file_name)))  # Прикрепление файла
        logger.info(f"Добавляемый файл: {file_name}")
        logger.info(f"Добавленный файл: {self.get_text(locator=self.FILE_NAMES_IN_DOCUMENT[num])}")

        # Проверка, что файл прикрепился к документу
        assert self.get_text(locator=self.FILE_NAMES_IN_DOCUMENT[num]) == file_name

    def add_5_files_for_document(self):
        """
        Загрузка файла для создаваемого документа.
        """
        file_names = ["upload_file.png", "upload_file.jpg", "upload_file.jpeg", "upload_file.pdf", "upload_file.txt"]
        for file_name in file_names:
            self.send_keys(locator=self.INPUT_FILE_UPLOAD,
                           value=str(Path(os.getcwd(), "files", file_name)))  # Прикрепление файла
            logger.info(f"Добавляемый файл: {file_name}")

    def download_file(self, directory="download_files"):
        """Скачивание файла в режиме просмотра документа."""
        self.element_is_enabled(locator=self.DOCUMENT_PREVIEW)  # Ожидание загрузки элемента
        self.click(locator=self.BUTTON_DOWNLOAD_FILE)
        download_wait(directory=directory)
        assertion_downloaded_file_in_directory(directory=directory, file_name=DocumentNotice.FILE_NAME_PNG)
        deleting_png_files(directory=directory)

    def upload_file(self, file_name):
        """
        Загрузка файла в просматриваемый документа.
        :param file_name: Прикрепляемый файл.
        """
        self.element_is_enabled(locator=self.BUTTON_ACTIONS)  # Ожидание, что кнопка стала активна
        self.click(locator=self.BUTTON_ACTIONS)  # Клик по кнопке "Действия"
        self.element_is_enabled(locator=self.LINK_UPLOAD_FILE)  # Ожидание, что кнопка стала активна
        self.click(locator=self.LINK_UPLOAD_FILE)  # Клик по подменю "Загрузить файл"

        # Проверка, что появилось окно загрузки файла
        self.element_is_displayed(locator=self.TITLE_UPLOAD_FILE)  # Ожидание появления элемента
        assert self.get_text(locator=self.TITLE_UPLOAD_FILE) == DocumentNotice.TITLE_UPLOAD_FILE

        self.send_keys(locator=self.INPUT_FILE_UPLOAD,
                       value=str(Path(os.getcwd(), "files", file_name)))  # Прикрепление файла
        # Проверка, что файл прикрепился к документу
        assert self.get_text(locator=self.FILE_NAME_IN_DOCUMENT) == file_name
        self.click(locator=self.BUTTON_UPLOAD)  # Клик по кнопке "Загрузить"

    def delete_file(self):
        """Удаление прикрепленного файла документа."""
        self.element_is_enabled(locator=self.BUTTON_ACTIONS)  # Ожидание, что кнопка стала активна
        self.click(locator=self.BUTTON_ACTIONS)  # Клик по кнопке "Действия"
        self.element_is_enabled(locator=self.LINK_DELETE_FILE)  # Ожидание, что кнопка стала активна
        self.click(locator=self.LINK_DELETE_FILE)  # Клик по подменю "Удалить файл"
        self.element_is_enabled(locator=self.BUTTON_DELETE)  # Ожидание, что кнопка стала активна
        self.click(locator=self.BUTTON_DELETE)  # Подтверждение удаления файла

    def data_entry_for_search_document(self, locator, document_data):
        """
        Ввод данных в поля поиска документа.
        :param locator: Локатор поля для поиска документа.
        :param document_data: Принимает сгенерированное значение из фикстуры создания документа.
        """
        self.send_keys(locator=locator, value=document_data)  # Ввод значения в поля для поиска документа

    def add_document_type(self, document_type, document_type_locator, document_type_name):
        """
        Добавление типа документа для поиска;
        :param document_type: тип документа;
        :param document_type_locator: локатора типа документа;
        :param document_type_name: название типа документа.
        """
        self.click(locator=self.BUTTON_ADD_DOCUMENT_TYPE)  # Клик по кнопке "Добавить тип документа"
        self.assertion_window_opening()
        self.click(locator=document_type)  # Выбор нужного типа документа из списка
        self.click(locator=self.BUTTON_SELECT)  # Клик по кнопке "Выбрать"
        self.assertion_document_selection(document_type_locator=document_type_locator,
                                          document_type_name=document_type_name)

    def open_form_to_create_document(self):
        """Открытие формы создания документа."""
        self.element_is_enabled(locator=self.BUTTON_CREATE)  # Ожидание элемента
        self.click(locator=self.BUTTON_CREATE)  # Клик по кнопке "Создать документ"

        # Проверка, что открылась форма создания документа
        self.element_is_enabled(locator=self.TITLE_CREATE_DOCUMENT)  # Ожидание элемента
        logger.info(f"Заголовок окна: {self.get_text(locator=self.TITLE_CREATE_DOCUMENT)}")
        assert self.get_text(locator=self.TITLE_CREATE_DOCUMENT) == DocumentNotice.TITLE_CREATE_DOCUMENT

    def selection_document_type(self, type_name):
        """
        Выбор типа документа.
        :param type_name: Имя типа документа.
        """
        self.click(locator=self.SELECT_FIELD_DOCUMENT_TYPE)  # Клик по полю "Тип документа"
        self.assertion_window_opening()
        self.click(locator=type_name)  # Выбор типа документа из списка
        self.click(locator=self.BUTTON_SELECT)  # Клик по кнопке "Выбрать"

    def selection_document_type_in_folder(self, folder_name, type_name):
        """
        Выбор типа документа в папке.
        :param folder_name: Имя папки с типами документов.
        :param type_name: Имя типа документа.
        """
        self.click(locator=self.SELECT_FIELD_DOCUMENT_TYPE)  # Клик по полю "Тип документа"
        self.assertion_window_opening()
        self.click(locator=folder_name)  # Клик по папке для раскрытия списка типов документов
        self.click(locator=type_name)  # Выбор типа документа из списка
        self.click(locator=self.BUTTON_SELECT)  # Клик по кнопке "Выбрать"

    def selection_file_type(self, type_name):
        """
        Выбор типа файла.
        :param type_name: Тип файла.
        """
        self.click(locator=self.FIELD_FILE_TYPE)
        self.click(locator=type_name)
        # Проверка появления предупреждения с разрешенными расширениями прикрепляемого файла
        self.element_is_enabled(locator=self.AVAILABLE_EXTENSIONS)  # Ожидание элемента
        assert DocumentNotice.AVAILABLE_EXTENSIONS in self.get_text(locator=self.AVAILABLE_EXTENSIONS)

    def data_entry_to_create_document(self, doc_type, document_data):
        """
        Ввод данных в форме создания документа.
        :param doc_type: Тип документа.
        :param document_data: Принимает рандомное значение из теста.
        """
        self.click(locator=self.SELECT_FIELD_DOCUMENT_TYPE)  # Клик по полю "Тип документа"
        self.assertion_window_opening()
        self.click(locator=doc_type)  # Выбор нужного типа документа из списка
        self.click(locator=self.BUTTON_SELECT)  # Клик по кнопке "Выбрать"
        # Цикл проходит по всем полям ввода заполняя их сгенерированными значениями
        for locator in self.LOCATORS_METADATA_TO_CREATE_DOCUMENT.values():
            self.send_keys(locator=locator, value=document_data)

    def additional_metadata_entry_to_create_document(self):
        """Ввод дополнительных метаданных в форме создания документа."""
        self.send_keys(locator=self.LOCATORS_ADDITIONAL_METADATA_TO_CREATE_DOCUMENT["NUMBER"], value="1234567890")
        self.send_keys(locator=self.LOCATORS_ADDITIONAL_METADATA_TO_CREATE_DOCUMENT["DATE"],
                       value=date.today().strftime("%d.%m.%Y"))
        self.send_keys(locator=self.LOCATORS_ADDITIONAL_METADATA_TO_CREATE_DOCUMENT["STRING"], value="Строка")

    def document_create(self):
        """Клик по кнопке для создания документа"""
        self.element_is_displayed(locator=self.BUTTON_CREATE)  # Ожидание появления элемента
        self.click(locator=self.BUTTON_CREATE)  # Клик по кнопке "Создать документ"

        # Проверка появления уведомления об успешном создании документа
        self.element_is_enabled(locator=self.SUCCESS_DOCUMENT_CREATE)  # Ожидание появления элемента
        logger.info(f"Текст всплывашки: {self.get_text(locator=self.SUCCESS_DOCUMENT_CREATE)}")
        assert self.get_text(locator=self.SUCCESS_DOCUMENT_CREATE) == DocumentNotice.SUCCESS_DOCUMENT_CREATE

    def create_document_without_data(self, locator_document_type, locator_error_required_field):
        """
        Создание документа без заполнения полей.
        :param locator_document_type: Локатор типа документа.
        :param locator_error_required_field: Локатор предупреждения незаполненности поля.
        """
        self.element_is_enabled(locator=self.SELECT_FIELD_DOCUMENT_TYPE)  # Ожидание появления элемента
        self.click(locator=self.SELECT_FIELD_DOCUMENT_TYPE)  # Клик по полю "Тип документа"
        self.assertion_window_opening()
        self.click(locator=locator_document_type)  # Выбор нужного типа документа из списка
        self.click(locator=self.BUTTON_SELECT)  # Клик по кнопке "Выбрать"
        self.click(locator=self.BUTTON_CREATE)  # Клик по кнопке "Создать документ"

        # Проверка появления предупреждения, что поле не заполнено
        assert self.get_text(locator=locator_error_required_field) == DocumentNotice.ERROR_REQUIRED_FIELD

    def data_entry_and_search_document(self, document_data):
        """
        Ввод данных в поля для поиска документа.
        Цикл проходит по всем полям по которым можно найти документ, проверяя корректность данных документа.
        :param document_data: Принимает возвращаемые генерируемые данные из фикстуры создания документа.
        """
        for num, locator in self.LOCATORS_METADATA_TO_SEARCH_DOCUMENT.items():
            self.send_keys(locator=locator, value=document_data)  # Ввод значения в поля для поиска документа
            self.document_search()

            # Проверяем, что значения полей найденного документа равны значениям при создании документа
            self.element_is_enabled(locator=self.LINES_PER_PAGE)  # Ожидание загрузки страницы
            assert self.get_text(locator=(By.XPATH, f"//tbody[@class='MuiTableBody-root']//td[{num}]")) == document_data
            self.click(locator=self.LINK_SEARCH_DOCUMENT)  # Переход/возврат в форму поиска документов

    def select_only_signed_documents(self):
        """Перевод бегунка для поиска только подписанных документов"""
        self.click(locator=self.CHECKBOX_ONLY_SIGNED_DOCUMENTS)  # Клик по чекбоксу "Только подписанные" в поиске

    def document_search(self):
        """Поиск документа с уже выбранным типом документа."""
        self.element_is_enabled(locator=self.BUTTON_SEARCH)  # Ожидание элемента
        self.click(locator=self.BUTTON_SEARCH)  # Клик по кнопке "Найти" для поиска документов
        self.assertion_go_to_search_page()

    def document_open(self):
        """Открытие найденного документа для редактирования."""
        self.element_is_enabled(locator=self.LINK_DOCUMENT)  # Ожидание элемента
        self.click(locator=self.LINK_DOCUMENT)  # Клик по ссылке на документ для открытия
        self.assertion_document_opened_for_viewing()

    def open_document(self):
        """Открытие выбранного документа для редактирования."""
        self.document_search()
        self.element_is_enabled(locator=self.LINK_DOCUMENT)  # Ожидание элемента
        self.click(locator=self.LINK_DOCUMENT)  # Клик по ссылке на документ для открытия
        self.assertion_document_opened_for_viewing()

    def assertion_display_of_4_files_previews(self):
        """Проверка отображение превью файлов в режиме просмотра документа."""
        for file_name in ['upload_file.png', 'upload_file.jpg', 'upload_file.jpeg']:
            self.element_is_enabled(locator=self.DROPDOWN_FILE)  # Ожидание элемента
            self.click(locator=self.DROPDOWN_FILE)  # Клик по полю прикрепленных файлов документа
            self.element_is_enabled(locator=(By.XPATH, f"//li[contains(text(), '{file_name}')]"))  # Ожидание элемента
            self.click(locator=(By.XPATH, f"//li[contains(text(), '{file_name}')]"))  # Выбор нужного файла
            self.element_is_enabled(locator=self.DOCUMENT_PREVIEW)  # Ожидание загрузки превью файла
        self.element_is_enabled(locator=self.DROPDOWN_FILE)  # Ожидание элемента
        self.click(locator=self.DROPDOWN_FILE)  # Клик по полю прикрепленных файлов документа
        self.click(locator=(By.XPATH, f"//li[contains(text(), 'upload_file.pdf')]"))  # Выбор нужного PDF файла
        self.element_is_enabled(locator=self.PDF_DOCUMENT_PREVIEW)  # Ожидание загрузки превью PDF файла

    def select_document_version(self):
        """
        Выбор версии документа.
        Если первая версия документа актуальна - выбирается вторая версия(неактуальная). И наоборот.
        """
        self.click(locator=self.DROPDOWN_DOCUMENT_VERSION)  # Клик для выбора версии документа
        if self.get_text(locator=self.DROPDOWN_DOCUMENT_VERSION) == DocumentNotice.DOCUMENT_VERSION_1_ACTUAL:
            self.click(locator=self.DROPDOWN_DOCUMENT_VERSION_2)  # Выбор второй версии документа
            self.document_version_change(document_version=DocumentNotice.DOCUMENT_VERSION_2_ACTUAL)
        else:
            self.click(locator=self.DROPDOWN_DOCUMENT_VERSION_1)  # Выбор первой версии документа
            self.document_version_change(document_version=DocumentNotice.DOCUMENT_VERSION_1_ACTUAL)

    def document_version_change(self, document_version):
        """Изменение версии документа."""
        self.click(locator=self.BUTTON_ACTIONS)  # Клик кнопки Действие
        self.click(locator=self.BUTTON_DOCUMENT_VERSION_ACTUAL)  # Клик Сделать версию документа актуальной
        self.click(locator=self.BUTTON_CONFIRM)  # Подтвердить

        # Проверка, что в списке версий у текущей версии появился признак "(актуальная)"
        assert self.get_text(locator=self.DROPDOWN_DOCUMENT_VERSION) == document_version

    def go_to_tab_electronic_signature(self):
        """Переход на вкладку Подписание ЭП в режиме просмотра документа."""
        self.click(locator=self.ELECTRONIC_SIGNATURE)

    def checking_electronic_signature_of_document(self):
        """
        Переход во вкладку Подписание ЭП в режиме просмотра документа.
        Проверка, что найденный документ имеет статус Подписан.
        """
        time.sleep(1)
        self.click(locator=self.ELECTRONIC_SIGNATURE)  # Переход в вкладку Подписание ЭП
        logger.info(f"Статут ЭП: {self.get_text(locator=self.STATUS_ELECTRONIC_SIGNATURE)}")
        # Проверка, что открытый документ подписан ЭП
        assert self.get_text(locator=self.STATUS_ELECTRONIC_SIGNATURE) == DocumentNotice.STATUS_ELECTRONIC_SIGNATURE

    def metadata_editing(self):
        """Открытие документа в режиме редактирования."""
        self.element_is_enabled(locator=self.BUTTON_ACTIONS)  # Ожидание появления элемента
        self.click(locator=self.BUTTON_ACTIONS)  # Клик по кнопке "Действие"
        self.element_is_enabled(locator=self.EDIT_METADATA)  # Ожидание появления элемента
        self.click(locator=self.EDIT_METADATA)  # Клик в выпадающем меню "Редактировать метаданные"

        # Проверка, что документ открылся для редактирования
        self.element_is_enabled(locator=self.TITLE_METADATA_EDITING)  # Ожидание появления элемента
        logger.info(f"Заголовок окна: {self.get_text(locator=self.TITLE_METADATA_EDITING)}")
        assert self.get_text(locator=self.TITLE_METADATA_EDITING) == DocumentNotice.TITLE_METADATA_EDITING

    def add_document_date(self):
        """Добавить сегодняшнюю дату в редактируемый документ."""
        self.element_is_enabled(locator=self.DATE_FIELD)  # Ожидание появления элемента
        self.send_keys(locator=self.DATE_FIELD, value=datetime.datetime.now().strftime('%d.%m.%Y'))

    def save_document(self):
        """Сохранения документа после редактирования."""
        self.element_is_enabled(locator=self.BUTTON_SAVE)  # Ожидание появления элемента
        self.click(locator=self.BUTTON_SAVE)  # Клик по кнопке "Сохранить"
        self.assertion_document_opened_for_viewing()  # Проверка, что открылся документ после сохранения

    def editing_document(self, document_data):
        """Редактирование метаданных документа."""
        self.element_is_enabled(locator=self.BUTTON_ACTIONS)  # Ожидание появления элемента
        self.click(locator=self.BUTTON_ACTIONS)  # Клик по кнопке "Действие"
        self.element_is_enabled(locator=self.EDIT_METADATA)  # Ожидание появления элемента
        self.click(locator=self.EDIT_METADATA)  # Клик в выпадающем меню "Редактировать метаданные"

        # Проверка, что документ открылся для редактирования
        self.element_is_enabled(locator=self.TITLE_METADATA_EDITING)  # Ожидание появления элемента
        logger.info(f"Заголовок окна: {self.get_text(locator=self.TITLE_METADATA_EDITING)}")
        assert self.get_text(locator=self.TITLE_METADATA_EDITING) == DocumentNotice.TITLE_METADATA_EDITING

        # Цикл проходит по всем полям ввода очищая их заполняя новыми значениями
        for locator in self.LOCATORS_METADATA.values():
            self.clear_by_deletion(locator=locator)
            self.send_keys(locator=locator, value=document_data)
        self.click(locator=self.BUTTON_SAVE)  # Клик по кнопке "Сохранить"
        self.assertion_document_opened_for_viewing()
        self.assertion_data_saved(document_data=document_data)

    def change_file_relevance(self, locator_button_dropdown_menu):
        """
        Изменение актуальности файла.
        :param locator_button_dropdown_menu: Принимает локатор необходимого действия над документом
        """
        self.click(locator=self.BUTTON_ACTIONS)  # Клик по кнопке "Действие"
        self.click(locator=locator_button_dropdown_menu)  # Выбор пункта в выпадающем меню
        self.click(locator=self.BUTTON_CONFIRM)  # Клик по кнопке "Подтвердить"

        # Проверка, что файл в статусе актуальный
        # time.sleep(0.5)
        # self.element_is_enabled(locator=self.DOCUMENT_PREVIEW)  # Ожидание загрузки страницы
        # assert DocumentNotice.STATUS_FILE_ACTUAL in self.get_text(locator=self.FILE_RELEVANCE_STATUS)

    def assertion_file_is_up_to_date(self):
        """Проверка, что файл в статусе актуальный."""
        time.sleep(0.5)
        self.element_is_enabled(locator=self.DOCUMENT_PREVIEW)  # Ожидание загрузки страницы
        assert DocumentNotice.STATUS_FILE_ACTUAL in self.get_text(locator=self.FILE_RELEVANCE_STATUS)

    def assertion_file_is_out_of_date(self):
        """Проверка, что файл в статусе неактуальный."""
        time.sleep(0.5)
        self.element_is_enabled(locator=self.DOCUMENT_PREVIEW)  # Ожидание загрузки страницы
        assert DocumentNotice.STATUS_FILE_ACTUAL is not self.get_text(locator=self.FILE_RELEVANCE_STATUS)

    def select_40_documents(self):
        """Выбрать 40 найденных документов."""
        self.element_is_enabled(locator=self.WAITING_FOR_SEARCH_RESULT)  # Ожидание появления элемента
        self.click(locator=self.CHECKBOX_SELECT_20_DOCUMENTS)  # Выбрать 20 документов
        self.element_is_enabled(locator=self.BUTTON_NEXT_PAGE)  # Ожидание появления элемента
        self.click(locator=self.BUTTON_NEXT_PAGE)  # Переход на вторую страницу
        self.element_is_enabled(locator=self.WAITING_FOR_SEARCH_RESULT)  # Ожидание появления элемента
        self.click(locator=self.CHECKBOX_SELECT_20_DOCUMENTS)  # Выбрать еще 20 документов на следующей странице

    def download_documents(self):
        """Скачивание выбранных документов в поиске."""
        self.click(locator=self.BUTTON_DOWNLOAD)  # Скачать
        self.element_is_enabled(locator=self.FAILURE_DOWNLOAD_MORE_20_DOCUMENTS)  # Ожидание появления элемента
        logger.info(f"Текст всплывашки: {self.get_text(locator=self.FAILURE_DOWNLOAD_MORE_20_DOCUMENTS)}")
        assert self.get_text(
            locator=self.FAILURE_DOWNLOAD_MORE_20_DOCUMENTS) == DocumentNotice.FAILURE_DOWNLOAD_MORE_20_DOCUMENTS

    def get_document_modification_date(self):
        """Получение даты создания или изменения документа."""
        self.element_is_enabled(locator=self.LOCATORS_DOCUMENTS_DATA['DATE'])  # Ожидание элемента
        modification_date = self.get_text(locator=self.LOCATORS_DOCUMENTS_DATA['DATE'])
        logger.info(f"Дата изменения документа: {self.get_text(locator=self.LOCATORS_DOCUMENTS_DATA['DATE'])}")
        return modification_date

    def assertion_window_opening(self):
        """Проверка и логирование успешного открытия окна выбора типа документа."""
        time.sleep(0.25)
        self.element_is_enabled(locator=self.TITLE_DOCUMENT_TYPE_SELECTION_WINDOW)  # Ожидание появления элемента
        logger.info(f"Заголовок окна: {self.get_text(locator=self.TITLE_DOCUMENT_TYPE_SELECTION_WINDOW)}")
        assert self.get_text(
            locator=self.TITLE_DOCUMENT_TYPE_SELECTION_WINDOW) == DocumentNotice.TITLE_DOCUMENT_TYPE_SELECTION_WINDOW

    def assertion_document_selection(self, document_type_locator=None, document_type_name=None):
        """
        Проверка и логирование успешного выбора типа документа;
        :param document_type_locator: локатора типа документа;
        :param document_type_name: название типа документа.
        """
        logger.info(f"Выбран тип документа: {document_type_locator}")
        # Проверка, что выбрался нужный документ
        self.element_is_enabled(locator=document_type_locator)  # Ожидание появления элемента
        assert self.get_text(locator=document_type_locator) == document_type_name

    def assertion_go_to_search_page(self):
        """Проверка и логирование успешного перехода на страницу поиска документа."""
        logger.info(f"Заголовок окна: {self.get_text(locator=self.SEARCH_RESULT)}")
        # Проверка, что произошел переход на страницу результатов поиска документа
        assert self.get_text(locator=self.SEARCH_RESULT) == DocumentNotice.SEARCH_RESULT

    def assertion_document_opened_for_viewing(self):
        """Проверка и логирование успешного открытия документа для просмотра."""
        logger.info(f"Заголовок метаданных: {self.get_text(locator=self.TITLE_METADATA_AND_VALUES)}")
        # Проверка, что документ открылся для просмотра
        assert DocumentNotice.TITLE_METADATA_AND_VALUES in self.get_text(locator=self.TITLE_METADATA_AND_VALUES)

    def assertion_data_saved(self, document_data):
        """Проверка и логирование успешного сохранения данных после редактирования."""
        time.sleep(1)
        self.element_is_enabled(locator=self.DOCUMENT_PREVIEW)  # Ожидание загрузки страницы
        logger.info(f"Метаданные и значения: {self.get_text(locator=self.METADATA_AND_VALUES)}")

        # Проверка, что данные сохранились после редактирования
        assert self.get_text(locator=self.METADATA_AND_VALUES) == document_data

    def assertion_document_found(self, document_data):
        """
        Проверка, что найденный документ соответствует искомому.
        :param document_data: Номер заявки документа
        """
        self.element_is_enabled(locator=(By.XPATH, "//tbody[@class='MuiTableBody-root']//td[5]/span"))  # Ожидание
        assert self.get_text(locator=(By.XPATH, "//tbody[@class='MuiTableBody-root']//td[5]/span")) == document_data

    def assertion_display_preview_file(self):
        """Проверка отображения превью файла в режиме просмотра документа."""
        # app.base_page.element_is_enabled(locator=DocumentsPage.DOCUMENT_PREVIEW)
        self.element_is_enabled(locator=self.DOCUMENT_PREVIEW)  # Ожидание загрузки страницы
        logger.info(f"Атрибут превью файла: {self.get_attribute(locator=self.DOCUMENT_PREVIEW, attribute='alt')}")
        assert self.get_attribute(locator=self.DOCUMENT_PREVIEW, attribute="alt") == "Документ"
