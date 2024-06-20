import logging
from requests import Response, request
from api.fixtures.base import BaseClass
from api.fixtures.document.document import Document

logger = logging.getLogger("Live Plus. Electronic Archive")


class DocumentVersionSetActual(BaseClass):
    """"""

    API_V0_FILE = "api/v0.1/"  # API v0.1
    API_V1_FILE = "api/v1.0/"  # API v1.0
    API_V2_FILE = "api/v2.0/"  # API v2.0
    API_V3_FILE = "api/v3.0/"  # API v3.0

    # Для параметризации изменения актуальности версий документа, где:
    # 1 - ID версии документа, 2 - версия API, 3 - дата добавления версии, 4 - вычисление хеша, 5 - имя файла.
    DATA_FOR_CHANGING_VERSION_OF_DOCUMENT_ACTUAL = [
        ["api/v0.1/Document/", "api/v0.1/DocumentVersion/", "api/v0.1/"],
        ["api/v1.0/Document/", "api/v1.0/DocumentVersion/", "api/v1.0/"],
        ["api/v2.0/Document/", "api/v2.0/DocumentVersion/", "api/v2.0/"],
        ["api/v3.0/Document/", "api/v3.0/DocumentVersion/", "api/v3.0/"],
    ]

    def set_document_version_actual(self, url_api=None, ver_id=None, set_actual=True, header=None,
                                    response=200) -> Response:
        """
        Установка актуальности версии документа по ее ID.
        :param url_api: URL версии API;
        :param ver_id: ID версии документа;
        :param set_actual: Установить актуальность версии документа;
        :param header: Токен авторизации;
        :param response: Ожидаемый ответ сервера;
        """
        res = request(
            method="PUT",
            url=f"{self.app.url}{url_api}DocumentVersion/{ver_id}/SetActual/{set_actual}",
            headers=header,
        )
        logger.info(f"PUT запрос: установка актуальности версии документа. Ответ: {res.status_code}")
        assert res.status_code == response
        return res.json()
