from pytest_testrail.plugin import pytestrail
from api.fixtures.document.document import Document
from api.fixtures.assertions import Assertions
from api.data.constants import ApiVersions, DocumentNotice


class TestsGetDocumentLink:
    """Тесты получения связанных документов с их типами."""

    @pytestrail.case("C17125938")
    def test_get_document_with_list_ist_versions_and_files_by_document_id(self, app, auth):
        """Тест получения связанных документов-родителей с их типами по id документа дочернего."""
        res = app.doc_link.get_linked_documents_by_id(api_version=ApiVersions.API_V3,
                                                      doc_id=DocumentNotice.LINKED_DOC_ID)
        Assertions.assertion_linked_documents(res=res)
