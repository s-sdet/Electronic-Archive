import pytest
from pytest_testrail.plugin import pytestrail
from api.fixtures.document_version.document_version import DocumentVersion
from api.fixtures.file.file import File


class TestsGetHistory:
    """Тесты получения истории версий документов."""

    @pytestrail.case("C17129194")
    @pytest.mark.xfail(reason="Возможно падение из-за отсутствия метода History на дев окружении в свагере.")
    def test_get_history_by_document_version_id(self, app, auth, doc_type_without_file_type, api="api/v3.0/"):
        """Тест получения информации об истории версии документа по ее id."""
        # Загрузка 3х файлов в систему
        file = app.file.upload_files_in_api_v3(api_version=api, quantity_files=3,
                                               data=File.data_upload_file_with_calculate_hash(calculate_hash=True))

        # Создание документа и его версии с указанием id загруженного в систему файла
        doc = app.doc.create_document(
            url_api=api, data=app.doc.data_for_creating_document_with_expire_and_source_date(
                doc_type_id=doc_type_without_file_type["result"]["id"], file_id=file["result"]["files"][0]["id"]))

        # Создание второй версии документа с передачей ID второго файла
        for index in range(1, 3):
            app.doc_ver.create_document_version(
                url_api=api, data=DocumentVersion.for_document_version_with_file(
                    doc_id=doc["result"]["documentId"], file_id=file["result"]["files"][index]["id"]))

        res = app.history.get_history(api_ver=api,
                                      doc_ver_id=doc["result"]["documentVersionId"])
        # Проверяем, что в ответе есть массив "data" содержащий историю изменений
        assert "data" in res["result"]
        assert res["result"]["data"][0]["entityType"] != "DocumentEntity"
