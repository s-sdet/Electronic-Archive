import logging
from requests import Response, request, JSONDecodeError
from requests.structures import CaseInsensitiveDict

from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class GraphicSign(BaseClass):
    """Класс взаимодействия с графическими подписями."""

    @staticmethod
    def data_for_add_graphic_sign(sign: str = "GraphicSign"):
        """
        Тело запроса для передачи строковых объектов, содержащих текст, который должен быть на штампе.
        """
        data = {
            "signParam": f"{sign}",
        }
        return data

    def add_graphic_sign(self, url_api="api/v3.0/", header=None, data=None, specific_files=None, quantity_files=1,
                         status_code=200) -> CaseInsensitiveDict[str]:
        """
        Метод проставления штампа на документ.
        :param status_code: Ожидаемый ответ;
        :param url_api: Версия API;
        :param specific_files: Список конкретных файлов для загрузки или строка с именем файла;
        :param quantity_files: Кол-во прикрепляемых файлов;
        :param data: Тело POST запроса;
        :param header: Токен авторизации;
        """
        res = request(
            method="POST",
            url=f"{self.app.url}{url_api}GraphicSign",
            headers=header,
            data=data,
            files=self.app.file.open_file(key="file", specific_files=specific_files, quantity_files=quantity_files)
        )
        try:
            logger.info(f"POST: Проставления штампа. Ответ: {res.status_code}")
            logger.info(f"HEADERS: {res.headers}")
            assert res.status_code == status_code
            return res.headers
        except JSONDecodeError:
            assert res.status_code == status_code

    def invalid_add_graphic_sign(self, url_api="api/v3.0/", header=None, data=None, specific_files=None,
                                 quantity_files=1, status_code=200) -> Response:
        """
        Метод невалидного проставления штампа на документ.
        :param status_code: Ожидаемый ответ;
        :param url_api: Версия API;
        :param specific_files: Список конкретных файлов для загрузки или строка с именем файла;
        :param quantity_files: Кол-во прикрепляемых файлов;
        :param data: Тело POST запроса;
        :param header: Токен авторизации;
        """
        res = request(
            method="POST",
            url=f"{self.app.url}{url_api}GraphicSign",
            headers=header,
            data=data,
            files=self.app.file.open_file(key="file", specific_files=specific_files, quantity_files=quantity_files)
        )
        try:
            logger.info(f"POST: Проставления штампа. Ответ: {res.status_code}")
            logger.info(f"JSON: {res.json()}")
            assert res.status_code == status_code
            return res.json()
        except JSONDecodeError:
            assert res.status_code == status_code
