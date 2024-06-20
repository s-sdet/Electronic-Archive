from pytest_testrail.plugin import pytestrail
from api.data.constants import ApiVersions


class TestsGetHistory:
    """Тесты получения истории версий документов."""

    @pytestrail.case("C19002657")
    def test_get_history_by_document_version_id(self, app, auth):
        """Тест получения информации об истории версии документа по ее id."""
        res = app.history.get_history(api_ver=ApiVersions.API_V3,
                                      doc_ver_id="789632e2-a693-fd09-bffc-8969e7a4ceb7")
        # Проверяем, что в ответе есть массив "data" содержащий историю изменений
        assert "data" in res["result"]
        assert res["result"]["data"][0]["entityType"] != "DocumentEntity"
