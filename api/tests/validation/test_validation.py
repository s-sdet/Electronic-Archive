import pytest
from pytest_testrail.plugin import pytestrail
from api.fixtures.assertions import Assertions
from api.data.constants import ValidationNotice, ApiVersions, DocumentTypeNotice
from api.fixtures.validation.validation import Validation


class TestsValidation:
    """Тесты для валидации данных документов."""

    doc_type = DocumentTypeNotice()

    @pytestrail.case("C18759503", "C18759505", "C18759512", "C18759514")
    @pytest.mark.parametrize("doc_type_id, okz_number, url, method", Validation.DATA_FOR_CHECKING_FIELD_LENGTH)
    def test_add_invalid_application_number(self, app, auth, doc_type_id, okz_number, url, method):
        """Тест добавление невалидных данных в поле "№ заявки АС ОКЗ" более 64 символов."""
        res = app.validation.add_data(
            method=method,
            url_api=ApiVersions.API_V2,
            url=url,
            header=auth,
            data=Validation.data_credit_dossier(doc_type_id=doc_type_id, okz_number=okz_number),
            response=400
        )
        assert res['error'] == ValidationNotice.ERROR

    @pytestrail.case("C17606508")
    def test_creation_document_without_document_type(self, app, auth):
        """Тест создания документа без типа документа."""
        res = app.validation.add_data(
            url_api=ApiVersions.API_V3,
            url="Document",
            header=auth,
            data=Validation.data_without_document_type_key(),
            response=400
        )
        assert res['error'] == ValidationNotice.ERROR_DOC_TYPE

    @pytestrail.case("C17682364")
    def test_creation_document_without_value_document_type(self, app, auth):
        """Тест создания документа без значения типа документа."""
        res = app.validation.add_data(
            url_api=ApiVersions.API_V3,
            url="Document",
            header=auth,
            data=Validation.data_without_document_type_value(),
            response=400
        )
        assert res['error'] == ValidationNotice.ERROR_DOC_TYPE

    @pytestrail.case("C17562791")
    def test_get_information_without_value_document_id(self, app, auth):
        """Тест получение информации без передачи значения ключа ID документа."""
        res = app.validation.get_info(
            url_api=ApiVersions.API_V3,
            url="Document/Download",
            header=auth,
            data=Validation.data_without_document_id_value(),
            response=400
        )
        assert res['error'] == ValidationNotice.ERROR_DOC_ID

    @pytestrail.case("C18436744", "C18436745", "C18436746", "C18436747")
    @pytest.mark.parametrize("doc_type_name, url", Validation.VALID_DOCUMENT_TYPE_NAME_LENGTH)
    def test_valid_checking_length_of_document_type_name(self, app, auth, doc_type_name, url):
        """Позитивные тесты на проверку длинны названия типа документа менее 64 символов."""
        res = app.doc_type.create_doc_type(
            url_api=ApiVersions.API_V4,
            url=url,
            header=auth,
            data=Validation.creating_document_type(doc_type_name=doc_type_name)
        )
        Assertions.assertion_creation_document_type(res=res)

    @pytestrail.case("C18437357", "C18437356")
    @pytest.mark.parametrize("doc_type_name, file_name, url", Validation.VALID_FILE_TYPE_NAME_LENGTH)
    def test_valid_checking_length_for_file_type_name(self, app, auth, doc_type_name, file_name, url):
        """Позитивные тесты на проверку длинны названия для типов файла менее 64 символов."""
        res = app.doc_type.create_doc_type(
            url_api=ApiVersions.API_V4,
            url=url,
            header=auth,
            data=Validation.creating_document_type(doc_type_name=doc_type_name,
                                                   file_name=file_name)
        )
        Assertions.assertion_creation_document_type(res=res)

    @pytestrail.case("C18637145", "C18637146")
    @pytest.mark.parametrize("api_ver, doc_type_name, file_name, extensions, url",
                             Validation.VALID_DATA_ALLOWED_EXTENSIONS)
    def test_valid_checking_allowed_extensions(self, app, auth, api_ver, doc_type_name, file_name, extensions, url):
        """
        Позитивные тесты на проверку поля "Возможные расширения" для типа файла.
         Кейс "C18637145": "allowedExtensions" латиница и цифры до 10 знаков;
         Кейс "C18637146": "allowedExtensions" < 64 букв латиницы;
        """
        res = app.doc_type.create_doc_type(
            url_api=api_ver,
            url=url,
            header=auth,
            data=Validation.creating_document_type(doc_type_name=doc_type_name, file_name=file_name,
                                                   extensions=extensions)
        )
        Assertions.assertion_creation_document_type(res=res)

    @pytestrail.case("C18637141")
    def test_update_allowed_extensions_in_document_type(self, app, auth, create_document_type):
        """Тест обновления поля "Возможные расширения" для типа документа валидными значениями."""
        res = app.doc_type.update_data(
            url_api=ApiVersions.API_V4,
            header=auth,
            data=Validation.update_document_type(doc_type_id=create_document_type["result"]["id"])
        )
        assert res["success"] is True

    @pytestrail.case("C18475402")
    def test_update_name_in_document_type(self, app, auth, create_document_type, name=doc_type.doc_type_name_latin):
        """Тест обновления поля "Название типа документа" для типа документа валидными значениями."""
        res = app.doc_type.update_data(
            url_api=ApiVersions.API_V4,
            header=auth,
            data=Validation.update_document_type(doc_type_id=create_document_type["result"]["id"], doc_type_name=name)
        )
        assert res["success"] is True

    @pytestrail.case("C18524890", "C18504519")
    @pytest.mark.parametrize("api_ver, doc_type_name, file_type_name, url", Validation.VALID_DATA_FILE_TYPE_NAME)
    def test_update_name_in_file_type(self, app, auth, create_document_type, api_ver, doc_type_name, file_type_name,
                                      url):
        """
        Тесты обновления поля "Название для типа файла" для типа документа валидными значениями.
         Кейс "C18524890": обновлении в поле fileTypes.name буквами латиницы;
         Кейс "C18504519": обновлении в поле fileTypes.name буквами кириллицы;
        """
        res = app.doc_type.update_data(
            url_api=api_ver,
            url=url,
            header=auth,
            data=Validation.update_document_type(doc_type_id=create_document_type["result"]["id"],
                                                 doc_type_name=doc_type_name,
                                                 file_type_name=file_type_name)
        )
        assert res["success"] is True

    @pytestrail.case("C17888224", "C17888229", "C17888231")
    @pytest.mark.parametrize("api_ver, doc_type_name, system_type_name, file_type_name, url, error_text",
                             Validation.INVALID_DATA_SYSTEM_TYPE_NAME)
    def test_invalid_system_type_name(self, app, auth, api_ver, doc_type_name, system_type_name, file_type_name, url,
                                      error_text):
        """Невалидные тесты на валидацию поля Системное название типа."""
        res = app.doc_type.create_doc_type(
            url_api=api_ver,
            url=url,
            header=auth,
            data=Validation.creating_document_type(doc_type_name=doc_type_name, system_type_name=system_type_name,
                                                   file_name=file_type_name),
            response=400
        )
        assert res["errorDetails"]["properties[0].name"][0] == error_text

    @pytestrail.case("C17916516", "C18004736", "C18004740")
    @pytest.mark.parametrize("api_ver, doc_type_name, display_name, file_type_name, url, error_text",
                             Validation.INVALID_DATA_DISPLAY_NAME)
    def test_invalid_display_name(self, app, auth, api_ver, doc_type_name, display_name, file_type_name, url,
                                  error_text):
        """Невалидные тесты на проверку поля Отображаемое название."""
        res = app.doc_type.create_doc_type(
            url_api=api_ver,
            url=url,
            header=auth,
            data=Validation.creating_document_type(doc_type_name=doc_type_name, display_name=display_name,
                                                   file_name=file_type_name),
            response=400
        )
        assert res["errorDetails"]["properties[0].displayName"][0] == error_text

    @pytestrail.case("C18436748", "C18436749", "C18004616", "C18005257")
    @pytest.mark.parametrize("api_ver, doc_type_name, file_type_name, url, error_text",
                             Validation.INVALID_DOCUMENT_TYPE_NAME)
    def test_invalid_document_type_name(self, app, auth, api_ver, doc_type_name, file_type_name, url, error_text):
        """Невалидные тесты на проверку поля Название типа документа."""
        res = app.doc_type.create_doc_type(
            url_api=api_ver,
            url=url,
            header=auth,
            data=Validation.creating_document_type(doc_type_name=doc_type_name, file_name=file_type_name),
            response=400
        )
        assert res["errorDetails"]["name"][0] == error_text

    @pytestrail.case("C18437355", "C18005493", "C18005498")
    @pytest.mark.parametrize("api_ver, doc_type_name, file_type_name, url, error_text",
                             Validation.INVALID_FILE_TYPE_NAME)
    def test_invalid_file_type_name(self, app, auth, api_ver, doc_type_name, file_type_name, url, error_text):
        """Невалидные тесты на проверку поля Название для типа файла."""
        res = app.doc_type.create_doc_type(
            url_api=api_ver,
            url=url,
            header=auth,
            data=Validation.creating_document_type(doc_type_name=doc_type_name, file_name=file_type_name),
            response=400
        )
        assert res["errorDetails"]["fileTypes[0].name"][0] == error_text

    @pytestrail.case("C18005504", "C18005507", "C18005508", "C18005509")
    @pytest.mark.parametrize("api_ver, doc_type_name, file_type_name, extensions, url, error_text",
                             Validation.INVALID_ALLOWED_EXTENSIONS)
    def test_invalid_allowed_extensions(self, app, auth, api_ver, doc_type_name, file_type_name, extensions, url,
                                        error_text):
        """Невалидные тесты на проверку поля Возможные расширения."""
        res = app.doc_type.create_doc_type(
            url_api=api_ver,
            url=url,
            header=auth,
            data=Validation.creating_document_type(doc_type_name=doc_type_name, file_name=file_type_name,
                                                   extensions=extensions),
            response=400
        )
        assert res["errorDetails"]["fileTypes[0].allowedExtensions[0]"][0] == error_text
