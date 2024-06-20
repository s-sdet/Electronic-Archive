import logging
from requests import Response, request
from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class DocumentLink(BaseClass):
    """Класс взаимодействия ссылками между документов."""

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
        assert res.status_code == response
        return res.json()
