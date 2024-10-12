"""Константы, в т.ч. тексты ошибок и уведомлений."""


class LoginNotice:
    """Страница авторизации ***"""
    LOGIN_FORM_TEXT = "Авторизация"  # Заголовок формы авторизации
    URL_DOCUMENT_SEARCH = "{}document/search"  # Раздел Поиск документов
    URL_ENTITIES_SEARCH = "{}entities/search"  # Раздел Сущности
    USER_NAME = "СУЗ для теста UserFatca"  # Отображаемое имя и фамилия пользователя
    TITLE_SEARCH_DOCUMENTS = "Поиск документов"  # Заголовок раздела "Поиск документов"


class DocumentNotice:
    """Страница документов ***"""

    # Типы документа
    DOCUMENT_TYPE_WITH_2_FIELDS = "Тестовый тип документа с 2 дополнительными полями"
    DOCUMENT_TYPE_EA_123 = "ЭА 123"
    DOCUMENT_TYPE_WITH_DIFFERENT_EXTENSIONS = "Тип документа с разными расширениями"
    DOCUMENT_TYPE_FOR_SIGN = "For Sign"

    # Заголовки форм и страниц
    TITLE_DOCUMENT_TYPE_SELECTION_WINDOW = "Выбор типа документа"  # Заголовок всплывашки выбора типа документа
    TITLE_DOCUMENT = "version control"  # Название документа
    TITLE_METADATA_AND_VALUES = "Метаданные и значения"  # Заголовок метаданных
    TITLE_METADATA_EDITING = "Редактирование метаданных"  # Заголовок формы редактирования метаданных документа
    TITLE_NAME_EDITING = "Редактирование название документа"  # Заголовок формы редактирования название документа
    TITLE_CREATE_DOCUMENT = "Создание документа"  # Заголовок формы создания документа
    TITLE_UPLOAD_FILE = "Загрузка файла"  # Заголовок формы загрузки файла

    SEARCH_RESULT = "Результат поиска"  # Заголовок окна результатов поиска документа
    SUCCESS_DOCUMENT_CREATE = "Документ был успешно создан"  # Уведомление об успешном создании документа
    ERROR_INVALID_REQUEST_PARAMETERS = "Переданы некорректные параметры запроса"
    ERROR_EMPTY_DOCUMENT_TITLE = "Поле обязательно для заполнения"
    FAILURE_DOWNLOAD_MORE_20_DOCUMENTS = "Превышено допустимое количество документов (20) для загрузки"

    FILE_NAME_PNG = "upload_file.png"  # PNG файл для загрузки при создании документа
    FILE_NAME_PDF = "upload_file.pdf"  # PDF файл для загрузки при создании документа
    STATUS_FILE_ACTUAL = "актуальный"  # Статус файла
    STATUS_ELECTRONIC_SIGNATURE = "Подписан"  # Статус электронной подписи
    ERROR_REQUIRED_FIELD = "Обязательное поле"  # Предупреждение, что поле не заполнено
    AVAILABLE_EXTENSIONS = "Доступные расширения:"  # Предупреждение формата файла
    DOCUMENT_WITH_TWO_VERSIONS = "3230712777"  # Номер заявки документа с двумя версиями
    DOCUMENT_VERSION_ACTUAL = "{} (актуальная)"  # Статус версии документа
    DOCUMENT_VERSION_1_ACTUAL = "Версия 1 (актуальная)"  # Статус 1-й версии документа
    DOCUMENT_VERSION_2_ACTUAL = "Версия 2 (актуальная)"  # Статус 2-й версии документа


class EntitiesNotice:
    """Страница сущностей ***"""

    TITLE_ENTITIES = "Сущности"  # Заголовок раздела

    # Названия для создания сущности
    ENTITY_SYSTEM_NAME = "EntitySystemName"
    ENTITY_DISPLAY_NAME = "EntityDisplayName"
    ATTRIBUTE_SYSTEM_NAME = "AttributeSystemName"
    ATTRIBUTE_DISPLAY_NAME = "AttributeDisplayName"
    SUCCESS_ENTITY_CREATE = "Тип сущности успешно создан"


class InstructionsNotice:
    """Страница инструкций ***"""

    TITLE_UPDATES_AND_INSTRUCTIONS = "Обновления и инструкции"  # Заголовок раздела
    URL_INSTRUCTIONS = "{}info?tab=Instructions"  # Вкладка Инструкции


class DocumentsTypeNotice:
    """
    Страница администрирования типов документов***
    """

    # Заголовки окон и страниц
    TITLE_ADMIN_PANEL = "Администрирование"  # Страница администрирования
    TITLE_FORM_DOC_TYPE_CREATE = "Создание типа документа"  # Страница "Создание типа документа"
    TITLE_FORM_FOLDER_CREATE = "Создание папки"  # Страница "Создание папки"
    TITLE_ADD_GROUPS_AD = "Добавление группы AD"  # Окно "Добавление группы AD"
    TITLE_CREATE_FILE_TYPE = "Создание типа файла"  # Окно "Создание типа файла"
    TITLE_CREATE_FIELD_TYPE = "Создание типа метаданных"  # Окно Создание типа метаданных
    TITLE_ACTION_CONFIRMATION = "Подтверждение действий"  # Окно подтверждения
    TITLE_DELETE_CONFIRMATION = "Подтверждение удаления"  # Окно подтверждения
    TITLE_EDITING_FOLDER = "Редактирование папки"  # Страница "Редактирование папки"
    TITLE_CHANGE_HISTORY = "История изменений групп AD"  # Окно "История изменений групп AD"

    # Названия для создания типа документа
    DOCUMENT_TYPE_NAME = "DocTypeAutotest"  # Тип документа
    FILE_TYPE_NAME = "FileTypeAutotest"  # Тип файла
    FILE_EXTENSIONS = ".png"  # Возможные расширения файла
    FIELD_TYPE_NAME = "FiledTypeAutotest"  # Тип поля
    FIELD_TYPE_NAME_DISPLAY = "FiledTypeDisplayAutotest"  # Отображаемый тип поля

    SUCCESS_TYPE_CREATE = "Тип документа успешно создан"
    SUCCESS_TYPE_DELETE = "Тип документа успешно удален"
    SUCCESS_FOLDER_CREATE = "Папка успешно создана"
    SUCCESS_FOLDER_SAVE = "Папка успешно изменена"


class FilterNotice:
    """
    Константы для страницы фильтров
    ***
    """

    TITLE_FILTERS = "Фильтры"  # Заголовок окна фильтров
