import logging
from requests import Response, request
from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class History(BaseClass):
    """Класс взаимодействия с историей версий документов."""

    def get_history(self, api_ver=None, doc_ver_id=None, header=None, response=200) -> Response:
        """
        Получение истории изменений версии документа по id версии документа.
        :param api_ver: Версия API;
        :param doc_ver_id: ID версии документа;
        :param header: Токен авторизации;
        :param response: Ожидаемый ответ сервера;
        """
        res = request(
            method="GET",
            url=f"{self.app.url}{api_ver}DocumentVersion/{doc_ver_id}/History",
            headers=header
        )
        logger.info(f"GET: Получение истории изменений версии документа. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()
