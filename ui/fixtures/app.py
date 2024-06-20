from ui.fixtures.pages.base_page import BasePage
from ui.fixtures.pages.login import LoginPage
from ui.fixtures.pages.document.documents import DocumentsPage
from ui.fixtures.pages.entities.entities import EntitiesPage
from ui.fixtures.pages.administration.document_types import DocumentsTypePage
from ui.fixtures.pages.updates_and_instructions.instructions import InstructionsPage
from ui.fixtures.pages.precondition import CreatePrecondition
from ui.fixtures.pages.document.sorting.sorting import SortingPage
from ui.fixtures.pages.document.filtration.filtration import FiltrationPage


class Application:
    def __init__(self, driver, url: str):
        self.driver = driver
        self.url = url
        self.base_page = BasePage(self)
        self.login = LoginPage(self)
        self.document = DocumentsPage(self)
        self.entities = EntitiesPage(self)
        self.doc_type = DocumentsTypePage(self)
        self.instructions = InstructionsPage(self)
        self.precondition = CreatePrecondition(self)
        self.sort = SortingPage(self)
        self.filter = FiltrationPage(self)

    def quit(self):
        self.driver.quit()
