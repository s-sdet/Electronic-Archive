import pytest
from pytest_testrail.plugin import pytestrail


class TestDownloadInstructions:
    """
    Тесты для скачивания файлов инструкций
    https://electronicarchive-frontend-afds.dev.akbars.ru/info?tab=Instructions
    """

    @pytest.mark.lp
    @pytestrail.case("C14989312")
    def test_download_instructions(self, app, go_to_instructions):
        """Тест скачивание инструкции."""
        app.instructions.download_file()
