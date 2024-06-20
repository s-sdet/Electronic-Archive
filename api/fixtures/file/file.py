import os
import logging
import itertools

from pathlib import Path
from requests import Response, request
from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class File(BaseClass):
    """Класс взаимодействия с файлами документов."""

    API_V0_FILE = "api/v0.1/"  # API v0.1
    API_V1_FILE = "api/v1.0/"  # API v1.0
    API_V2_FILE = "api/v2.0/"  # API v2.0
    API_V3_FILE = "api/v3.0/"  # API v3.0

    # Для параметризации загрузки двух файлов, где:
    # 1 - ID версии документа, 2 - версия API, 3 - дата добавления версии, 4 - вычисление хеша.
    DATA_FOR_UPLOADING_TWO_FILES = [
        ["d3f88d67-0fe8-30c4-1e8c-79eb95211eb6", "api/v0.1/", "2023-08-09T20:00:00.000Z", True],
        ["d3f88d67-0fe8-30c4-1e8c-79eb95211eb6", "api/v1.0/", "2023-08-09T20:00:00.000Z", True],
        ["d3f88d67-0fe8-30c4-1e8c-79eb95211eb6", "api/v2.0/", "2023-08-09T20:00:00.000Z", True],
        ["d3f88d67-0fe8-30c4-1e8c-79eb95211eb6", "api/v3.0/", "2023-08-09T20:00:00.000Z", True],
    ]

    @staticmethod
    def open_file(quantity_files=None):
        """
        Метод открытия файла с добавлением в массив для дальнейшего прикрепления к документу.
        :param quantity_files: Ожидаемое кол-во файлов;
        """
        files = []
        for file_name in itertools.islice(os.listdir(Path(os.getcwd(), "files")), quantity_files):
            file = open(Path(os.getcwd(), "files", file_name), "rb")
            files.append(('files', (file_name, file)))
        return files

    @staticmethod
    def data_for_file_upload(file_type_id=None, calculate_hash=None, doc_type_id=None, doc_id=None):
        """
        Универсальное тело запроса для загрузки файлов
        :param file_type_id:
        :param calculate_hash:
        :param doc_type_id:
        :param doc_id:
        """
        data = {
                "FileTypeId": file_type_id,
                "CalculateHash": calculate_hash,
                "DocumentTypeId": doc_type_id,
                "DocumentId": doc_id
        }
        return data

    @staticmethod
    def data_upload_file_with_calculate_hash_and_document_typeid(calculate_hash=None, doc_type_id=None):
        """
        Тело запроса для загрузки файла с указанием ID типа документа и с вычислением хеша файла.
        :param calculate_hash: True или False вычисления хеша файла;
        :param doc_type_id: ID типа документа к которому прикрепляются файлы;
        """
        data = {
                "CalculateHash": calculate_hash,
                "DocumentTypeId": doc_type_id
                }
        return data

    @staticmethod
    def data_upload_file_with_calculate_hash(calculate_hash=None):
        """
        Тело запроса для загрузки файла с вычислением хеша файла и без указания ID типа документа.
        :param calculate_hash: True или False вычисления хеша файла;
        """
        data = {
            "CalculateHash": calculate_hash
        }
        return data

    @staticmethod
    def data_for_invalid_file_upload(file_type_id=None, doc_type_id=None):
        """
        Тело запроса для загрузки файла с указанием типа файла.
        :param file_type_id: ID типа файла;
        :param doc_type_id: ID типа документа;
        """
        data = {
            "FileTypeId": file_type_id,
            "DocumentTypeId": doc_type_id
        }
        return data

    def get_information_about_file(self, api_version=None, file_id=None, header=None, response=200) -> Response:
        """Получение информации о файле."""
        res = request(
            method="GET",
            url=f"{self.app.url}{api_version}File/{file_id}",
            headers=header
        )
        logger.info(f"GET запрос на получение информации о файле. Ответ: {res.status_code}")
        assert res.status_code == response
        return res.json()

    def attach_files_to_document(self, response=200, api_version=None, doc_ver_id=None, quantity_files=None,
                                 source_date=None, calculate_hash=True) -> Response:
        """
        Прикрепление двух файлов к документу.
        :param response: Ожидаемый ответ;
        :param api_version: Версия API;
        :param doc_ver_id: ID версии документа к которому прикрепляются файлы;
        :param quantity_files: Кол-во прикрепляемых файлов;
        :param source_date: Дата создания типа документа;
        :param calculate_hash: Вычислять хэш или нет;
        """
        res = request(
            method="POST",
            verify=False,
            url=f"{self.app.url}{api_version}File",
            data={
                "DocumentVersionId": doc_ver_id,
                "SourceDate": source_date,
                "CalculateHash": calculate_hash,
            },
            files=self.open_file(quantity_files=quantity_files)
        )
        logger.info(f"POST: Загрузка файлов. Ответ: {res.status_code}")
        assert res.status_code == response
        return res.json()

    def upload_files(self, response=200, api_version=None, header=None, data=None, quantity_files=None) -> Response:
        """
        Метод загрузки файла в систему.
        :param response: Ожидаемый ответ;
        :param api_version: Версия API;
        :param quantity_files: Кол-во прикрепляемых файлов;
        :param header: Токен авторизации;
        :param data: Тело POST запроса;
        """
        res = request(
            method="POST",
            verify=False,
            url=f"{self.app.url}{api_version}File",
            headers=header,
            data=data,
            files=self.open_file(quantity_files=quantity_files)
        )
        logger.info(f"POST: Загрузка файлов. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        assert res.json()["result"]["files"][0]["name"] == self.open_file()[0][1][0]
        return res.json()

    def invalid_upload_files(self, response=404, api_version=None, url="File", data=None, quantity_files=None) -> Response:
        """
        Метод невалидной загрузки файла в систему.
        :param response: Ожидаемый ответ;
        :param api_version: Версия API;
        :param url: URL;
        :param quantity_files: Кол-во прикрепляемых файлов;ла;
        :param data: Тело POST запроса;
        """
        res = request(
            method="POST",
            verify=False,
            url=f"{self.app.url}{api_version}{url}",
            data=data,
            files=self.open_file(quantity_files=quantity_files)
        )
        logger.info(f"POST: Загрузка файлов. Ответ: {res.status_code}")
        assert res.status_code == response
        assert res.json()["success"] is False
        return res.json()
