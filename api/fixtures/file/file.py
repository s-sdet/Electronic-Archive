import os
import logging
import itertools
import mimetypes
from io import BytesIO
from pathlib import Path
from requests import Response, request, JSONDecodeError
from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class File(BaseClass):
    """Класс взаимодействия с файлами документов."""

    API_V0_FILE = "api/v0.1/"  # API v0.1
    API_V1_FILE = "api/v1.0/"  # API v1.0
    API_V2_FILE = "api/v2.0/"  # API v2.0
    API_V3_FILE = "api/v3.0/"  # API v3.0

    # Для параметризации загрузки двух файлов, где:
    # 1 - версия API, 2 - дата добавления версии, 3 - вычисление хеша.
    DATA_FOR_UPLOADING_TWO_FILES = [
        ["api/v2.0/", "2023-08-09T20:00:00.000Z", True],
        ["api/v3.0/", "2023-08-09T20:00:00.000Z", True],
    ]

    @staticmethod
    def open_file(key: str = "files", quantity_files=None, specific_files=None):
        """
        Метод открытия файла с добавлением в массив для дальнейшего прикрепления к документу.
        :param key: Название ключа требуемое API;
        :param quantity_files: Ожидаемое кол-во файлов;
        :param specific_files: Список конкретных файлов для загрузки или строка с именем файла;
        """
        files = []
        files_folder = Path(os.getcwd(), "files")

        # Преобразуем строку с именем файла в список, если передана одна строка
        if isinstance(specific_files, str):
            specific_files = [specific_files]

        if specific_files:
            # Если передан список конкретных файлов (или один файл), работаем только с ними
            file_names = specific_files
        else:
            # Если список не передан, загружаем все файлы в директории (ограничиваем количеством quantity_files)
            file_names = itertools.islice(os.listdir(files_folder), quantity_files)

        for file_name in file_names:
            file_path = files_folder / file_name

            # Проверяем, существует ли файл
            if not file_path.is_file():
                logger.warning(f"Файл {file_name} не найден в директории {files_folder}")
                continue

            # Определение MIME-типа файла
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'  # Тип по умолчанию, если не удается определить

            # Открываем файл и читаем его содержимое в память
            with open(file_path, "rb") as file:
                file_content = file.read()

            # Создаем объект BytesIO для передачи содержимого в запрос
            file_stream = BytesIO(file_content)
            files.append((key, (file_name, file_stream, mime_type)))
            logger.info(f"Загружаемый файл: {file_name} с MIME-типом: {mime_type}")

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
    def file_upload(doc_id=None):
        """
        Универсальное тело запроса для загрузки файлов
        :param doc_id:
        """
        data = {
            "documentId": doc_id
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
            "CalculateHash": calculate_hash,
            "mimeType": ""
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

    def get_information_about_file(self, api_version="api/v3.0/", file_id=None, header=None, response=200) -> Response:
        """Получение информации о файле."""
        res = request(
            method="GET",
            url=f"{self.app.url}{api_version}File/{file_id}",
            headers=header
        )
        logger.info(f"GET: Получение информации о файле. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
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
            url=f"{self.app.url}{api_version}File",
            data={
                "DocumentVersionId": doc_ver_id,
                "SourceDate": source_date,
                "CalculateHash": calculate_hash,
            },
            files=self.open_file(quantity_files=quantity_files)
        )
        logger.info(f"POST: Загрузка файлов. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == response
        return res.json()

    def upload_files(self, response=200, api_version="api/v4.0/", doc_id=None, url="Files", file_type_id="",
                     header=None, data=None, quantity_files=None) -> Response:
        """
        Метод загрузки файла в систему.
        :param response: Ожидаемый ответ;
        :param api_version: Версия API;
        :param doc_id: ID документа к которому прикрепляется файл;
        :param file_type_id: ID типа файла;
        :param url: URL;
        :param quantity_files: Кол-во прикрепляемых файлов;
        :param data: Тело POST запроса;
        :param header: Токен авторизации;
        """
        res = request(
            method="POST",
            url=f"{self.app.url}{api_version}Document/{doc_id}/{url}/{file_type_id}",
            headers=header,
            data=data,
            files=self.open_file(quantity_files=quantity_files)
        )
        # try except добавлен по причине, если передан ID несуществующего документа - json не возвращается, проверка
        # только по статусу кода.
        try:
            logger.info(f"POST: Загрузка файлов. Ответ: {res.status_code}")
            logger.info(f"JSON: {res.json()}")
            assert res.status_code == response
            return res.json()
        except JSONDecodeError:
            assert res.status_code == response

    def invalid_upload_files(self, response=400, api_version="api/v4.0/", doc_id=None, url="Files", header=None,
                             data=None, quantity_files=None) -> Response:
        """
        Метод невалидной загрузки файла в систему.
        :param response: Ожидаемый ответ;
        :param api_version: Версия API;
        :param doc_id: ID документа к которому прикрепляется файл;
        :param url: URL;
        :param header: Токен авторизации;
        :param data: Тело POST запроса;
        :param quantity_files: Кол-во прикрепляемых файлов;ла;
        """
        res = request(
            method="POST",
            url=f"{self.app.url}{api_version}Document/{doc_id}/{url}",
            headers=header,
            data=data,
            files=self.open_file(quantity_files=quantity_files)
        )
        logger.info(f"POST: Загрузка файлов. Ответ: {res.status_code}")
        # try except добавлен по причине, если передан ID несуществующего документа - json не возвращается, проверка
        # только по статусу кода.
        try:
            logger.info(f"JSON: {res.json()}")
            assert res.status_code == response
            assert res.json()["success"] is False
            return res.json()
        except JSONDecodeError:
            logger.info(f"Status code: {res.status_code}")
            assert res.status_code == response

    def update_files(self, response=200, api_version="api/v4.0/", doc_id=None, url="Files", file_type_id="",
                     header=None, data=None, quantity_files=None) -> Response:
        """
        Метод обновления файла в системе.
        :param response: Ожидаемый ответ;
        :param api_version: Версия API;
        :param doc_id: ID документа к которому прикрепляется файл;
        :param file_type_id: ID типа файла;
        :param url: URL;
        :param quantity_files: Кол-во прикрепляемых файлов;
        :param data: Тело POST запроса;
        :param header: Токен авторизации;
        """
        res = request(
            method="PUT",
            url=f"{self.app.url}{api_version}Document/{doc_id}/{url}/{file_type_id}",
            headers=header,
            data=data,
            files=self.open_file(quantity_files=quantity_files)
        )
        try:
            logger.info(f"PUT: Обновление файлов. Ответ: {res.status_code}")
            logger.info(f"JSON: {res.json()}")
            assert res.status_code == response
            return res.json()
        except JSONDecodeError:
            assert res.status_code == response

    def upload_files_in_api_v3(self, status_code=200, api_version="api/v3.0/", url="File", header=None, data=None,
                               quantity_files=None) -> Response:
        """
        Метод загрузки файла в систему.
        :param status_code: Ожидаемый ответ;
        :param api_version: Версия API;
        :param url: URL;
        :param quantity_files: Кол-во прикрепляемых файлов;
        :param header: Токен авторизации;
        :param data: Тело POST запроса;
        """
        res = request(
            method="POST",
            url=f"{self.app.url}{api_version}{url}",
            headers=header,
            data=data,
            files=self.open_file(quantity_files=quantity_files)
        )
        logger.info(f"POST: Загрузка файлов. Ответ: {res.status_code}")
        logger.info(f"JSON: {res.json()}")
        assert res.status_code == status_code
        assert res.json()["result"]["files"][0]["name"] == self.open_file()[0][1][0]
        return res.json()

    def invalid_upload_files_in_api_v3(self, status_code=404, api_version="api/v3.0/", url="File", data=None,
                                       quantity_files=None) -> Response:
        """
        Метод невалидной загрузки файла в API v3.
        :param status_code: Ожидаемый ответ;
        :param api_version: Версия API;
        :param url: URL;
        :param quantity_files: Кол-во прикрепляемых файлов;ла;
        :param data: Тело POST запроса;
        """
        res = request(
            method="POST",
            url=f"{self.app.url}{api_version}{url}",
            data=data,
            files=self.open_file(quantity_files=quantity_files)
        )
        logger.info(f"POST: Невалидная загрузка файлов. Ответ: {res.status_code}")
        assert res.status_code == status_code
        assert res.json()["success"] is False
        return res.json()
