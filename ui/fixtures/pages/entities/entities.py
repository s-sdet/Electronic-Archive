import logging
import random

from selenium.webdriver.common.by import By
from ui.fixtures.pages.base_page import BasePage
from ui.data.constants import EntitiesNotice

logger = logging.getLogger("Electronic Archive")


class CreateEntitiesModel:
    """Генерация рандомных данных для валидного создания сущности."""

    def __init__(self, entity_system_name: str = None, entity_display_name: str = None, attribute_number: str = None,
                 attribute_system_name: str = None, attribute_display_name: str = None):
        self.entity_system_name = entity_system_name
        self.entity_display_name = entity_display_name
        self.attribute_number = attribute_number
        self.attribute_system_name = attribute_system_name
        self.attribute_display_name = attribute_display_name

    @staticmethod
    def random_valid_data_for_entity():
        entity_system_name = f"{EntitiesNotice.ENTITY_SYSTEM_NAME}{random.randint(10, 1000)}"
        entity_display_name = f"{EntitiesNotice.ENTITY_DISPLAY_NAME}{random.randint(10, 1000)}"
        attribute_number = str(random.randint(10, 1000))
        attribute_system_name = f"{EntitiesNotice.ATTRIBUTE_SYSTEM_NAME}{random.randint(10, 1000)}"
        attribute_display_name = f"{EntitiesNotice.ATTRIBUTE_DISPLAY_NAME}{random.randint(10, 1000)}"
        return CreateEntitiesModel(entity_system_name=entity_system_name, entity_display_name=entity_display_name,
                                   attribute_number=attribute_number, attribute_system_name=attribute_system_name,
                                   attribute_display_name=attribute_display_name)


