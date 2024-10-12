import datetime
import os
import pytest
import logging
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ui.fixtures.app import Application
from ui.data.constants import DocumentNotice, InstructionsNotice
from ui.fixtures.pages.document.documents import DocumentsPage
from ui.fixtures.pages.administration.document_types import CreateDocumentsTypeModel

logger = logging.getLogger("Live Plus - Electronic Archive")


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://***.ru/",  # DEV
        # default="https://***.ru/",  # STAGE
        help="DEV UI url",
    ),
    parser.addoption("--headless", action="store_true", help="Headless mode"),


@pytest.fixture
def app(request):
    url = request.config.getoption("--url")
    logger.info(f"Start UI tests Electronic Archive, url is {url}")
    headless = request.config.getoption("--headless")
    options = Options()
    # options.add_argument("--start-maximized")
    options.add_argument("window-size=1920,1080")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("prefs", {"download.default_directory": os.getcwd()+"\\download_files\\"})
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    app = Application(driver, url)
    yield app
    app.driver.close()
    app.quit()


@pytest.fixture
def open_login_page(app):
    """Фикстура авторизации пользователя."""
    app.login.open_login_page()


@pytest.fixture
def login_user(app, open_login_page):
    """Фикстура авторизации пользователя."""
    app.login.entry_data_authorization()


@pytest.fixture
def go_to_search(app):
    """Фикстура перехода в раздел Хранилище документов"""
    app.document.go_to_doc_search()


@pytest.fixture
def go_to_entities(app, login_user):
    """Фикстура перехода в раздел Сущности."""
    app.entities.go_to_entities()


@pytest.fixture
def go_to_instructions(app, login_user):
    """Фикстура перехода на вкладку Просмотр инструкций."""
    app.instructions.click_link_updates_and_instructions()
    app.instructions.click_link_instructions()

    #  Проверка, что переход на вкладку "Просмотр инструкций" выполнен
    assert app.base_page.get_url() == InstructionsNotice.URL_INSTRUCTIONS.format(app.url)


@pytest.fixture
def go_to_admin_panel(app, login_user):
    """Фикстура перехода в раздел Администрирование."""
    app.doc_type.open_admin_panel()


@pytest.fixture
def random_document_data(app):
    """Фикстура генерации значений метаданных для документов."""
    random_data = str(random.randint(1000, 10000000000))
    logger.info(f"Рандомное значение: {random_data}")
    return random_data


@pytest.fixture
def create_document(app, login_user, random_document_data):
    """Фикстура создания документа с заполнением всех метаданных валидными значениями."""
    app.document.open_form_to_create_document()
    app.document.data_entry_to_create_document(doc_type=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123,
                                               document_data=random_document_data)
    app.document.document_create()
    return random_document_data


@pytest.fixture()
def create_document_with_all_fields(app, login_user, random_document_data):
    """Фикстура создания документа с типом документа всех полей."""
    app.document.open_form_to_create_document()
    app.document.data_entry_to_create_document(doc_type=DocumentsPage.SELECT_DOCUMENT_TYPE_WITH_ALL_FIELD_TYPES,
                                               document_data=random_document_data)
    app.document.document_create()
    return random_document_data


@pytest.fixture
def create_document_with_png_file(app, login_user, random_document_data):
    """Фикстура создания документа с загрузкой PNG файла и заполнением всех метаданных валидными значениями."""
    app.document.open_form_to_create_document()
    app.document.add_file_for_document(file_name=DocumentNotice.FILE_NAME_PNG)
    app.document.data_entry_to_create_document(doc_type=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123,
                                               document_data=random_document_data)
    app.document.document_create()
    return random_document_data


@pytest.fixture
def create_document_with_pdf_file(app, login_user, random_document_data):
    """Фикстура создания документа с загрузкой PDF файла и заполнением всех метаданных валидными значениями."""
    app.document.open_form_to_create_document()
    app.document.add_file_for_document(file_name=DocumentNotice.FILE_NAME_PDF)
    app.document.data_entry_to_create_document(doc_type=DocumentsPage.SELECT_DOCUMENT_TYPE_EA_123,
                                               document_data=random_document_data)
    app.document.document_create()
    return random_document_data


