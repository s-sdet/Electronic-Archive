import logging
from requests import Response, request
from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class SetActual(BaseClass):
    """Класс установки актуальности файлов версий документов."""

    API_V0_FILE = "api/v0.1/"  # API v0.1
    API_V1_FILE = "api/v1.0/"  # API v1.0
    API_V2_FILE = "api/v2.0/"  # API v2.0
    API_V3_FILE = "api/v3.0/"  # API v3.0

    def make_file_current(self, api_version=None, file_id=None, is_actual=True, header=None, response=200) -> Response:
        """Установка актуальности файла нужной версии документа."""
        res = request(
            method="PUT",
            url=f"{self.app.url}{api_version}File/{file_id}/SetActual/{is_actual}",
            headers=header
        )
        logger.info(f"PUT: Установка актуальности файла. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()
