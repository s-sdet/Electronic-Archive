import pytest
from pytest_testrail.plugin import pytestrail
from api.fixtures.document.document import Document
from api.fixtures.document_version.document_version import DocumentVersion
from api.fixtures.document_version.set_actual.set_actual import DocumentVersionSetActual


class TestsSetActual:
    """Тесты для изменения актуальности версий документа."""

    @pytest.mark.lp
    @pytestrail.case("C19034911", "C19011411")
    @pytest.mark.parametrize("doc_api, doc_ver_api",
                             DocumentVersionSetActual.DATA_FOR_CHANGING_VERSION_OF_DOCUMENT_ACTUAL)
    def test_make_first_version_of_document_actual(self, app, auth, doc_type_without_file_type, doc_api, doc_ver_api):
        """Тест установки актуальности первой версии документа по ее ID."""

        # Создание документа и его версии.
        create_doc = app.doc.save_document(data=Document.for_saving_document_with_date(
            doc_type_id=doc_type_without_file_type["result"]["id"]), url_api=doc_api)

        # Создание второй версии уже созданного документа
        create_ver = app.doc_ver.create_document_version(url_api=doc_ver_api,
                                                         data=DocumentVersion.for_creating_minor_version(
                                                             doc_id=create_doc['result']['documentId']))
        # Создание третьей версии уже созданного документа
        app.doc_ver.create_document_version(url_api=doc_ver_api, data=DocumentVersion.for_creating_minor_version(
                                            doc_id=create_doc['result']['documentId']))
        # Получение информации о документе, проверка, что последняя версия документа имеет признак актуальности
        get_info = app.doc.get_data_by_document_id(url_api=doc_api, doc_id=create_doc['result']['documentId'])
        assert get_info['result']['documentVersions'][0]['isActual'] is True

        # Установка признака актуальности второй созданной версии документа по ее id
        app.doc_ver_set_actual.set_document_version_actual(url_api=doc_ver_api, ver_id=create_ver['result']['id'],
                                                           set_actual=True)
        # Получение информации о документе, проверка, что вторая версия документа имеет признак актуальности
        get_info = app.doc.get_data_by_document_id(url_api=doc_api, doc_id=create_doc['result']['documentId'])
        assert get_info['result']['documentVersions'][1]['isActual'] is True

        # Установка признака актуальности первой созданной версии документа по ее id
        app.doc_ver_set_actual.set_document_version_actual(url_api=doc_ver_api, set_actual=True,
                                                           ver_id=create_doc['result']['documentVersionId'])
        # Получение информации о документе, проверка, что первая версия документа имеет признак актуальности
        get_info = app.doc.get_data_by_document_id(url_api=doc_api, doc_id=create_doc['result']['documentId'])
        assert get_info['result']['documentVersions'][2]['isActual'] is True