class EntitiesPage(BasePage):
    """Страница поиска и создания сущностей https://electronicarchive-frontend-afds.dev.akbars.ru/entities/search"""

    LINK_ENTITIES = (By.XPATH, "//div[@id='root']//nav/div[2]/div[2]")  # Ссылка на раздел Сущности
    TITLE_ENTITIES = (By.XPATH, "//h2[contains(text(), 'Сущности')]")  # Заголовок раздела

    # Кнопки
    BUTTON_ENTITY_CREATE = (By.XPATH, "//span[contains(text(), 'Создать тип сущности')]")  # Создать тип сущности
    BUTTON_ADD_ATTRIBUTE = (By.XPATH, "//span[contains(text(), 'Добавить атрибут')]")  # Добавить атрибут
    BUTTON_ADD = (By.XPATH, "//div[@class='sc-kFCsca dUsTPr']/form/div[2]/div")  # Добавить
    BUTTON_CREATE = (By.XPATH, "//span[contains(text(), 'Создать')]")  # Создать

    # Поля для ввода данных типа сущности
    FIELD_ENTITY_SYSTEM_NAME = (By.NAME, "systemName")  # Системное название
    FIELD_ENTITY_DISPLAY_NAME = (By.NAME, "displayName")  # Отображаемое название

    # Поля для ввода данных атрибута
    FIELD_ATTRIBUTE_NUMBER = (By.NAME, "displayIndex")  # Порядковый номер
    FIELD_ATTRIBUTE_SYSTEM_NAME = (By.XPATH, "//div[@class='sc-kFCsca dUsTPr']/form/div/div[2]//input")  # Системное
    FIELD_ATTRIBUTE_DISPLAY_NAME = (By.XPATH, "//div[@class='sc-kFCsca dUsTPr']/form/div/div[3]//input")  # Отображаемое
    FIELD_DATA_TYPE = (By.XPATH, "//div[@class='sc-kFCsca dUsTPr']/form/div/div[4]")  # Тип данных

    DATA_TYPE = (By.XPATH, "//div[@id='menu-valueType']//ul/li[1]")  # Тип данных
    CHECKBOX = (By.XPATH, "//label[@data-testid='formCheckbox']")  # Чексбокс Обязательный
    ENTITY_SYSTEM_NAME = (By.XPATH, "//tbody[@class='MuiTableBody-root']/tr/td[2]")  # Системное название после создания
    SUCCESS_ENTITY_CREATE = (By.XPATH, "//div[@class='MuiCollapse-wrapperInner']")  # Тип сущности успешно создан

    def go_to_entities(self):
        """Переход в раздел Сущности."""
        self.click(locator=self.LINK_ENTITIES)
        logger.info(f"Заголовок раздела: {self.get_text(locator=self.TITLE_ENTITIES)}")
        # Проверка, что переход в раздел "Сущности" выполнен
        assert self.get_text(locator=self.TITLE_ENTITIES) == EntitiesNotice.TITLE_ENTITIES

    def fill_entity_type_creation_form(self, data: CreateEntitiesModel):
        """Открытие формы создания сущности."""
        self.element_is_enabled(locator=self.BUTTON_ENTITY_CREATE)  # Ожидание элемента
        self.click(locator=self.BUTTON_ENTITY_CREATE)  # Клик по кнопке "Создать тип сущности"
        logger.info(f"Системное название типа: {data.entity_system_name}, "
                    f"Отображаемое название типа: {data.entity_display_name}, "
                    f"Порядковый номер атрибута: {data.attribute_number}, "
                    f"Системное название атрибута: {data.attribute_system_name}, "
                    f"Отображаемое название атрибута: {data.attribute_display_name}")

        self.send_keys(locator=self.FIELD_ENTITY_SYSTEM_NAME, value=data.entity_system_name)  # Системное название
        self.send_keys(locator=self.FIELD_ENTITY_DISPLAY_NAME, value=data.entity_display_name)  # Отображаемое название
        self.fill_entity_attribute_creation_form(attribute_number=data.attribute_number,
                                                 attribute_system_name=data.attribute_system_name,
                                                 attribute_display_name=data.attribute_display_name)
        self.click(locator=self.BUTTON_CREATE)  # Клик по кнопке "Создать"

        # Проверка появления уведомления об успешном создании сущности
        self.element_is_enabled(locator=self.SUCCESS_ENTITY_CREATE)  # Ожидание элемента
        logger.info(f"Текст уведомления: {self.get_text(locator=self.SUCCESS_ENTITY_CREATE)}")
        assert self.get_text(locator=self.SUCCESS_ENTITY_CREATE) == EntitiesNotice.SUCCESS_ENTITY_CREATE

    def fill_entity_attribute_creation_form(self, attribute_number, attribute_system_name, attribute_display_name):
        """
        Добавление атрибутов при создании сущности.
        :param attribute_number: Порядковый номер
        :param attribute_system_name: Системное название
        :param attribute_display_name: Отображаемое название
        """
        self.click(locator=self.BUTTON_ADD_ATTRIBUTE)  # Клик по кнопке "Добавить атрибут"
        self.send_keys(locator=self.FIELD_ATTRIBUTE_NUMBER, value=attribute_number)  # Порядковый номер
        self.send_keys(locator=self.FIELD_ATTRIBUTE_SYSTEM_NAME, value=attribute_system_name)  # Системное название
        self.send_keys(locator=self.FIELD_ATTRIBUTE_DISPLAY_NAME, value=attribute_display_name)  # Отображаемое название
        self.click(locator=self.FIELD_DATA_TYPE)  # Клик по полю "тип данных"
        self.click(locator=self.DATA_TYPE)  # Выбор нужного типа данных
        self.click(locator=self.CHECKBOX)  # Выбор чекбокса "Обязательный"
        self.click(locator=self.BUTTON_ADD)  # Клик по кнопке "Добавить"

        # Проверка, что атрибут со всеми заполненными полями отображается в списке атрибутов
        assert self.get_text(locator=self.ENTITY_SYSTEM_NAME) == attribute_system_name
