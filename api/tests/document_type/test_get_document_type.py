import pytest
from pytest_testrail.plugin import pytestrail
from api.data.constants import ApiVersions
from api.fixtures.assertions import Assertions


class TestsGetDocumentType:
    """Тесты создания и получения типов документов."""

    @pytest.mark.lp
    @pytestrail.case("C17483107", "C17468155")
    def test_search_document_type(self, app, auth, name="пасп"):
        """
        C17483107: Позитивный тест поиска типа документа не связанного с папкой, по части названия типа документа (name)
        C17468155: Позитивный тест поиска типа документа по части названия типа документа (name).
        """
        res = app.doc_type.get_document_type(
            header=auth,
            key=name
        )
        Assertions.assert_search_document_type_by_document_name(res=res, name=name)

    @pytestrail.case("C17486706")
    def test_get_info_non_existent_folder(self, app, auth):
        """Тест проверки возвращение пустого массива в ответе, при передаче в запросе несуществующего id папки."""
        res = app.doc_type.get_info(
            header=auth,
            url_api=ApiVersions.API_V3,
            url="DocumentType?ParentFolderId=",
            folder_id="20de722a-6b33-4d0f-a7d9-a0759c49e4a1"
        )
        assert res['result']['data'] == []
