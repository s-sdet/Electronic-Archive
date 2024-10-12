import pytest
from pytest_testrail.plugin import pytestrail
from api.data.constants import ApiVersions
from api.fixtures.document.document import Document
from api.fixtures.document_type.document_type import DocumentType
from api.fixtures.assertions import Assertions


class TestsGetActualVersion:
    """Тесты получения актуальной версии документов."""

    @pytest.mark.lp
    @pytestrail.case("C17498618")
    def test_get_actual_version_of_document_by_document_id(self, app, auth):
        """Тест получения актуальной версии документа по document ID."""

        doc_type = app.doc_type.create_doc_type(
            url_api=ApiVersions.API_V3, header=auth,
            data=DocumentType.doc_type_with_metadata_type_and_without_file_type_in_v3())

        # Сохранение документа и его версии документа с указанием даты окончания действия, дате создания версии в
        # системе-источнике, дополнительными метаданными, БЕЗ прикрепления файлов и БЕЗ основных 6 полей метаданных.
        res = app.doc.save_document(
            header=auth,
            url_api=Document.URL_API_V3_DOCUMENT,
            data=Document.for_saving_document_with_date(doc_type_id=doc_type["result"]["id"])
        )

        res_act_ver = app.act_ver.get_actual_version(header=auth, doc_id=res['result']['documentId'])
        Assertions.assert_actual_version_document_by_document_id(res=res, res_act_ver=res_act_ver)

    @pytestrail.case("C17498620")
    def test_saving_document_version_as_current_after_its_expiration_date(
            self, app, auth, doc_type_without_file_type_in_v3, url_api=ApiVersions.API_V3):
        """Тест сохранения версии документа как актуальной после истечения ее срока действия."""
        doc = app.doc.create_document(url_api=url_api, data=Document.data_for_creating_document_whit_expire_date(
            doc_type_id=doc_type_without_file_type_in_v3["result"]["id"], expire_date="2023-07-06T11:12:34.833Z"))
        res = app.doc.get_doc_info_by_doc_id(doc_id=doc["result"]["documentId"])
        # Проверяем, что версия документа имеет признак актуальности
        assert 'isActual' in res["result"]["documentVersions"][0]
