import logging
from requests import Response, request
from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class DocumentLink(BaseClass):
    """Класс взаимодействия ссылками между документов."""

    @staticmethod
    def data_for_document_linking(parent_doc_id=None, child_doc_ids=None):
        """
        Тело запроса для создания связи между документами.
        :param parent_doc_id: ID первого документа;
        :param child_doc_ids: ID второго документа;
        """
        data = {
                "parentDocumentId": parent_doc_id,
                "childDocumentIds": [child_doc_ids]
            }
        return data

    def get_linked_documents_by_id(self, api_version=None, doc_id=None, header=None, response=200) -> Response:
        """
        Получение связанных документов по id документа.
        :param api_version: URL версии API;
        :param doc_id: ID документа
        :param header: Токен авторизации;
        :param response: Ожидаемый ответ сервера;
        """
        res = request(
            method="GET",
            url=f"{self.app.url}{api_version}DocumentLink/LinkedDocuments/{doc_id}",
            headers=header
        )
        logger.info(f"GET: Получение связанных документов. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()

    def document_linking(self, url_api: str = "api/v4.0/", status_code: int = 200, header=None, data=None) -> Response:
        """
        Создание связи между документами.
        :param url_api: URL версии API;
        :param status_code: Ожидаемый ответ сервера;
        :param header: Токен авторизации;
        :param data: Тело запроса;
        """
        res = request(
            method="POST",
            url=f"{self.app.url}{url_api}DocumentLink",
            headers=header,
            json=data
        )
        logger.info(f"POST: Создание связи между документами. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == status_code
        return res.json()
