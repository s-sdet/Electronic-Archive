import logging
from requests import Response, request

from api.data.constants import DocumentTypeNotice
from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class Filter(BaseClass):
    """Класс взаимодействия с фильтрацией и поиска документов."""

    doc_type = DocumentTypeNotice()

    # Данные для параметризации тестов обновления данных документа и типов метаданных:
    # 1: name типа документа; 2: название; 3: отображаемое название; 4: тип; 5: название; 6: отображаемое название;
    # 7: тип; 8: название документа; 9: первый тип метаданных; 10: значение метаданных; 11: второй тип метаданных;
    # 12: значение метаданных
    DATA_FOR_DOCUMENT_TYPE_WITHOUT_FILE_TYPE_WITH_METADATA_TYPE = [
        # Обновление данных документа не содержащее типы метаданных:
        [doc_type.doc_type_name_latin, "Number", "Номер", "Number", "DateTime", "ДатаВремя", "DateTime", None, None,
         "Тестовый документ", "Number", 12000, "DateTime", "2023-10-20T00:00:00"]]

    # Данные для параметризации тестов поиска документа по значениям в свойствах документа "valuePropertySearchText":
    # 1: name типа документа; 2: обязательность типа; 3: тип; 4: отображаемое название; 5: значение метаданных;
    DATA_FOR__SEARCH_DOCUMENT_BY_VALUE_PROPERTY_SEARCH_TEXT = [
        # Обновление данных документа не содержащее типы метаданных:
        [doc_type.doc_type_name_latin, False, "String", "Строка", "123456", 200],
        [doc_type.doc_type_name_latin, False, "Number", "Номер", 10, 200],
        [doc_type.doc_type_name_latin, False, "String", "Строка", "000000", 200]]

    @staticmethod
    def data_for_search_doc_by_filter(doc_type_ids: str, properties_type: str = "String",
                                      properties_value: str = "string"):
        """
        Тело запроса для поиска документа по фильтру.
        :param doc_type_ids: ID типа документа str;
        :param properties_type: Тип метаданных;
        :param properties_value: Значение типа метаданных;
        """
        data = {
            "documentTypeIds": [doc_type_ids],
            "properties": {
                properties_type: properties_value
            }
        }
        return data

    @staticmethod
    def data_for_search_doc__by_modification_date(
            date_from: str = "2024-01-01", date_to=None, order_by: str = "AggregateModifiedOn", is_ascending=True,
            page_number: int = 1, page_size: int = 20):
        """
        Тело запроса для поиска документа по фильтру.
        :param date_from: Дата изменения ОТ;
        :param date_to: Дата изменения ДО;
        :param order_by: Поле сортировки. Можно указать имя свойства документа или атрибуты документа;
        :param is_ascending: Если True - сортировка от А до Я, если False - в обратном порядке;
        :param page_number: Номер страницы;
        :param page_size: Размер страницы;
        """
        data = {
                "documentTypeIds": [],
                "properties": {},
                "modifiedDateFrom": date_from,
                "modifiedDateTo": date_to,
                "orderBy": order_by,
                "isAscending": is_ascending,
                "pageNumber": page_number,
                "pageSize": page_size
            }
        return data

    @staticmethod
    def data_for_search_doc_by_value_property(
            doc_type_ids: str, doc_properties: str = "valuePropertySearchText", doc_properties_value: str = "123456",
            page_number: int = 1, page_size: int = 20):
        """
        Тело запроса для поиска документа по фильтру.
        :param doc_type_ids: ID типа документа str;
        :param doc_properties: Свойство документа;
        :param doc_properties_value: Значение свойства документа;
        :param page_number: Номер страницы;
        :param page_size: Размер страницы;
        """
        data = {
                "documentTypeIds": [doc_type_ids],
                "properties": {},
                doc_properties: doc_properties_value,
                "pageNumber": page_number,
                "pageSize": page_size
            }
        return data

    @staticmethod
    def data_for_search_doc_by_properties_filter(
            doc_type_ids: str, properties_type: str = "debitCardNumber", properties_value: str = "1221",
            page_number: int = 1, page_size: int = 20):
        """
        Тело запроса для поиска документа по фильтру.
        :param doc_type_ids: ID типа документа str;
        :param properties_type: Тип метаданных;
        :param properties_value: Значение типа метаданных;
        :param page_number: Номер страницы;
        :param page_size: Размер страницы;
        """
        data = {
                "documentTypeIds": [doc_type_ids],
                "properties": {},
                "globalPropertiesFilter": {
                    properties_type: properties_value
                },
                "pageNumber": page_number,
                "pageSize": page_size
            }
        return data

    @staticmethod
    def data_for_search_doc_without_doc_type(properties_type: str = "okzRequestNumber", properties_value: str = "1222",
                                             page_number: int = 1, page_size: int = 20):
        """
        Тело запроса для поиска документа по фильтру без передачи documentTypeIds.
        :param properties_type: Тип метаданных;
        :param properties_value: Значение типа метаданных;
        :param page_number: Номер страницы;
        :param page_size: Размер страницы;
        """
        data = {
            "documentTypeIds": [],
            "properties": {},
            "globalPropertiesFilter": {
                properties_type: properties_value
            },
            "pageNumber": page_number,
            "pageSize": page_size
        }
        return data

    @staticmethod
    def data_for_search_doc_by_two_properties(
            doc_type_ids: str, first_property_type: str = "Number", first_value: str = "12000",
            second_property_type: str = "DateTime", second_value: str = "2023-10-20T00:00:00"):
        """
        Тело запроса для поиска документа по фильтру.
        :param doc_type_ids: ID типа документа str;
        :param first_property_type: Тип метаданных;
        :param first_value: Значение типа метаданных;
        :param second_property_type: Тип метаданных;
        :param second_value: Значение типа метаданных;
        """
        data = {
            "documentTypeIds": [doc_type_ids],
            "properties": {
                first_property_type: first_value,
                second_property_type: second_value
            }
        }
        return data

    @staticmethod
    def data_for_search_doc_by_two_doc_type_id(
            first_doc_type: str, second_doc_type: str, properties_type: str = "String",
            properties_value: str = "string", page_number: int = 1, page_size: int = 20):
        """
        Тело запроса для поиска документа по фильтру.
        :param first_doc_type: ID первого типа документа str;
        :param second_doc_type: ID второго типа документа str;
        :param properties_type: Тип метаданных;
        :param properties_value: Значение типа метаданных;
        :param page_number: Номер страницы;
        :param page_size: Размер страницы;
        """
        data = {
            "documentTypeIds": [first_doc_type, second_doc_type],
            "properties": {
                properties_type: properties_value
            },
            "pageNumber": page_number,
            "pageSize": page_size
        }
        return data

    @staticmethod
    def data_for_search_doc_by_filter_page_number(doc_type_ids: str, page_number: int = 1, page_size: int = 20):
        """
        Тело запроса для поиска документа по фильтру.
        :param doc_type_ids: ID типа документа str;
        :param page_number: Номер страницы;
        :param page_size: Размер страницы;
        """
        data = {
            "documentTypeIds": [doc_type_ids],
            "properties": {},
            "pageNumber": page_number,
            "pageSize": page_size
        }
        return data

    def find_document(self, url_api="api/v4.0/", header=None, data=None, status_code=200) -> Response:
        """
        Поиск документов по фильтрам.
        :param url_api: URL версии API;
        :param header: Токен авторизации;
        :param data: Тело запроса;
        :param status_code: Ожидаемый ответ сервера;
        """
        res = request(
            method="POST",
            url=f"{self.app.url}{url_api}Document/Filter/FindDocuments",
            headers=header,
            json=data
        )
        logger.info(f"POST: Поиск документа. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == status_code
        return res.json()
