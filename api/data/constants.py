"""Константы, в т.ч. тексты ошибок и уведомлений."""
import random


class ApiVersions:
    """Версии API."""
    API_V0 = "api/v0.1/"  # API v0.1
    API_V1 = "api/v1.0/"  # API v1.0
    API_V2 = "api/v2.0/"  # API v2.0
    API_V3 = "api/v3.0/"  # API v3.0
    API_V4 = "api/v4.0/"  # API v4.0


class ValidationNotice:
    """Константы, тексты ошибок при валидации полей."""
    ERROR = "Переданы некорректные параметры запроса"  # Ошибка при передаче невалидных значений в поле
    ERROR_DOC_TYPE = "Отсутствует идентификатор типа документа"  # Ошибка при отсутствии типа документа в теле запроса
    ERROR_DOC_ID = "Отсутствуют идентификаторы документов"  # Ошибка при отсутствии ID документа в теле запроса
    ERROR_INVALID_SYSTEM_TYPE_NAME = ("В имени свойства документа можно использовать только латиницу, цифры и "
                                      "спецсимволы: пробел, запятая, точка,-, _, @,(,),; Использование только символов "
                                      "или цифр не допустимо")
    ERROR_SYSTEM_TYPE_NAME_MAX_LENGTH = "Имя свойства документа не должно быть больше 64 знаков"
    ERROR_SYSTEM_TYPE_NAME_NULL = "Не задано имя свойства документа"
    ERROR_DISPLAY_NAME_MAX_LENGTH = "Отображаемое имя свойства документа не должно быть больше 64 знаков"
    ERROR_INVALID_DISPLAY_NAME = ("В отображаемом имени свойства документа можно использовать только латиницу или "
                                  "кириллицу, цифры и спецсимволы: пробел, запятая, точка,/,-, _, @,(,),; Использование"
                                  " только символов или цифр не допустимо")
    ERROR_DISPLAY_NAME_NULL = "Не задано имя свойства документа"

    ERROR_INVALID_DOC_TYPE_NAME = ("В имени типа документа можно использовать только латиницу или кириллицу, цифры и "
                                   "спецсимволы: пробел, запятая, точка,/,-, _, @,(,),;. Использование только символов"
                                   " или цифр не допустимо")
    ERROR_DOC_TYPE_NAME_MAX_LENGTH = "Имя типа документа не должно быть больше 64 знаков"
    ERROR_DOC_TYPE_NAME_NULL = "Не задано название типа документа"

    ERROR_INVALID_FILE_TYPE_NAME = ("В имени типа файла можно использовать только латиницу кириллицу пробел цифры и /. "
                                    "Использование только цифр не допустимо")
    ERROR_FILE_TYPE_NAME_MAX_LENGTH = "Имя типа файла не должно быть больше 64 знаков"
    ERROR_FILE_TYPE_NAME_NULL = "Не задано название типа файла документа"

    ERROR_EXTENSIONS_MAX_LENGTH = "Расширение файла может содержать не более 10 символов"
    ERROR_INVALID_EXTENSIONS = ("Расширение файла должно начинаться с точки. В расширении файла можно использовать "
                                "только латиницу и цифры")
    ERROR_EXTENSIONS_DUPLICATED = "Расширения не должны дублироваться"

    ERROR_DOC_NAME_NULL = "Не задано имя документа"
    ERROR_DOC_NAME_MAX_LENGTH = "Имя документа не должно быть больше 64 знаков"

    # Данные для валидации поля "Системное название типа"
    SYSTEM_TYPE_NAME = {
        "LATIN_LENGTH_65": "System Type Name System Type Name System Type Name System Type Na",
        "CYRILLIC_LENGTH_23": "Системное название типа"
    }

    # Данные для валидации поля "Отображаемое название"
    DISPLAY_NAME = {
        "LATIN_LENGTH_65": "Display Name Display Name Display Name Display Name Display NameD",
        "NUMBERS_AND_SYMBOLS": "123~@#$"
    }

    # Данные для валидации поля "Название типа документа"
    DOCUMENT_TYPE_NAME = {
        "SYMBOLS": "-,_,@,(,),#,;.",
        "NUMBERS": "123456789",
        "LATIN_LENGTH_65": "Document Type Name Document Type Name Document Type Name Document"
    }

    # Данные для валидации поля "Название для типа файла"
    FILE_TYPE_NAME = {
        "NUMBERS": "123456789",
        "CYRILLIC_LENGTH_65": "Название для типа документа Название для типа документа Названиее"
    }

    # Данные для валидации поля "Возможные расширения"
    EXTENSIONS = {
        "SYMBOLS": "-,_,@,(,),#,;.-,_,@,(,),#,;.-,_,@,(,),#,;.-,_,@,(,),#,;.-,_,@,(,)",
        "CYRILLIC": "пдф",
        "NUMBERS_LENGTH_65": '"123456", "123456", "123456", "123456", "12345", "12345", "12345"',
        "WITHOUT_SPACES": "pdfjpegpng",
        "REPETITIVE": "",
    }


