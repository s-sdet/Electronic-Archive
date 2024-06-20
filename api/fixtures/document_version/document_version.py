import logging
from requests import Response, request
from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class DocumentVersion(BaseClass):
    """Класс взаимодействия с версиями документов."""

    API_V0 = "api/v0.1/"  # API v0.1
    API_V1 = "api/v1.0/"  # API v1.0
    API_V2 = "api/v2.0/"  # API v2.0
    API_V3 = "api/v3.0/"  # API v3.0
    URL_API_V0_DOCUMENT_VERSION = "api/v0.1/DocumentVersion/"  # Для создания версии документа. API v0.1
    URL_API_V1_DOCUMENT_VERSION = "api/v1.0/DocumentVersion/"  # Для создания версии документа. API v1.0
    URL_API_V2_DOCUMENT_VERSION = "api/v2.0/DocumentVersion/"  # Для создания версии документа. API v2.0
    URL_API_V3_DOCUMENT_VERSION = "api/v3.0/DocumentVersion/"  # Для создания версии документа. API v3.0
    URL_FILTER_FOR_GET_DOCUMENT_VERSION_BY_TYPE_ID = \
        "?DocumentTypeId=68d0dc25-9c83-3730-07a4-64f843995846&PageNumber=1&PageSize={}"
    URL_FILTER_FOR_GET_DOCUMENT_VERSION_BY_TYPE = \
        "?DocumentVersion?OkzRequestNumber=1900&DebitCardNumber=1900&AccountNumber=1900&CrmClientId=1900&ApplicationId=1900&PageNumber=1&PageSize={}"

    FILTER_MODIFIED_DATE_FROM = '?Filters=%7B"documentTypeId": "{}","filters": []%7D&ModifiedDateFrom={}'
    FILTER_FIELD_NAME = ('?Filters=%7B"documentTypeId": "{}","filters": [%7B"fieldName": "expireDate", '
                         '"Operation": "DateLaterThan", "Value": "{}"%7D]%7D')

    @staticmethod
    def for_creating_minor_version(doc_id=None):
        """Тело запроса для создания дополнительной версии для уже созданного документа."""
        data = {"documentId": f"{doc_id}",
                "documentProperties":
                    {"Дополнительные метаданные": "Метаданные для версии 2"},
                "expireDate": "2023-07-06T11:48:58.7510000",
                "sourceDate": "2023-07-06T11:48:58.7510000",
                "files": [],
                "entities": [
                    {"documentEntityType": "CreditDossier",
                     "entityKey": "string",
                     "properties": {}
                     }
                            ]
                }
        return data

    @staticmethod
    def data_for_creating_version_in_created_document(doc_id=None):
        """Тело запроса для создания еще 1 версии в уже созданном документе"""
        data = {"documentId": f"{doc_id}",
                "documentProperties": {},
                "expireDate": "2023-08-07T09:18:17.4770000",
                "sourceDate": "2023-08-07T09:18:17.4770000",
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

    def create_document_version(self, url_api=None, header=None, data=None, response=200) -> Response:
        """Создание дополнительной версии уже созданного документа."""
        res = request(
            method="POST",
            url=f"{self.app.url}{url_api}",
            headers=header,
            json=data
        )
        logger.info(f"POST запрос на создание версии документа. Ответ: {res.status_code}")
        assert res.status_code == response
        return res.json()

    def get_info_about_document_version(self, api_version=None, doc_ver_id=None, header=None, response=200) -> Response:
        """Получение информации о конкретной версии документа по ее id."""
        res = request(
            method="GET",
            url=f"{self.app.url}{api_version}DocumentVersion/{doc_ver_id}",
            headers=header
        )
        logger.info(f"GET: Получение данных по ID версии документа. Ответ: {res.status_code}")
        assert res.status_code == response
        return res.json()

    def get_document_versions(self, api_version=None, query_string=None, header=None, response=200) -> Response:
        """Получение версий документа по фильтру DocumentTypeId."""
        res = request(
            method="GET",
            url=f"{self.app.url}{api_version}DocumentVersion/{query_string}",
            headers=header
        )
        logger.info(f"GET document versions by document type ID. Status code: {res.status_code}")
        assert res.status_code == response
        return res.json()
