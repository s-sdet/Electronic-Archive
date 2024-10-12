import pytest
from pytest_testrail.plugin import pytestrail
from api.data.constants import DocumentTypeNotice
from api.fixtures.document.filter.filter import Filter


class TestsFindDocument:
    """Тесты поиска документов."""
    doc_type = DocumentTypeNotice()

    @pytestrail.case("C21107758")
    def test_search_doc_by_one_metadata_type(self, app, auth, metadata_type="Number", metadata_type_value=12000):
        """Тест поиска документа по одному типу метаданных."""
        # Создание типа документа
        doc_type = app.doc_type.create_doc_type(
            header=auth, data=app.doc_type.data_to_create_document_type_with_metadata_type(
                is_required=False, metadata_type_name=metadata_type, display_name="Номер", metadata_type=metadata_type))

        # Создание документа с типом метаданных Number
        doc = app.doc.create_document(
            header=auth, data=app.doc.data_for_creating_document_with_required_metadata_type(
                doc_type_id=doc_type["result"]["id"], name="Док", metadata_type=metadata_type,
                metadata_type_value=metadata_type_value))

        # Поиск документа
        search = app.filter.find_document(header=auth, data=app.filter.data_for_search_doc_by_filter(
            doc_type_ids=doc_type["result"]["id"], properties_type=metadata_type,
            properties_value=f"{metadata_type_value}"))
        assert search["result"]["documents"][0]["id"] == doc["result"]["documentVersionId"]
        assert search["result"]["documents"][0]["documentId"] == doc["result"]["documentId"]
        assert search["result"]["documents"][0]["documentTypeId"] == doc_type["result"]["id"]

    @pytestrail.case("C21704388")
    def test_checking_flag_for_existence_the_next_page_is_true(self, app, auth, doc_type_without_file_type):
        """Тест проверки на существование следующей страницы == True."""
        # Создание 21 документа с типом метаданных Number
        for _ in range(21):
            app.doc.create_document(
                header=auth, data=app.doc.data_for_creating_document_with_required_metadata_type(
                    doc_type_id=doc_type_without_file_type["result"]["id"]))

        # Поиск документа
        search = app.filter.find_document(header=auth, data=app.filter.data_for_search_doc_by_filter_page_number(
            doc_type_ids=doc_type_without_file_type["result"]["id"]))
        assert search["result"]["hasNextPage"] is True

    @pytestrail.case("C21115525")
    def test_search_document_by_2_doc_types_and_one_metadata_type(self, app, auth, metadata_type="Number",
                                                                  metadata_type_value=12000):
        """Тест поиска документа по 2 типам документа и по ОДНОМУ типу метаданных."""

        # Создание двух типов документа
        first_doc_type, second_doc_type = (app.doc_type.create_doc_type(
            header=auth, data=app.doc_type.data_to_create_document_type_with_metadata_type(
                doc_type_name=self.doc_type.doc_type_name_latin, is_required=False, metadata_type_name=metadata_type,
                display_name="Номер", metadata_type=metadata_type))
            for _ in range(2))

        # Создание двух документов с типом метаданных Number
        first_doc, second_doc = (app.doc.create_document(
            header=auth, data=app.doc.data_for_creating_document_with_required_metadata_type(
                doc_type_id=first_doc_type["result"]["id"], name="Док1", metadata_type=metadata_type,
                metadata_type_value=metadata_type_value))
            for _ in range(2))

        # Поиск документа
        search = app.filter.find_document(header=auth, data=app.filter.data_for_search_doc_by_two_doc_type_id(
            first_doc_type=first_doc_type["result"]["id"], second_doc_type=second_doc_type["result"]["id"],
            properties_type=metadata_type, properties_value=f"{metadata_type_value}"))

        # Обработка исключения добавлена по причине отсутствия сортировки документов json
        try:
            assert search["result"]["documents"][0]["id"] == first_doc["result"]["documentVersionId"]
            assert search["result"]["documents"][0]["documentId"] == first_doc["result"]["documentId"]
            assert search["result"]["documents"][0]["documentTypeId"] == first_doc_type["result"]["id"]
        except AssertionError:
            assert search["result"]["documents"][0]["id"] == second_doc["result"]["documentVersionId"]
            assert search["result"]["documents"][0]["documentId"] == second_doc["result"]["documentId"]
            assert search["result"]["documents"][0]["documentTypeId"] == second_doc_type["result"]["id"]

    @pytestrail.case("C21107759")
    @pytest.mark.parametrize(
        "doc_type_name, name_first_system_file, display_name_first_system_file, first_file_type,"
        "name_second_system_file, display_name_second_system_file, second_file_type, regular_expression, expression,"
        "doc_name, first_metadata_type, first_metadata_type_value, second_metadata_type, second_metadata_type_value",
        Filter.DATA_FOR_DOCUMENT_TYPE_WITHOUT_FILE_TYPE_WITH_METADATA_TYPE)
    def test_search_doc_by_multiple_types_metadata(
            self, app, auth, doc_type_name, name_first_system_file, display_name_first_system_file, first_file_type,
            name_second_system_file, display_name_second_system_file, second_file_type, regular_expression, expression,
            doc_name, first_metadata_type, first_metadata_type_value, second_metadata_type, second_metadata_type_value):
        """Тест поиска документа по нескольким типам метаданных."""
        # Создание типа документа
        doc_type = app.doc_type.create_doc_type(
            header=auth, data=app.doc_type.data_for_create_document_type_with_two_type_metadata(
                doc_type_name=doc_type_name, name_first_system_file=name_first_system_file,
                display_name_first_system_file=display_name_first_system_file, first_file_type=first_file_type,
                name_second_system_file=name_second_system_file,
                display_name_second_system_file=display_name_second_system_file, second_file_type=second_file_type,
                regular_expression=regular_expression, expression=expression
            ))

        # Создание документа с типом метаданных Number
        doc = app.doc.create_document(
            header=auth, data=app.doc.data_for_creating_document_with_multiple_types(
                doc_type_id=doc_type["result"]["id"], name=doc_name, first_metadata_type=first_metadata_type,
                first_metadata_type_value=first_metadata_type_value, second_metadata_type=second_metadata_type,
                second_metadata_type_value=second_metadata_type_value))

        # Поиск документа
        search = app.filter.find_document(header=auth, data=app.filter.data_for_search_doc_by_two_properties(
            doc_type_ids=doc_type["result"]["id"]))
        assert search["result"]["documents"][0]["id"] == doc["result"]["documentVersionId"]
        assert search["result"]["documents"][0]["documentId"] == doc["result"]["documentId"]
        assert search["result"]["documents"][0]["documentTypeId"] == doc_type["result"]["id"]

    @pytestrail.case("C21115527")
    def test_search_document_by_invalid_value(self, app, auth, doc_type_without_file_type, api="api/v3.0/"):
        """Негативный тест поиска документа по неверному значению."""
        # Создание документа с api v3
        app.doc.create_document(url_api=api, header=auth, data=app.doc.data_for_creating_document_with_entities(
                doc_type_id=doc_type_without_file_type["result"]["id"]))

        # Поиск документа
        search = app.filter.find_document(header=auth, data=app.filter.data_for_search_doc_by_properties_filter(
            doc_type_ids=doc_type_without_file_type["result"]["id"]))
        assert search["result"]["count"] == 0

    @pytestrail.case("C21115616")
    @pytest.mark.parametrize("api, entity_type", [("api/v3.0/", "CreditDossier")])
    def test_search_document_by_invalid_value(self, app, auth, doc_type_without_file_type, api, entity_type):
        """Позитивный тест поиска документа без documentTypeIds по одному значению."""
        # Создание документа с api v3
        app.doc.create_document(url_api=api, header=auth, data=app.doc.data_for_creating_document_with_entities(
            doc_type_id=doc_type_without_file_type["result"]["id"], entity_type=entity_type))

        # Поиск документа
        search = app.filter.find_document(header=auth, data=app.filter.data_for_search_doc_without_doc_type())
        assert search["result"]["count"] != 0

    @pytestrail.case("C21115466", "C21641100", "C21115524")
    @pytest.mark.parametrize("name, is_required, metadata_type, display_name, metadata_type_value, status_code",
                             Filter.DATA_FOR__SEARCH_DOCUMENT_BY_VALUE_PROPERTY_SEARCH_TEXT)
    def test_search_document_by_value_property_search_text(self, app, auth, name, is_required, metadata_type,
                                                           display_name, metadata_type_value, status_code):
        """Тесты поиска документа по значению String и Number в свойствах документа "valuePropertySearchText"."""
        # Создание типа документа
        doc_type = app.doc_type.create_doc_type(
            header=auth, data=app.doc_type.data_to_create_document_type_with_metadata_type(
                doc_type_name=name, is_required=is_required, metadata_type_name=metadata_type,
                display_name=display_name,  metadata_type=metadata_type))
        # Создание документа с типом метаданных Number
        doc = app.doc.create_document(
            header=auth, data=app.doc.data_for_creating_document_with_required_metadata_type(
                doc_type_id=doc_type["result"]["id"], metadata_type=metadata_type,
                metadata_type_value=metadata_type_value))
        # Поиск документа
        search = app.filter.find_document(header=auth, data=app.filter.data_for_search_doc_by_value_property(
            doc_type_ids=doc_type["result"]["id"], doc_properties=str(metadata_type_value)), status_code=status_code)
        assert search["result"]["documents"][0]["id"] == doc["result"]["documentVersionId"]
        assert search["result"]["documents"][0]["documentId"] == doc["result"]["documentId"]
        assert search["result"]["documents"][0]["documentTypeId"] == doc_type["result"]["id"]

    @pytestrail.case("C21107764", "C21107765")
    @pytest.mark.parametrize("date_to", (None, "2024-01-05"))
    def test_search_document_by_modification_date(self, app, auth, date_to):
        """Тесты поиска документов по датам изменения."""
        search = app.filter.find_document(header=auth, data=app.filter.data_for_search_doc__by_modification_date(
            date_to=date_to
        ))
        assert search["result"]["count"] != 0
