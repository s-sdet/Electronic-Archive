import os
import logging

from pathlib import Path
from requests import Response, request
from api.fixtures.base import BaseClass

logger = logging.getLogger("Live Plus. Electronic Archive")


class DownloadActual(BaseClass):
    """Класс взаимодействия с актуальностью файлов версий документов."""

    API_V0_DOCUMENT = "api/v0.1/"  # API v0.1
    API_V1_DOCUMENT = "api/v1.0/"  # API v1.0
    API_V2_DOCUMENT = "api/v2.0/"  # API v2.0
    API_V3_DOCUMENT = "api/v3.0/"  # API v3.0

    DATA_FOR_DOWNLOADING_FILE = [
        ["ca6a9bed-6e99-585a-7549-c478a5415b42", "api/v0.1/"],
        ["3ace26a4-5a06-f993-1215-7fb463efa597", "api/v1.0/"],
        ["d6a200c3-04c7-4f52-f7d2-f2d46397d133", "api/v2.0/"],
        ["0754d896-3c0e-b1ca-aaf5-d5fa12050394", "api/v3.0/"],
    ]

    def get_info_about_document_version(self, api_version=None, doc_ver_id=None, header=None, response=200) -> Response:
        """Получение данных по ID версии документа или его версии."""
        res = request(
            method="GET",
            url=f"{self.app.url}{api_version}DocumentVersion/{doc_ver_id}",
            headers=header
        )
        logger.info(f"GET запрос получения данных по ID версии документа. Ответ: {res.status_code}")
        assert res.status_code == response
        return res.json()

    def download_file_by_doc_version_id(self, api_version=None, doc_ver_id=None, is_inline=False, header=None,
                                        file_name=None, response=200) -> Response:
        """Скачивание актуального файла по id версии документа."""
        res = request(
            method="GET",
            url=f"{self.app.url}{api_version}DocumentVersion/{doc_ver_id}/DownloadActual?isInline={is_inline}",
            headers=header
        )
        logger.info(f"GET запрос на скачивание актуального файла по id версии документа. Ответ: {res.status_code}")
        assert res.status_code == response
        with open(Path(os.getcwd(), "download_files", file_name), "wb") as file:
            file.write(res.content)
            logger.info(f"Открыт файл: {file_name}")
            files = os.listdir(Path(os.getcwd(), "download_files"))
            assert file_name in files
        os.remove(Path(os.getcwd(), "download_files", file_name))
        return res
