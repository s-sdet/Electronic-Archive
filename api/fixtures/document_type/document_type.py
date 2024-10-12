import logging
from requests import Response, request

from api.data.constants import DocumentTypeNotice, FileNotice
from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class DocumentType(BaseClass):
    """Класс взаимодействия с типами документов."""

    doc_type = DocumentTypeNotice()
    file_type = FileNotice()

    URL_DOCUMENT_TYPE = "api/v3.0/DocumentType?SearchPattern={}"  # Получение типа документа

    API_V0 = "api/v0.1/"  # API v0.1
    API_V1 = "api/v1.0/"  # API v1.0
    API_V2 = "api/v2.0/"  # API v2.0
    API_V3 = "api/v3.0/"  # API v3.0

    # Валидные данные для проверки создания типов документа.
    VALID_DATA_FOR_DOC_TYPE = [
        [doc_type.doc_type_name_latin, file_type.file_type_name_latin, "allowedExtensions", []],
        [doc_type.doc_type_name_latin, file_type.file_type_name_latin, "allowedExtensions", None],
        [doc_type.doc_type_name_latin, file_type.file_type_name_latin, None, None]
    ]

    # Невалидные данные для проверки создания типов документа.
    INVALID_DATA_FOR_DOC_TYPE = [
        [doc_type.doc_type_name_latin, file_type.file_type_name_latin, "allowedExtensions", [".pdf", ".jpeg", ".jpeg"]]
    ]

    # Валидные данные для обновления документов с несколькими типами метаданных. Где:
    # 1: name типа документа; 2: название 1-го типа; 3: отображаемое название 1-го типа; 4: тип; 5: название 2-го типа;
    # 6: отображаемое название 2-го типа; 7: второй тип; 8: регулярное выражение; 9: название документа;
    # 10: 1-й тип метаданных; 11: значение 1-го типа; 12: 2-й тип метаданных; 13: значение 2-го типа;
    # 14: новый 1-й тип метаданных; 15: новое значение 1-го типа; 16: новый 2-й тип метаданных; 17: значение 2-го типа;
    DATA_FOR_CREATE_DOCUMENT_TYPE_WITH_TWO_TYPE_METADATA = [
        [file_type.file_type_name_latin, "DateTime", "ДатаВремя", "DateTime", "String", "Строковое регулярное почта",
         "String", "regularExpression", "^[\\S]+@[\\S]+.[\\S]+$", "новый", "DateTime", "2023-10-10", "String",
         "mail@mail.ru", "DateTime", "2024-03-10", "String", "livespece@akbars.ru"],
        [file_type.file_type_name_latin, "Boolean", "Булево", "Boolean", "Number", "Номер", "Number", None, None,
         "новый", "Number", 2024, None, None, "Number", 2024, "Boolean", True]
    ]

    @staticmethod
    def data_to_create_document_type_with_metadata_type(
            doc_type_name=doc_type.doc_type_name_latin, is_required=True, metadata_type_name=None,
            display_name=None, metadata_type=None, regular_expression=None, regular_expression_value=None):
        """
        Тело запроса для создания типа документа без типа файла с указанием обязательного типа метаданных.
        :param doc_type_name: Название типа документа;
        :param is_required: Обязательность типа метаданных;
        :param metadata_type_name: Название типа метаданных;
        :param display_name: Отображаемое название типа метаданных;
        :param metadata_type: Тип метаданных;
        :param regular_expression: Регулярное выражение;
        :param regular_expression_value: Значение регулярного выражения;
        """
        data = {
                "name": doc_type_name,
                "properties": [{
                    "isRequired": is_required,
                    "name": metadata_type_name,
                    "displayName": display_name,
                    "type": metadata_type,
                    regular_expression: regular_expression_value
                }],
                "fileTypes": []
                }
        return data

    @staticmethod
    def doc_type_with_metadata_type_and_without_file_type_in_v3(
            doc_type_name=doc_type.doc_type_name_latin, system_name="String", display_name="String", is_required=False,
            value_type="String"):
        """Тело запроса для создания типа документа с типом метаданных и без типа файла в API v3."""
        data = {
            "name": doc_type_name,
            "properties": [{
                "name": system_name,
                "displayName": display_name,
                "isRequired": is_required,
                "valueType": value_type,
            }],
            "fileTypes": []
        }
        return data

    @staticmethod
    def data_for_create_document_type_without_metadata_type(doc_type_name=doc_type.doc_type_name_latin):
        """
        Тело запроса для создания типа документа без типа файла и типа метаданных.
        :param doc_type_name: Название типа документа;
        """
        data = {
            "name": doc_type_name,
            "properties": [],
            "fileTypes": []
        }
        return data

    @staticmethod
    def data_for_create_document_type_without_property_types(doc_type_name=doc_type.doc_type_name_latin):
        """
        Тело запроса для создания типа документа без типа файла и типа метаданных.
        :param doc_type_name: Название типа документа;
        """
        data = {
            "name": doc_type_name,
            "propertyTypes": [],
            "fileTypes": []
        }
        return data

    @staticmethod
    def data_for_create_document_type_with_metadata(
            doc_type_name=doc_type.doc_type_name_latin, system_file_name=file_type.file_type_name_latin,
            allowed_extensions="allowedExtensions", extensions=None, is_required=False):
        """
        Тело запроса для создания типа документа без типа файла и типа метаданных.
        :param doc_type_name: Название типа документа;
        :param system_file_name: Системное название файла;
        :param allowed_extensions: Доступные расширения для файлов;
        :param extensions: Список доступных расширений для файлов;
        :param is_required: Обязательность типа метаданных;
        """
        data = {
                "name": doc_type_name,
                "properties": [],
                "fileTypes": [{
                    "name": system_file_name,
                    allowed_extensions: extensions,
                    "isRequired": is_required
                }]
            }
        return data

    @staticmethod
    def document_type_without_metadata_and_with_file_type(
            doc_type_name=doc_type.doc_type_name_latin, system_file_name=file_type.file_type_name_latin,
            allowed_extensions="allowedExtensions", extensions='[".jpg", ".pdf", ".png"]', is_required=False):
        """
        Тело запроса для создания типа документа без типа файла и типа метаданных.
        :param doc_type_name: Название типа документа;
        :param system_file_name: Системное название файла;
        :param allowed_extensions: Доступные расширения для файлов;
        :param extensions: Список доступных расширений для файлов;
        :param is_required: Обязательность типа метаданных;
        """
        data = {
            "name": doc_type_name,
            "propertyTypes": [],
            "fileTypes": [{
                "name": system_file_name,
                allowed_extensions: extensions,
                "isRequired": is_required
            }]
        }
        return data

    @staticmethod
    def data_for_create_document_type_with_two_type_metadata(
            doc_type_name=None, name_first_system_file=None, display_name_first_system_file=None, first_file_type=None,
            name_second_system_file=None, display_name_second_system_file=None, second_file_type=None,
            regular_expression=None, expression=None):
        """
        Тело запроса для создания типа документа содержащего два типа метаданных.
        :param doc_type_name: Название типа документа;
        :param name_first_system_file: Системное название первого файла;
        :param display_name_first_system_file: Отображаемое название первого системного файла;
        :param first_file_type: Первый тип файла;
        :param name_second_system_file: Системное название второго файла;
        :param display_name_second_system_file: : Отображаемое название второго системного файла;
        :param second_file_type: Второй тип файла;
        :param regular_expression: Регулярное выражение;
        :param expression: Значение регулярного выражения;
        """
        data = {
                "name": doc_type_name,
                "properties": [
                    {
                        "isRequired": False,
                        "name": name_first_system_file,
                        "displayName": display_name_first_system_file,
                        "type": first_file_type
                    },
                    {
                        "isRequired": False,
                        "name": name_second_system_file,
                        "displayName": display_name_second_system_file,
                        "type": second_file_type,
                        regular_expression: expression
                    }
                ],
                "fileTypes": []
            }
        return data

    def search_doc_type_by_name(self, header=None, key=None, code_response=200) -> Response:
        """Поиск типов документов по названию или нескольким символам."""
        res = request(
            method="GET",
            url=f"{self.app.url}{self.URL_DOCUMENT_TYPE.format(key)}",
            headers=header
        )
        logger.info(f"GET: Поиск типа документа по названию. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == code_response
        return res.json()

    def get_info(self, url_api=None, url=None, folder_id=None, header=None, response=200) -> Response:
        """
        Получить данные.
        :param url_api: URL версии API;
        :param url: URL;
        :param folder_id: ID искомой сущности (документа, папки, типа документа);
        :param header: Токен авторизации;
        :param response: Ожидаемый ответ сервера;
        """
        res = request(
            method="GET",
            url=f"{self.app.url}{url_api}{url}{folder_id}",
            headers=header
        )
        logger.info(f"GET: Получение данных. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()

    def create_doc_type(self, url_api="api/v4.0/", url="DocumentType", header=None, data=None,
                        response=200) -> Response:
        """
        Создать тип документа.
        :param url_api: URL версии API;
        :param url: URL;
        :param header: Токен авторизации;
        :param data: Тело запроса;
        :param response: Ожидаемый ответ сервера;
        """
        res = request(
            method="POST",
            url=f"{self.app.url}{url_api}{url}",
            headers=header,
            json=data
        )
        logger.info(f"POST: Создание типа документа. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()

    def del_doc_type(self, url_api="api/v4.0/", url="DocumentType", type_id=None, header=None, data=None,
                     response=200) -> Response:
        """
        Удалить тип документа.
        :param url_api: URL версии API;
        :param url: URL;
        :param type_id: ID типа документа;
        :param header: Токен авторизации;
        :param data: Тело запроса;
        :param response: Ожидаемый ответ сервера;
        """
        res = request(
            method="DELETE",
            url=f"{self.app.url}{url_api}{url}/{type_id}",
            headers=header,
            json=data
        )
        logger.info(f"POST: Удаление типа документа. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()

    def get_file_type_id(self, url_api="api/v4.0/", url="DocumentType/", doc_type_id=None, header=None,
                         code_response=200) -> Response:
        """Получение ID типа файла по ID типа документа."""
        res = request(
            method="GET",
            url=f"{self.app.url}{url_api}{url}{doc_type_id}",
            headers=header
        )
        logger.info(f"GET: Получение типа документа. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == code_response
        return res.json()

    def update_data(self, url_api=None, url="DocumentType", header=None, data=None, response=200) -> Response:
        """
        Обновить данные типа документа.
        :param url_api: URL версии API;
        :param url: URL;
        :param header: Токен авторизации;
        :param data: Тело запроса;
        :param response: Ожидаемый ответ сервера;
        """
        res = request(
            method="PUT",
            url=f"{self.app.url}{url_api}{url}",
            headers=header,
            json=data
        )
        logger.info(f"PUT: Обновление данных типа документа. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()
