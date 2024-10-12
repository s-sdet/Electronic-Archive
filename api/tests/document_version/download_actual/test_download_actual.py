import pytest
from pytest_testrail.plugin import pytestrail

from api.data.constants import DocumentTypeNotice
from api.fixtures.document_type.document_type import DocumentType
from api.fixtures.file.file import File


class TestsDownloadActual:
    """Тесты скачивания файлов версий документов."""

    doc_type = DocumentTypeNotice()

    @pytest.mark.lp
    @pytestrail.case("C19136296", "C19128455")
    @pytest.mark.parametrize("doc_type, api", ((doc_type.doc_type_name_latin, "api/v2.0/"),
                                               (doc_type.doc_type_name_latin, "api/v3.0/")))
    def test_download_current_file_by_document_version_id(self, app, auth, doc_type, api):
        """Тест скачивание актуального файла по id версии документа."""

        # Создание типа документа
        doc_type = app.doc_type.create_doc_type(
            url_api=api, header=auth,
            data=DocumentType.data_for_create_document_type_without_property_types(doc_type_name=doc_type))

        # Загрузка файла в систему
        file = app.file.upload_files_in_api_v3(api_version=api, quantity_files=1,
                                               data=File.data_upload_file_with_calculate_hash(calculate_hash=True))

        # Создание документа и его версии с указанием id загруженного в систему файла
        doc = app.doc.create_document(
            url_api=api, data=app.doc.data_for_creating_document_with_expire_and_source_date(
                doc_type_id=doc_type["result"]["id"], file_id=file["result"]["files"][0]["id"]))

        # Получение информации о версии документа
        get_info = app.download_actual.get_info_about_document_version(
            api_version=api, doc_ver_id=doc["result"]["documentVersionId"])
        file_name = get_info['result']['files'][0]['name']  # Получение имени документа
        assert 'files' in get_info['result']

        # Установка актуальности 1 файла выбранной версии документа
        app.set_actual.make_file_current(api_version=api, file_id=get_info['result']['files'][0]['id'])

        # Получение информации о файле
        app.file.get_information_about_file(api_version=api, file_id=get_info['result']['files'][0]['id'])
        assert get_info['result']['isActual'] is True

        # Скачивание актуального файла по id версии документа
        app.download_actual.download_file_by_doc_version_id(
            api_version=api, doc_ver_id=doc["result"]["documentVersionId"], file_name=file_name)
