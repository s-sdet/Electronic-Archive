import os
import logging

from selenium.webdriver.common.by import By
from ui.fixtures.pages.base_page import BasePage
from ui.data.constants import InstructionsNotice
from ui.fixtures.pages.document.documents import download_wait, assertion_downloaded_file_in_directory

logger = logging.getLogger("Electronic Archive")


def deleting_png_files(directory):
    """Метод удаления файлов в папке."""
    for f in os.listdir(directory):
        if not f.endswith(".pdf"):
            continue
        os.remove(os.path.join(directory, f))


class InstructionsPage(BasePage):
    """Страница инструкций ***"""

    TITLE_UPDATES_AND_INSTRUCTIONS = (By.XPATH, "//h2[text()='Обновления и инструкции']")  # Заголовок раздела
    DOWNLOAD_FILE_NAME = (By.XPATH, "//div[@aria-haspopup='listbox']")  # Название скачиваемого файла
    FILE_DISPLAY = (By.XPATH, "//div[contains(@class, 'react-pdf__Document')]")  # Предпросмотр инструкции

    # Ссылки
    LINK_UPDATES_AND_INSTRUCTIONS = (By.XPATH, "//div[@id='root']//nav/div[2]/div[4]")  # Ссылка раздела
    LINK_INSTRUCTIONS = (By.XPATH, "//span[text()='Просмотр инструкций']")  # Вкладка Инструкции

    # Кнопки
    BUTTON_DOWNLOAD_FILE = (By.XPATH, "//div[@class='sc-bpUBKd idHsp']//button")  # Кнопка скачать файл инструкции

    def click_link_updates_and_instructions(self):
        """Переход в раздел Обновления и инструкции."""
        self.click(locator=self.LINK_UPDATES_AND_INSTRUCTIONS)

        logger.info(f"Заголовок раздела: {self.get_text(locator=self.TITLE_UPDATES_AND_INSTRUCTIONS)}")
        # Проверка, что переход в раздел "Сущности" выполнен
        assert self.get_text(
            locator=self.TITLE_UPDATES_AND_INSTRUCTIONS) == InstructionsNotice.TITLE_UPDATES_AND_INSTRUCTIONS

    def click_link_instructions(self):
        """Переход во вкладку инструкции."""
        self.element_is_enabled(locator=self.LINK_INSTRUCTIONS)  # Ожидание элемента
        self.click(locator=self.LINK_INSTRUCTIONS)

    def download_file(self, directory="download_files"):
        """Скачивание инструкции в режиме предпросмотра."""
        self.element_is_enabled(locator=self.FILE_DISPLAY, wait_time=30)  # Ожидание загрузки отображения файла
        self.click(locator=self.BUTTON_DOWNLOAD_FILE)  # Клик по кнопке скачать
        download_wait(directory=directory)  # Скачивание файла в локальную папку

        # Проверка, что файл скачан
        assertion_downloaded_file_in_directory(directory=directory,
                                               file_name=self.get_text(locator=self.DOWNLOAD_FILE_NAME))
        deleting_png_files(directory=directory)  # Удаление скаченного файла из папки
