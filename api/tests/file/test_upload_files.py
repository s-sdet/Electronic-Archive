import pytest
from pytest_testrail.plugin import pytestrail

from api.fixtures.document.document import Document
from api.fixtures.file.file import File
from api.fixtures.assertions import Assertions
from api.data.constants import ApiVersions, FileNotice, DocumentTypeNotice


class TestsUploadFiles:
    """Тесты загрузки/прикрепления файлов к документам."""

    doc_type = DocumentTypeNotice()

    @pytest.mark.lp
    @pytestrail.case("C18982459", "C18982450")
    @pytest.mark.parametrize("api_version, source_date, calculate_hash", File.DATA_FOR_UPLOADING_TWO_FILES)
    def test_upload_two_files_to_document_version_with_hash_calculation(
            self, app, auth, doc_type_without_file_type, api_version, source_date, calculate_hash):
        """
        Тест прикрепления двух файлов к версии документа с вычислением хеша файла.
        :param api_version: Версия API;
        :param source_date: Дата создания типа документа;
        :param calculate_hash: Вычислять хэш или нет;
        """
        doc = app.doc.create_document(
            url_api=api_version, header=auth, data=Document.data_for_creating_document_without_properties_and_files(
                doc_type_id=doc_type_without_file_type["result"]["id"]))
        res = app.file.attach_files_to_document(doc_ver_id=doc["result"]["documentVersionId"], api_version=api_version,
                                                source_date=source_date, calculate_hash=calculate_hash,
                                                quantity_files=2)
        Assertions.assert_upload_two_files_to_document_version(res=res, doc_ver_id=doc["result"]["documentVersionId"])

    @pytestrail.case("C17682355")
    def test_upload_file_with_invalid_file_type(self, app, auth):
        """Невалидный тест загрузки файла с указанием невалидного (не существующего) типа файла."""
        res = app.file.invalid_upload_files_in_api_v3(quantity_files=1, data=File.data_for_invalid_file_upload(
                                                        file_type_id=FileNotice.INVALID_FILE_TYPE_ID))
        assert res["error"] == FileNotice.ERROR_FILE_TYPE_ID.format(FileNotice.INVALID_FILE_TYPE_ID)

    @pytestrail.case("C17682357")
    def test_upload_file_with_invalid_document_type(self, app, auth):
        """Невалидный тест загрузки файла с указанием невалидного (не существующего) типа документа."""
        res = app.file.invalid_upload_files_in_api_v3(quantity_files=1, data=File.data_for_invalid_file_upload(
                                                        doc_type_id=FileNotice.INVALID_DOCUMENT_TYPE_ID))
        assert res["error"] == FileNotice.ERROR_DOC_TYPE_ID.format(FileNotice.INVALID_DOCUMENT_TYPE_ID)

    @pytestrail.case("C17682356")
    @pytest.mark.xfail(reason="Возможно падение теста, связано с багом: LP-2641")
    def test_upload_large_file_with_invalid_file_type(self, app, auth):
        """Невалидный тест загрузки большого файла с указанием невалидного (не существующего) типа файла."""
        res = app.file.invalid_upload_files_in_api_v3(url=FileNotice.URL_LARGE_FILE,
                                                      quantity_files=1, data=File.data_for_invalid_file_upload(
                                                        file_type_id=FileNotice.INVALID_FILE_TYPE_ID))
        assert res["error"] == FileNotice.ERROR_FILE_TYPE_ID.format(FileNotice.INVALID_FILE_TYPE_ID)

    @pytestrail.case("C20621608")
    def test_upload_file_without_file_type_id(self, app, doc_without_properties):
        """Валидный тест загрузки файла в созданном документе без FileTypeID."""
        res = app.file.upload_files(api_version=ApiVersions.API_V4,
                                    doc_id=doc_without_properties["result"]["documentId"], quantity_files=1)
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
    def test_upload_file_without_file(self, app, auth, auth_form_data, doc_without_properties):
        """Невалидный тест загрузки файла без прикрепления файла."""
        res = app.file.invalid_upload_files(header=auth_form_data, response=400, api_version=ApiVersions.API_V4,
                                            doc_id=doc_without_properties["result"]["documentId"], quantity_files=0)
        assert res["errorDetails"]["files"][0] == FileNotice.ERROR_FILE_NOT_UPLOAD

    @pytestrail.case("C20625515")
    def test_upload_file_with_invalid_document_id(self, app, auth_form_data, doc_id=FileNotice.INVALID_DOCUMENT_ID):
        """Невалидный тест загрузки файла с передачей невалидного DocumentID."""
        app.file.invalid_upload_files(response=404, api_version=ApiVersions.API_V4, doc_id=doc_id, quantity_files=1)

    @pytestrail.case("C20621937")
    def test_upload_two_files_without_file_type_id(self, app, auth, doc_without_properties, quantity_files=2):
        """Валидный тест загрузки 2х файлов в созданном документе без FileTypeID."""
        res = app.file.upload_files(api_version=ApiVersions.API_V4,
                                    doc_id=doc_without_properties["result"]["documentId"], quantity_files=2)
        assert len(res["result"]["files"][0]) == quantity_files
        assert "id" in (res["result"]["files"][0] and res["result"]["files"][1])

    @pytestrail.case("C20621938")
    @pytest.mark.parametrize("doc_name, metadata_type, metadata_type_value, quantity_files",
                             [("Тестовый документ", None, None, 1)])
    def test_upload_file_with_file_type_id(self, app, auth, doc_type_with_file_type, doc_name, metadata_type,
                                           metadata_type_value, quantity_files):
        """Валидный тест загрузки файла с указанием FileTypeID и с указанными расширениями."""
        # Создание документа с ID созданного типа документа
        doc = app.doc.create_document(header=auth,
                                      data=Document.data_for_creating_document_with_required_metadata_type(
                                        doc_type_id=doc_type_with_file_type["result"]["id"], name=doc_name,
                                        metadata_type=metadata_type, metadata_type_value=metadata_type_value))

        # Получение информации о типе файла для получения его ID, так как при создании ID не возвращается в json
        file_type_id = app.doc_type.get_file_type_id(header=auth, doc_type_id=doc_type_with_file_type["result"]["id"])

        # Загрузка файла с указанием ID документа и ID типа файла
        file = app.file.upload_files(doc_id=doc["result"]["documentId"],
                                     file_type_id=file_type_id["result"]["fileTypes"][0]["id"],
                                     quantity_files=quantity_files)
        assert "id" in file["result"]["files"][0]

        # Получение метаданных файла по id загруженного файла в API v3
        file_info = app.file.get_information_about_file(file_id=file["result"]["files"][0]["id"])
        assert file_info["result"]["id"] == file["result"]["files"][0]["id"]

    @pytestrail.case("C20621949", "C20624345")
    @pytest.mark.parametrize("entity_id, status_code", (("1c7ada92-a968-4656-a24e-5fe1fe9e634c", 400), ("", 404)))
    def test_upload_file_with_invalid_doc_id(self, app, auth_form_data, entity_id, status_code, quantity_files=1):
        """Невалидные тесты загрузки файлов с передачей невалидных DocumentID."""
        app.file.upload_files(doc_id=entity_id, file_type_id=entity_id, quantity_files=quantity_files,
                              response=status_code)