@pytest.fixture(scope="function")
def create_document_with_different_extensions(app, login_user, random_document_data):
    """
    Фикстура создания документа с загрузкой PNG файла и заполнением всех метаданных валидными значениями.
    Документ создается с типом: 'Тип документа с разными расширениями'.
    """
    app.document.open_form_to_create_document()
    app.document.add_file_for_document(file_name=DocumentNotice.FILE_NAME_PNG)
    app.document.data_entry_to_create_document(doc_type=DocumentsPage.SELECT_DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS,
                                               document_data=random_document_data)
    app.document.selection_file_type(type_name=DocumentsPage.FILE_TYPE_DIFFERENT_EXTENSIONS)
    app.document.document_create()
    return random_document_data


@pytest.fixture
def create_document_with_4_files(app, login_user, random_document_data):
    """
    Фикстура создания документа с загрузкой 4 файлов разных расширений(PNG, JPG, JPEG, PDF).
    Документ создается с типом: 'Тип документа с разными расширениями'.
    """
    app.document.open_form_to_create_document()
    num = 1
    file_names = ['upload_file.png', 'upload_file.jpg', 'upload_file.jpeg', 'upload_file.pdf']
    for file_name in file_names:
        app.document.add_files_for_document(file_name=file_name, num=num)
        num += 1
    app.document.data_entry_to_create_document(doc_type=DocumentsPage.SELECT_DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS,
                                               document_data=random_document_data)
    app.document.document_create()
    return random_document_data


@pytest.fixture
def random_folder_name(app):
    """Фикстура генерации названия папки типов документа."""
    folder_name = f"Папка {random.randint(10, 1000000)}"
    logger.info(f"Название папки: {folder_name}")
    return folder_name


@pytest.fixture
def random_new_folder_name(app):
    """Фикстура генерации названия папки типов документа."""
    new_folder_name = f"Новая папка {random.randint(10, 1000000)}"
    logger.info(f"Новое название папки: {new_folder_name}")
    return new_folder_name


@pytest.fixture
def random_group_name(app):
    """Фикстура генерации названия группы AD."""
    group_name = f"Группа {random.randint(10, 1000000)}"
    logger.info(f"Название группы: {group_name}")
    return group_name


@pytest.fixture
def random_second_group_name(app):
    """Фикстура генерации названия второй группы AD."""
    second_group_name = f"Вторая группа {random.randint(10, 1000000)}"
    logger.info(f"Название второй группы: {second_group_name}")
    return second_group_name


@pytest.fixture
def create_folder(app, go_to_admin_panel, random_folder_name, random_group_name):
    """Фикстура создания папки типов документов в панели администрирования."""
    app.doc_type.open_form_to_create_folder()
    app.doc_type.data_entry_to_create_folder(folder_name=random_folder_name, group_name=random_group_name)
    app.doc_type.create_folder()
    return random_folder_name


@pytest.fixture(scope="function")
def create_doc_type(app, go_to_admin_panel):
    """Фикстура создания типа документа."""
    data = CreateDocumentsTypeModel.random_valid_data_for_doc_type()
    app.doc_type.open_form_doc_type_create()
    app.doc_type.data_entry_doc_type(data=data)
    app.doc_type.data_entry_file_types(data=data)
    app.doc_type.data_entry_metadata_type(data=data)
    app.doc_type.creation_type()
    return data.document_type_name


@pytest.fixture(scope="function")
def document_creation_date():
    """Фикстура определения даты и времени."""
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября',
              'ноября', 'декабря']
    mont = int(datetime.date.today().strftime("%m"))
    date = datetime.datetime.today().strftime(f"%d {months[mont-1]} %Y, %H:%M")
    return date
