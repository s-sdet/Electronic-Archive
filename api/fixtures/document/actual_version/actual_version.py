import logging
from requests import Response, request
from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class ActualVersion(BaseClass):
    """Класс взаимодействия с актуальными версиями документов."""

    URL_ACTUAL_VERSION = "api/v3.0/Document/{}/ActualVersion"  # Получения актуальной версии документа

    def get_actual_version(self, header=None, data=None, type_response=200, doc_id=None) -> Response:
        """Получение информации об актуальной версии документа с указанием id документа."""
        res = request(
            method="GET",
            url=f"{self.app.url}{self.URL_ACTUAL_VERSION.format(doc_id)}",
            headers=header,
            json=data
        )
        logger.info(f"GET Actual Version. Status code: {res.status_code}")
        assert res.status_code == type_response
        return res.json()
