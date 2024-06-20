import pytest
from pytest_testrail.plugin import pytestrail
from api.fixtures.document_version.download_actual.download_actual import DownloadActual


class TestsDownloadActual:
    """Тесты скачивания файлов версий документов."""

    @pytest.mark.lp
    @pytestrail.case("C19136301", "C19136299", "C19136296", "C19128455")
    @pytest.mark.parametrize("doc_ver_id, api_version", DownloadActual.DATA_FOR_DOWNLOADING_FILE)
    def test_download_current_file_by_document_version_id(self, app, auth, doc_ver_id, api_version):
        """Тест скачивание актуального файла по id версии документа."""

        # Получение информации о версии документа
        get_info = app.download_actual.get_info_about_document_version(api_version=api_version, doc_ver_id=doc_ver_id)
        file_name = get_info['result']['files'][0]['name']  # Получение имени документа
        assert 'files' in get_info['result']

        # Установка актуальности 1 файла выбранной версии документа
        app.set_actual.make_file_current(api_version=api_version,
                                         file_id=get_info['result']['files'][0]['id'], is_actual=True)

        # Получение информации о файле
        app.file.get_information_about_file(api_version=api_version, file_id=get_info['result']['files'][0]['id'])
        assert get_info['result']['isActual'] is True

        # Скачивание актуального файла по id версии документа
        app.download_actual.download_file_by_doc_version_id(api_version=api_version, doc_ver_id=doc_ver_id,
                                                            is_inline=False, file_name=file_name)
