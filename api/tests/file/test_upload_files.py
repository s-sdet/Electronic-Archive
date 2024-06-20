import pytest
from pytest_testrail.plugin import pytestrail
from api.fixtures.file.file import File
from api.fixtures.assertions import Assertions
from api.data.constants import ApiVersions, FileNotice, DocumentNotice


class TestsUploadFiles:
    """Тесты загрузки/прикрепления файлов к документам."""

    @pytest.mark.lp
    @pytestrail.case("C18982464", "C18982463", "C18982459", "C18982450")
    @pytest.mark.parametrize("doc_ver_id, api_version, source_date, calculate_hash", File.DATA_FOR_UPLOADING_TWO_FILES)
    def test_upload_two_files_to_document_version_with_hash_calculation(self, app, auth, doc_ver_id, api_version,
                                                                        source_date, calculate_hash):
        """
        Тест прикрепления двух файлов к версии документа с вычислением хеша файла.
        :param api_version: Версия API;
        :param doc_ver_id: ID версии документа к которому прикрепляются файлы;
        :param source_date: Дата создания типа документа;
        :param calculate_hash: Вычислять хэш или нет;
        """
        res = app.file.attach_files_to_document(doc_ver_id=doc_ver_id, api_version=api_version, source_date=source_date,
                                                calculate_hash=calculate_hash, quantity_files=2)
        Assertions.assert_upload_two_files_to_document_version(res=res, doc_ver_id=doc_ver_id)

    @pytestrail.case("C17682355")
    def test_upload_file_with_invalid_file_type(self, app, auth):
        """Невалидный тест загрузки файла с указанием невалидного (не существующего) типа файла."""
        res = app.file.invalid_upload_files(api_version=ApiVersions.API_V3, quantity_files=1,
                                            data=File.data_for_invalid_file_upload(
                                                file_type_id=FileNotice.INVALID_FILE_TYPE_ID))
        assert res["error"] == FileNotice.ERROR_FILE_TYPE_ID.format(FileNotice.INVALID_FILE_TYPE_ID)

    @pytestrail.case("C17682357")
    def test_upload_file_with_invalid_document_type(self, app, auth):
        """Невалидный тест загрузки файла с указанием невалидного (не существующего) типа документа."""
        res = app.file.invalid_upload_files(api_version=ApiVersions.API_V3, quantity_files=1,
                                            data=File.data_for_invalid_file_upload(
                                                doc_type_id=FileNotice.INVALID_DOCUMENT_TYPE_ID))
        assert res["error"] == FileNotice.ERROR_DOC_TYPE_ID.format(FileNotice.INVALID_DOCUMENT_TYPE_ID)

    @pytestrail.case("C17682356")
    def test_upload_large_file_with_invalid_file_type(self, app, auth):
        """Невалидный тест загрузки большого файла с указанием невалидного (не существующего) типа файла."""
        res = app.file.invalid_upload_files(api_version=ApiVersions.API_V3, url=FileNotice.URL_LARGE_FILE,
                                            quantity_files=1, data=File.data_for_invalid_file_upload(
                                                file_type_id=FileNotice.INVALID_FILE_TYPE_ID))
        assert res["error"] == FileNotice.ERROR_FILE_TYPE_ID.format(FileNotice.INVALID_FILE_TYPE_ID)

    @pytestrail.case("C20621608")
    def test_upload_file_without_file_type_id(self, app, auth):
        """Валидный тест загрузки файла в созданном документе без FileTypeID."""
        res = app.file.upload_files(api_version=ApiVersions.API_V4, quantity_files=1,
                                    data=File.data_for_file_upload(doc_id=DocumentNotice.DOC_ID_V4))
        assert "id" in res["result"]["files"][0]

        # Получение метаданных файла по id загруженного файла в API v3
        file_api_v3 = app.file.get_information_about_file(api_version=ApiVersions.API_V3,
                                                          file_id=res["result"]["files"][0]["id"])
        assert file_api_v3["result"]["id"] == res["result"]["files"][0]["id"]

        # Получение метаданных файла по id загруженного файла в API v2
        file_api_v2 = app.file.get_information_about_file(api_version=ApiVersions.API_V2,
                                                          file_id=res["result"]["files"][0]["id"])
        assert file_api_v2["result"]["id"] == res["result"]["files"][0]["id"]

    @pytestrail.case("C20624352")
    def test_upload_file_without_file(self, app, auth):
        """Невалидный тест загрузки файла без прикрепления файла."""
        res = app.file.invalid_upload_files(response=400, api_version=ApiVersions.API_V4, quantity_files=0,
                                            data=File.data_for_file_upload(doc_id=DocumentNotice.DOC_ID_V4))
        assert res["errorDetails"]["files"][0] == FileNotice.ERROR_FILE_NOT_UPLOAD

    @pytestrail.case("C20625515")
    def test_upload_file_with_invalid_document_id(self, app, auth, doc_id=FileNotice.INVALID_DOCUMENT_ID):
        """Невалидный тест загрузки файла с передачей невалидного DocumentID."""
        res = app.file.invalid_upload_files(response=400, api_version=ApiVersions.API_V4, quantity_files=1,
                                            data=File.data_for_file_upload(doc_id=doc_id))
        assert res["errorDetails"]["documentId"][0] == FileNotice.ERROR_DOCUMENT_ID.format(doc_id)

    @pytestrail.case("C20621937")
    def test_upload_two_files_without_file_type_id(self, app, auth, quantity_files=2):
        """Валидный тест загрузки 2х файлов в созданном документе без FileTypeID."""
        res = app.file.upload_files(api_version=ApiVersions.API_V4, quantity_files=quantity_files,
                                    data=File.data_for_file_upload(doc_id=DocumentNotice.DOC_ID_V4))
        assert len(res["result"]["files"][0]) == quantity_files
        assert "id" in (res["result"]["files"][0] and res["result"]["files"][1])

    @pytestrail.case("C20621938")
    @pytest.mark.parametrize("api_v3, api_v4, doc_id, file_type_id", [(ApiVersions.API_V3, ApiVersions.API_V4,
                                                                       "9b95449b-afca-8499-0470-a6330258ee0d",
                                                                       "ddc780a7-92b8-f90b-0d93-2becd0da45bf")])
    def test_upload_file_with_file_type_id(self, app, auth, api_v3, api_v4, doc_id, file_type_id, quantity_files=1):
        """Валидный тест загрузки файла с указанием FileTypeID и с указанными расширениями."""
        res = app.file.upload_files(api_version=api_v4, quantity_files=quantity_files,
                                    data=File.data_for_file_upload(doc_id=doc_id, file_type_id=file_type_id))
        assert len(res["result"]["files"][0]) == quantity_files
        assert "id" in res["result"]["files"][0]

        # Получение метаданных файла по id загруженного файла в API v3
        file_api_v3 = app.file.get_information_about_file(api_version=api_v3,
                                                          file_id=res["result"]["files"][0]["id"])
        assert file_api_v3["result"]["id"] == res["result"]["files"][0]["id"]

