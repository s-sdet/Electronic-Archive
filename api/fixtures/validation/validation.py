import logging
from requests import Response, request
from api.fixtures.base import BaseClass
from api.data.constants import DocumentTypeNotice, ValidationNotice, FileNotice, ApiVersions

logger = logging.getLogger("Live Plus. Electronic Archive")


class Validation(BaseClass):
    """Класс взаимодействия с документами."""

    doc_type = DocumentTypeNotice()
    file_type = FileNotice()

    # Данные для параметризации валидации максимальной длинны поля № заявки в "АС ОКЗ" для разных версий API. Где:
    # 1 - ID типа документа; 2 - строка для поля "АС ОКЗ", 3 - URL, 4 - версия API.
    DATA_FOR_CHECKING_FIELD_LENGTH = [
        ["a0f5994a-ecf3-4e3c-b412-dab864d704d4", "12312312412312321321321414123412431412413412412413412412414123423",
         "DocumentVersion", "PUT"],
        ["a0f5994a-ecf3-4e3c-b412-dab864d704d4", "12312312412312321321321414123412431412413412412413412412414123423",
         "DocumentVersion", "POST"],
        ["a0f5994a-ecf3-4e3c-b412-dab864d704d4", "12312312412312321321321414123412431412413412412413412412414123423",
         "Document/Link", "PUT"],
        ["a0f5994a-ecf3-4e3c-b412-dab864d704d4", "12312312412312321321321414123412431412413412412413412412414123423",
         "Document", "POST"],
    ]

    # Валидные данные для проверки длинны названия типа документа.
    VALID_DOCUMENT_TYPE_NAME_LENGTH = [
        [DocumentTypeNotice.NAME_CYRILLIC_AND_SYMBOLS, "DocumentType"],
        [DocumentTypeNotice.NAME_LATIN_AND_SYMBOLS, "DocumentType"],
        [doc_type.doc_type_name_cyrillic, "DocumentType"],
        [doc_type.doc_type_name_latin, "DocumentType"]
    ]

    # Валидные данные для проверки длинны названия для типа файла.
    VALID_FILE_TYPE_NAME_LENGTH = [
        [doc_type.doc_type_name_cyrillic, DocumentTypeNotice.FILE_TYPE_NAME_CYRILLIC, "DocumentType"],
        [doc_type.doc_type_name_latin, DocumentTypeNotice.FILE_TYPE_NAME_LATIN, "DocumentType"]
    ]

    # Валидные данные для проверки возможных расширений файлов.
    VALID_DATA_ALLOWED_EXTENSIONS = [
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, doc_type.FILE_TYPE_NAME_LATIN, ".mp3", "DocumentType"],
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, doc_type.FILE_TYPE_NAME_LATIN, ".pdf", "DocumentType"]
    ]

    # Валидные данные для проверки возможных названий типа файла.
    VALID_DATA_FILE_TYPE_NAME = [
        [ApiVersions.API_V4, doc_type.doc_type_name_cyrillic, file_type.file_type_name_cyrillic, "DocumentType"],
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, file_type.file_type_name_latin, "DocumentType"]
    ]

    # Невалидные данные для проверки поля системное названия типа.
    INVALID_DATA_SYSTEM_TYPE_NAME = [
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, ValidationNotice.SYSTEM_TYPE_NAME["LATIN_LENGTH_65"],
         file_type.file_type_name_latin, "DocumentType", ValidationNotice.ERROR_SYSTEM_TYPE_NAME_MAX_LENGTH],
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, ValidationNotice.SYSTEM_TYPE_NAME["CYRILLIC_LENGTH_23"],
         file_type.file_type_name_latin, "DocumentType", ValidationNotice.ERROR_INVALID_SYSTEM_TYPE_NAME],
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, "", file_type.file_type_name_latin, "DocumentType",
         ValidationNotice.ERROR_SYSTEM_TYPE_NAME_NULL]
    ]

    # Невалидные данные для проверки поля отображаемое название.
    INVALID_DATA_DISPLAY_NAME = [
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, ValidationNotice.DISPLAY_NAME["LATIN_LENGTH_65"],
         file_type.file_type_name_latin, "DocumentType", ValidationNotice.ERROR_DISPLAY_NAME_MAX_LENGTH],
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, ValidationNotice.DISPLAY_NAME["NUMBERS_AND_SYMBOLS"],
         file_type.file_type_name_latin, "DocumentType", ValidationNotice.ERROR_INVALID_DISPLAY_NAME],
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, "",
         file_type.file_type_name_latin, "DocumentType", ValidationNotice.ERROR_INVALID_DISPLAY_NAME]
    ]

    # Невалидные данные для проверки поля Названия типа документа.
    # 1: версия апи; 2: значение названия типа документа; 3: имя типа файла; 4: url, 5: текст ошибки.
    INVALID_DOCUMENT_TYPE_NAME = [
        [ApiVersions.API_V4, ValidationNotice.DOCUMENT_TYPE_NAME["SYMBOLS"],
         file_type.file_type_name_latin, "DocumentType", ValidationNotice.ERROR_INVALID_DOC_TYPE_NAME],
        [ApiVersions.API_V4, ValidationNotice.DOCUMENT_TYPE_NAME["NUMBERS"],
         file_type.file_type_name_latin, "DocumentType", ValidationNotice.ERROR_INVALID_DOC_TYPE_NAME],
        [ApiVersions.API_V4, ValidationNotice.DOCUMENT_TYPE_NAME["LATIN_LENGTH_65"],
         file_type.file_type_name_latin, "DocumentType", ValidationNotice.ERROR_DOC_TYPE_NAME_MAX_LENGTH],
        [ApiVersions.API_V4, "", file_type.file_type_name_latin, "DocumentType",
         ValidationNotice.ERROR_DOC_TYPE_NAME_NULL]
    ]

    # Невалидные данные для проверки поля Название для типа файла.
    # 1: версия апи; 2: название типа документа; 3: значение для имени типа файла; 4: url, 5: текст ошибки.
    INVALID_FILE_TYPE_NAME = [
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, ValidationNotice.FILE_TYPE_NAME["NUMBERS"], "DocumentType",
         ValidationNotice.ERROR_INVALID_FILE_TYPE_NAME],
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, ValidationNotice.FILE_TYPE_NAME["CYRILLIC_LENGTH_65"],
         "DocumentType", ValidationNotice.ERROR_FILE_TYPE_NAME_MAX_LENGTH],
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, "", "DocumentType",
         ValidationNotice.ERROR_FILE_TYPE_NAME_NULL],
    ]

    # Невалидные данные для проверки поля Возможные расширения.
    # 1: версия апи; 2: название типа документа; 3: имя типа файла; 4: возможные расширения; 5: url, 6: текст ошибки.
    INVALID_ALLOWED_EXTENSIONS = [
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, file_type.file_type_name_latin,
         ValidationNotice.EXTENSIONS["SYMBOLS"], "DocumentType", ValidationNotice.ERROR_EXTENSIONS_MAX_LENGTH],
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, file_type.file_type_name_latin,
         ValidationNotice.EXTENSIONS["CYRILLIC"], "DocumentType", ValidationNotice.ERROR_INVALID_EXTENSIONS],
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, file_type.file_type_name_latin,
         ValidationNotice.EXTENSIONS["NUMBERS_LENGTH_65"], "DocumentType", ValidationNotice.ERROR_EXTENSIONS_MAX_LENGTH],
        [ApiVersions.API_V4, doc_type.doc_type_name_latin, file_type.file_type_name_latin,
         ValidationNotice.EXTENSIONS["WITHOUT_SPACES"], "DocumentType", ValidationNotice.ERROR_INVALID_EXTENSIONS]
    ]

    @staticmethod
    def data_credit_dossier(doc_type_id=None, okz_number=None):
        """Тело запроса для передачи данных в поле № заявки в 'АС ОКЗ'."""
        data = {"documentTypeId": f"{doc_type_id}",
                "okzRequestNumber": f"{okz_number}",
                }
        return data

    @staticmethod
    def data_without_document_type_key():
        """Тело запроса для создания документа без передачи ключ-значения документа."""
        data = {}
        return data

    @staticmethod
    def data_without_document_type_value():
        """Тело запроса для создания документа без передачи значения ключа типа документа."""
        data = {
            "documentTypeId": None
        }
        return data

    @staticmethod
    def data_without_document_id_value():
        """Тело запроса для получения информации без передачи значения ключа ID документа."""
        data = {
            "documentId": None
        }
        return data

    @staticmethod
    def creating_document_type(doc_type_name=None, system_type_name="test", display_name="test", file_name=None,
                               extensions=".pdf"):
        """
        Тело запроса для создания типа документа.
        :param doc_type_name: Название типа документа;
        :param system_type_name: Системное название типа;
        :param display_name: Название, которое будет отображаться;
        :param file_name: Системное название файла;
        :param extensions: Расширение файла;
        """
        data = {
            "name": f"{doc_type_name}",
            "properties": [
                {
                    "name": system_type_name,
                    "displayName": display_name,
                    "isRequired": True,
                    "type": "String",
                }
            ],
            "fileTypes": [{
                "name": f"{file_name}",
                "allowedExtensions": [extensions],
                "isRequired": True
            }]
        }
        return data

    @staticmethod
    def update_document_type(doc_type_id=None, doc_type_name=doc_type.doc_type_name_cyrillic,
                             file_type_name="Тестовый файл", extensions=".png"):
        """
        Тело запроса для обновления типа документа.
        :param doc_type_id: ID типа документа;
        :param doc_type_name: Имя типа документа;
        :param file_type_name: Имя файла;
        :param extensions: Расширение файла;
        """
        data = {
                "id": doc_type_id,
                "name": doc_type_name,
                "properties": [],
                "fileTypes": [{
                        "name": file_type_name,
                        "allowedExtensions": [extensions],
                        "isRequired": True,
                    }]
                }
        return data

    def add_data(self, method="POST", url_api=None, url=None, header=None, data=None, response=200) -> Response:
        """
        Добавить данные в документ.
        :param method: Тип запроса;
        :param url_api: URL версии API;
        :param url: URL;
        :param header: Токен авторизации;
        :param data: Тело запроса;
        :param response: Ожидаемый ответ сервера;
        """
        res = request(
            method=f"{method}",
            url=f"{self.app.url}{url_api}{url}",
            headers=header,
            json=data
        )
        logger.info(f"POST: Добавление данных. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()

    def get_info(self, method="GET", url_api=None, url=None, header=None, data=None, response=200) -> Response:
        """
        Получить данные документов.
        :param method: Тип запроса;
        :param url_api: URL версии API;
        :param url: URL;
        :param header: Токен авторизации;
        :param data: Тело запроса;
        :param response: Ожидаемый ответ сервера;
        """
        res = request(
            method=f"{method}",
            url=f"{self.app.url}{url_api}{url}",
            headers=header,
            json=data
        )
        logger.info(f"GET: Получение данных. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()
