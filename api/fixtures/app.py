from api.fixtures.base import BaseClass
from api.fixtures.document.document import Document
from api.fixtures.document.actual_version.actual_version import ActualVersion
from api.fixtures.document_version.document_version import DocumentVersion
from api.fixtures.document_type.document_type import DocumentType
from api.fixtures.document_version.download_actual.download_actual import DownloadActual
from api.fixtures.file.file import File
from api.fixtures.file.set_actual.set_actual import SetActual
from api.fixtures.document_version.set_actual.set_actual import DocumentVersionSetActual
from api.fixtures.validation.validation import Validation
from api.fixtures.document_version.history.history import History
from api.fixtures.document_link.document_link import DocumentLink
from api.fixtures.document.filter.filter import Filter
from api.fixtures.graphic_sign.graphic_sign import GraphicSign


class App:
    def __init__(self, url: str):
        self.url = url
        self.base = BaseClass
        self.doc = Document(self)
        self.act_ver = ActualVersion(self)
        self.doc_ver = DocumentVersion(self)
        self.doc_type = DocumentType(self)
        self.download_actual = DownloadActual(self)
        self.file = File(self)
        self.set_actual = SetActual(self)
        self.doc_ver_set_actual = DocumentVersionSetActual(self)
        self.validation = Validation(self)
        self.history = History(self)
        self.doc_link = DocumentLink(self)
        self.filter = Filter(self)
        self.graphic_sign = GraphicSign(self)
