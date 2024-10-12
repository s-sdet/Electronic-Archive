import logging
from requests import Response, request

from api.data.constants import DocumentTypeNotice
from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class Document(BaseClass):
    """Класс взаимодействия с документами."""

    doc_type = DocumentTypeNotice()

    API_V0 = "api/v0.1/"  # API v0.1
    API_V1 = "api/v1.0/"  # API v1.0
    API_V2 = "api/v2.0/"  # API v2.0
    API_V3 = "api/v3.0/"  # API v3.0

    URL_API_V0_DOCUMENT = "api/v0.1/Document/"  # API v0.1
    URL_API_V1_DOCUMENT = "api/v1.0/Document/"  # API v1.0
    URL_API_V2_DOCUMENT = "api/v2.0/Document/"  # API v2.0
    URL_API_V3_DOCUMENT = "api/v3.0/Document/"  # API v3.0
    URL_API_V3_DOCUMENT_VERSION_ID = "api/v3.0/DocumentVersion/"  # Версия документа по ID

    CREDIT_DOSSIER = '{"documentEntityType":"CreditDossier", "entityKey":"string"}'  # Для фильтра по '№ заявки АС ОКЗ'

    URL_DOCUMENT_ENTITIES = "?DocumentEntities={}&PageNumber={}&PageSize={}"  # Для фильтрации документов по параметрам

    # Данные для параметризации тестов создания документа с указанием обязательных типов метаданных:
    # 1: name типа документа; 2: metadata_type_name; 3: displayName; 4: type; 5: name документа; 6: metadata_type;
    # 7: metadata_type_value;
    DATA_FOR_CREATE_DOCUMENT_WITH_REQUIRED_METADATA_TYPE = [
        # Создание документа с обязательным типом метаданных Number:
        [doc_type.doc_type_name_latin, "Number", "Номер", "Number", "1", "Number", 1, None, None],
        # Создание документа с обязательным типом метаданных DateTime:
        [doc_type.doc_type_name_latin, "DateTime", "ДатаВремя", "DateTime", "1", "DateTime", "2025-05-20", None, None],
        # Создание документа с обязательным типом метаданных string_1 (регулярное выражение с числами):
        [doc_type.doc_type_name_latin, "string_1", "Строковое регулярное", "String", "1", "string_1", "12 34",
         "regularExpression", "^\\d{2} \\d{2}$"],
        # Создание документа с обязательным типом метаданных String (регулярное выражение почта):
        [doc_type.doc_type_name_latin, "String", "Строковое регулярное", "String", "1", "String", "livespase@akbars.ru",
         "regularExpression", "^[\\S]+@[\\S]+.[\\S]+$"],
        # Создание документа с обязательным типом метаданных Boolean:
        [doc_type.doc_type_name_latin, "Boolean", "Булево", "Boolean", "1", "Boolean", True, None, None]
    ]

    # Данные для параметризации тестов изменения документа с указанием обязательных типов метаданных:
    # 1: name типа документа; 2: Название документа; 3: metadata_type; 4: metadata_type_value;
    DATA_FOR_CREATE_DOCUMENT_WITHOUT_FILE_TYPE_AND_METADATA_TYPE = [
        [doc_type.doc_type_name_latin, "Тестовый документ", None, None],
    ]

    # Данные для параметризации тестов обновления информации документа:
    # 1: name типа документа; 2: Название документа; 3: metadata_type; 4: metadata_type_value; 5: Новое название дока;
    DATA_FOR_UPDATE_DOCUMENT_WITHOUT_FILE_TYPE_AND_METADATA_TYPE = [
        [doc_type.doc_type_name_latin, "Тестовый документ", None, None, "Измененный документ"],
    ]

    # Данные для параметризации тестов обновления данных документа и типов метаданных:
    # 1: name типа документа; 2: Обязательность типа; 3: displayName; 4: type; 5: name документа; 6: metadata_type;
    # 7: metadata_type_value; 8: Новое название документа; 9: Новый тип метаданных; 10: Значение типа метаданных;
    DATA_FOR_CREATE_DOCUMENT_NOT_CONTAINING_METADATA_TYPES = [
        # Обновление данных документа не содержащее типы метаданных:
        [doc_type.doc_type_name_latin, False, "Number", "Номер", "Number", None, None, "Новый документ", None, None,
         "Измененный документ", "Number", 10],
        # Обновление данных документа содержащего типы метаданных:
        [doc_type.doc_type_name_latin, True, "DateTime", "ДатаВремя", "DateTime", None, None, "Новый документ",
         "DateTime", "2023-10-10", "Измененный документ", "DateTime", "2024-03-10"]
    ]

    @staticmethod
    def data_for_creating_document_with_required_metadata_type(doc_type_id: str, name: str = "Тестовый док",
                                                               metadata_type=None, metadata_type_value=None):
        """
        Тело запроса для создания документа с указанием обязательного типа метаданных.
        :param doc_type_id: ID типа документа;
        :param name: Название;
        :param metadata_type: Тип метаданных;
        :param metadata_type_value: Значение типа метаданных;
        """
        data = {
                "documentTypeId": doc_type_id,
                "name": name,
                "documentProperties": {
                    metadata_type: metadata_type_value
                }
            }
        return data

    @staticmethod
    def data_for_creating_document_with_multiple_types(
            doc_type_id: str, name: str, first_metadata_type: str, second_metadata_type: str,
            first_metadata_type_value=None, second_metadata_type_value=None):
        """
        Тело запроса для создания документа с указанием нескольких типов метаданных.
        :param doc_type_id: ID типа документа;
        :param name: Название;
        :param first_metadata_type: Первый тип метаданных;
        :param first_metadata_type_value: Значение первого типа метаданных;
        :param second_metadata_type: Второй тип метаданных;
        :param second_metadata_type_value: Значение второго типа метаданных;
        """
        data = {
                "documentTypeId": doc_type_id,
                "name": name,
                "documentProperties": {
                    first_metadata_type: first_metadata_type_value,
                    second_metadata_type: second_metadata_type_value
                }
            }
        return data

    @staticmethod
    def data_for_update_document_with_multiple_types(
            doc_id: str, name: str, first_metadata_type: str, second_metadata_type: str,
            first_metadata_type_value=None, second_metadata_type_value=None):
        """
        Тело запроса для обновления документа с указанием нескольких типов метаданных.
        :param doc_id: ID документа;
        :param name: Название;
        :param first_metadata_type: Первый тип метаданных;
        :param first_metadata_type_value: Новое значение первого типа метаданных;
        :param second_metadata_type: Второй тип метаданных;
        :param second_metadata_type_value: Новое значение второго типа метаданных;
        """
        data = {
            "documentId": doc_id,
            "name": name,
            "documentProperties": {
                first_metadata_type: first_metadata_type_value,
                second_metadata_type: second_metadata_type_value
            }
        }
        return data

    @staticmethod
    def data_for_updating_document(doc_id: str, name: str, metadata_type: str, metadata_type_value=1):
        """
        Тело запроса для изменения документа.
        :param doc_id: ID документа;
        :param name: Название;
        :param metadata_type: Тип метаданных;
        :param metadata_type_value: Значение типа метаданных;
        """
        data = {
            "documentId": doc_id,
            "name": name,
            "documentProperties": {
                metadata_type: metadata_type_value
            }
        }
        return data

    @staticmethod
    def json_data_for_saving_document(doc_type_id=None):
        """Тело запроса для сохранения документа и версии с указанием дополнительных метаданных."""
        data = {"documentTypeId": doc_type_id,
                "documentProperties":
                    {"Тестовое поле": "Для тестирования дополнительных метаданных"}
                }
        return data

    @staticmethod
    def data_for_create_document_and_its_version_in_test_document_type(doc_type_id=None):
        """Тело запроса для создания документа и его версии в тестовом типе документа CoreTeam."""
        data = {"documentTypeId": doc_type_id,
                "documentProperties": {},
                "expireDate": "2023-08-07T11:00:46.1310000",
                "sourceDate": "2023-08-07T11:00:46.1310000",
                "files": [],
                "okzRequestNumber": "1900",
                "debitCardNumber": "1900",
                "accountNumber": "1900",
                "crmClientId": "1900",
                "applicationId": "1900",
                "absClientId": "1900",
                "absDealId": "1900",
                "absCollateralObjectId": "1900",
                "creditContractNumber": "1900"
                }
        return data

    @staticmethod
    def data_for_creating_document_indicating_file_id(doc_type_id=None, file_id=None):
        """Тело запроса для сохранения документа и его версии с указанием id загруженного в систему файла,
        дополнительных метаданных, дат добавления документа и версии в систему-источник и даты окончания действия."""
        data = {
                "documentTypeId": doc_type_id,
                "documentProperties": {
                    "Boolean": "false",
                    "Date": "2023-09-14T20:00:00.000Z",
                    "DateTime": "2023-10-06T20:00:00.000Z",
                    "Decimal": "30",
                    "Dictionary": "New",
                    "Integer": "123",
                    "String": "Строка",
                    "StringArray": ["1", "2", "3"]
                },
                "expireDate": "2024-12-31T11:11:39.8510000",
                "sourceDate": "2023-08-04T11:11:39.8510000",
                "files": [f"{file_id}"]
            }
        return data

    @staticmethod
    def data_for_creating_document_with_expire_and_source_date(doc_type_id=None, name="Тестовый док", file_id=None):
        """
        Тело запроса для создания документа с передачей ID загруженного файла и указанием начала и окончания документа.
        :param doc_type_id: ID типа документа;
        :param name: Имя документа;
        :param file_id: ID загруженного файла;
        """
        data = {
            "documentTypeId": doc_type_id,
            "name": name,
            "documentProperties": {},
            "expireDate": "2024-12-31T11:11:39.8510000",
            "sourceDate": "2023-08-04T11:11:39.8510000",
            "files": [f"{file_id}"]
        }
        return data

    @staticmethod
    def data_for_creating_document_without_properties_and_files(doc_type_id=None, name="Тестовый док"):
        """
        Тело запроса для создания документа с передачей пустых значений в "documentProperties" и "files".
        :param doc_type_id: ID типа документа;
        :param name: Имя документа;
        """
        data = {
            "documentTypeId": doc_type_id,
            "name": name,
            "documentProperties": {},
            "files": []
        }
        return data

    @staticmethod
    def data_for_creating_document_with_entities(doc_type_id=None, entity_type: str = "DebitCard",
                                                 entity_key: str = "1222"):
        """
        Тело запроса для создания документа с передачей entities.
        :param doc_type_id: ID типа документа;
        :param entity_type: Ключ entities;
        :param entity_key: Значение entities;
        """
        data = {
                "documentTypeId": doc_type_id,
                "documentProperties": {},
                "files": [],
                "entities": [{
                    "documentEntityType": entity_type,
                    "entityKey": entity_key,
                    "properties": {}
                }]
            }
        return data

    @staticmethod
    def for_saving_document_with_date(doc_type_id=None):
        """Тело запроса для сохранения документа и его версии документа с указанием даты окончания действия,
        даты создания версии в системе-источнике, дополнительными метаданными, БЕЗ прикрепления файлов и
        БЕЗ основных 6 полей метаданных."""
        data = {"documentTypeId": doc_type_id,
                "documentProperties":
                    {"Тестовое поле": "Для тестирования дополнительных метаданных"},
                "expireDate": "2023-08-05T08:07:18.4380000",
                "sourceDate": "2023-07-05T08:07:18.4380000",
                "files": [],
                "entities": []
                }
        return data

    @staticmethod
    def json_data_for_creating_document_whit_one_version(doc_type_id=None):
        """Тело запроса для создания документа и его одной версии."""
        data = {"documentTypeId": doc_type_id,
                "documentProperties":
                    {"Дополнительные метаданные": "Метаданные"},
                "expireDate": "2023-07-06T11:12:34.833Z",
                "sourceDate": "2023-07-06T11:12:34.833Z",
                "files": [],
                "entities": [
                    {"documentEntityType": "CreditDossier",
                     "entityKey": "string",
                     "properties": {}
                     }]
                }
        return data

    @staticmethod
    def data_for_creating_document_whit_expire_date(doc_type_id=None, expire_date=None):
        """Тело запроса для создания документа и его версии с датой окончания действия РАНЕЕ текущей даты."""
        data = {"documentTypeId": f"{doc_type_id}",
                "expireDate": f"{expire_date}"
                }
        return data

    @staticmethod
    def data_for_creating_document_whit_source_date(doc_type_id=None, source_date=None):
        """Тело запроса для создания документа и его версии с датой создания в системе-источнике РАНЕЕ текущей даты."""
        data = {"documentTypeId": f"{doc_type_id}",
                "sourceDate": f"{source_date}"
                }
        return data

    @staticmethod
    def data_for_creating_document_and_its_version_with_id_files_in_system(doc_type_id=None, first_file=None,
                                                                           second_file=None, third_file=None):
        """Тело запроса для создания документа и версии с указанием существующих в системе файлов."""
        data = {
                "documentTypeId": f"{doc_type_id}",
                "files": [
                    f"{first_file}",
                    f"{second_file}",
                    f"{third_file}"]
                }
        return data

    def save_document(self, url_api=None, header=None, data=None, response=200) -> Response:
        """
        Сохранение документа.
        :param url_api: URL версии API;
        :param header: Токен авторизации;
        :param data: Тело запроса;
        :param response: Ожидаемый ответ сервера;
        """
        res = request(
            method="POST",
            url=f"{self.app.url}{url_api}",
            headers=header,
            json=data
        )
        logger.info(f"POST: Сохранение документа. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()

    def create_document(self, url_api="api/v4.0/", header=None, data=None, response=200) -> Response:
        """
        Создание документа.
        :param url_api: URL версии API;
        :param header: Токен авторизации;
        :param data: Тело запроса;
        :param response: Ожидаемый ответ сервера;
        """
        res = request(
            method="POST",
            url=f"{self.app.url}{url_api}Document",
            headers=header,
            json=data
        )
        logger.info(f"POST: Создание документа. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()

    def update_document(self, url_api="api/v4.0/", header=None, data=None, status_code=200) -> Response:
        """
        Обновление/изменение документа.
        :param url_api: URL версии API;
        :param header: Токен авторизации;
        :param data: Тело запроса;
        :param status_code: Ожидаемый ответ сервера;
        """
        res = request(
            method="PUT",
            url=f"{self.app.url}{url_api}Document",
            headers=header,
            json=data
        )
        logger.info(f"PUT: Обновление документа. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == status_code
        return res.json()

    def get_documents_by_entities(self, api_version=None, query_string=None, header=None, response=200) -> Response:
        """Получение списка документов с применением фильтра по связанным сущностям."""
        res = request(
            method="GET",
            url=f"{self.app.url}{api_version}Document/{query_string}",
            headers=header
        )
        logger.info(f"GET: Получение документов с применением фильтра. Ответ: {res.status_code}")
        assert res.status_code == response
        return res.json()

    def get_doc_info_by_doc_id(self, api_version="api/v3.0/", doc_id=None, header=None, response=200) -> Response:
        """
        Получение информации о конкретной версии документа по ее id.
        :param api_version: URL версии API;
        :param doc_id: ID документа
        :param header: Токен авторизации;
        :param response: Ожидаемый ответ сервера;
        """
        res = request(
            method="GET",
            url=f"{self.app.url}{api_version}Document/{doc_id}",
            headers=header
        )
        logger.info(f"GET: Получение данных по ID документа. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()

    def get_data_by_document_id(self, url_api=None, doc_id=None, header=None, response=200) -> Response:
        """Получение данных по ID документа или его версии."""
        res = request(
            method="GET",
            url=f"{self.app.url}{url_api}{doc_id}",
            headers=header
        )
        logger.info(f"GET Data by Document ID. Status code: {res.status_code}")
        assert res.status_code == response
        return res.json()

    def get_data_by_document_version_id(self, url_api=None, doc_ver_id=None, header=None, response=200) -> Response:
        """Получение данных по ID версии документа или его версии"""
        res = request(
            method="GET",
            url=f"{self.app.url}{url_api}{doc_ver_id}",
            headers=header
        )
        logger.info(f"GET Data by Document Version ID. Status code: {res.status_code}")
        assert res.status_code == response
        return res.json()

    def get_document_by_version_id(self, url_api="api/v4.0/", ver_id=None, header=None, status_code=200) -> Response:
        """
        Получение данных документа по идентификатору версии.
        :param url_api: URL версии API;
        :param ver_id: ID версии документа
        :param header: Токен авторизации;
        :param status_code: Ожидаемый ответ сервера;
        """
        res = request(
            method="GET",
            url=f"{self.app.url}{url_api}Document/Version/{ver_id}",
            headers=header
        )
        logger.info(f"GET: Получение данных документа по versionID. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == status_code
        return res.json()