class DocumentTypeNotice:
    """Константы для версий документов."""
    DOC_TYPE_ID = "68d0dc25-9c83-3730-07a4-64f843995846"  # ID типа документа
    SOURCE_DATE = "2023-04-01T20:15:52.5170000"  # Дата создания типа документа
    EXPIRE_DATE = "2023-04-01T20:15:52.5170000"  # Да окончания срока действия типа документа
    NAME_CYRILLIC = f"Тип документа {random.randint(1, 1000000)}"  # < 64 букв кириллицы
    NAME_LATIN = f"Document type {random.randint(1, 1000000)}"  # < 64 букв латиницы
    NAME_CYRILLIC_AND_SYMBOLS = f"Тип документа - {random.randint(1, 1000000)}"  # < 64 букв кириллицы+спецсимволы
    NAME_LATIN_AND_SYMBOLS = f"Document type - {random.randint(1, 1000000)}"  # < 64 букв латиницы+спецсимволы
    FILE_TYPE_NAME_CYRILLIC = f"Файл"  # Название типа файла кириллица < 64
    FILE_TYPE_NAME_LATIN = f"File"  # Название типа файла латиница < 64

    @property
    def doc_type_name_latin(self):
        """Метод генерации имени типа документа на латинице без спецсимволов для тестов валидации полей."""
        name = f"Document type {random.randint(1, 1000000000)}"
        return name

    @property
    def doc_type_name_cyrillic(self):
        """Метод генерации имени типа документа на кириллице без спецсимволов для тестов валидации полей."""
        name = f"Тип документа {random.randint(1, 1000000000)}"
        return name


class DocumentNotice:
    """Константы для документов."""
    DOC_TYPE_ID = "68d0dc25-9c83-3730-07a4-64f843995846"  # ID типа документа
    DOC_ID = "e77654ef-c938-01f3-b8ac-5711f53f6cf9"  # ID документа с разными версиями и прикрепленными файлами
    DOC_ID_V4 = "7f64d4e6-b395-08cb-b34c-c69182ca342a"  # ID документа в API v4
    LINKED_DOC_ID = "81f71402-b2f3-e20d-d68a-f2bc9f400cc2"  # ID дочернего документа связанного с родителем
    FIRST_FILE = "727681fd-568c-93d8-d573-116cee3f8a1c"  # ID первого файла в системе
    SECOND_FILE = "82c5b1e3-6113-8f8e-2964-611ee1086132"  # ID второго файла в системе
    THIRD_FILE = "e200d429-59d0-80cf-5db2-28547b21482d"  # ID третьего файла в системе


class DocumentVersionNotice:
    """Константы для версий документов."""
    DOC_TYPE_ID = "68d0dc25-9c83-3730-07a4-64f843995846"  # ID типа документа
    DOC_ID_WITH_MULTIPLE_VERSIONS = "a0f5994a-ecf3-4e3c-b412-dab864d704d4"  # ID документа с несколькими версиями
    DATE_VALUE = "2023-03-01"  # Значение Value для фильтра


class FileNotice:
    """Константы для загрузки файлов."""

    @property
    def file_type_name_latin(self):
        """Метод генерации имени типа файла на кириллице без спецсимволов для тестов валидации полей."""
        name = f"File type {random.randint(1, 1000000000)}"
        return name

    @property
    def file_type_name_cyrillic(self):
        """Метод генерации имени типа файла на кириллице без спецсимволов для тестов валидации полей."""
        name = f"Тип файла {random.randint(1, 1000000000)}"
        return name

    URL_FILE = "File"  # URL для загрузки файлов;
    URL_LARGE_FILE = "File/Large"  # URL для загрузки больших файлов;
    INVALID_FILE_TYPE_ID = "0f3e1ff6-aac4-5773-8eed-426dfbccb000"  # Несуществующий тип файла
    INVALID_DOCUMENT_TYPE_ID = "0f3e1ff6-aac4-5773-8eed-426dfbccb000"  # Несуществующий тип документа
    INVALID_DOCUMENT_ID = "1234"  # Невалидный ID документа
    ERROR_FILE_TYPE_ID = "Не найдены типы файлов с идентификаторами: {}."  # Текст ошибки невалидного типа файла
    ERROR_DOC_TYPE_ID = "Не найдены типы документов с идентификаторами: {}."  # Текст ошибки невалидного типа документа
    ERROR_DOCUMENT_ID = "The value '{}' is not valid for DocumentId."  # Текст ошибки невалидного ID документа
    ERROR_FILE_NOT_UPLOAD = "Не приложены файлы"  # Текст ошибки при незагруженном файле
