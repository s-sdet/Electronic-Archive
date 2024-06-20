from pytest_testrail.plugin import pytestrail
from api.fixtures.document.document import Document
from api.fixtures.assertions import Assertions
from api.fixtures.document_version.document_version import DocumentVersion
from api.data.constants import ApiVersions, DocumentTypeNotice, DocumentVersionNotice


class TestsFiltrationDocumentVersion:
    """Тесты фильтраций версий документов."""

    @pytestrail.case("C19972662")
    def test_get_document_versions_using_filter_modified_date_from(self, app, auth):
        """Тест получения списка версий документа по фильтру "Дата изменения от" (ModifiedDateFrom)."""
        res = app.doc_ver.get_document_versions(
            api_version=ApiVersions.API_V3,
            query_string=DocumentVersion.FILTER_MODIFIED_DATE_FROM.format(DocumentTypeNotice.DOC_TYPE_ID,
                                                                          DocumentTypeNotice.SOURCE_DATE)
        )
        Assertions.assertion_modified_on_in_documents(res=res, doc_type_id=DocumentTypeNotice.DOC_TYPE_ID)

    @pytestrail.case("C17126038")
    def test_get_document_versions_using_filter_field_name(self, app, auth):
        """Тест получения списка версий документа по фильтру fieldName + DateLaterThan."""
        res = app.doc_ver.get_document_versions(
            api_version=ApiVersions.API_V3,
            query_string=DocumentVersion.FILTER_FIELD_NAME.format(DocumentVersionNotice.DOC_ID_WITH_MULTIPLE_VERSIONS,
                                                                  DocumentVersionNotice.DATE_VALUE)
        )
        assert "documentProperties" in res["result"]["data"][0]
