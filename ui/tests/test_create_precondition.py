from ui.data.constants import DocumentNotice


class TestCreatePrecondition:
    """
    Тесты для создания сущностей перед прогоном тестов***
    """

    def test_create_doc_type_ea_123(self, app, go_to_admin_panel):
        """Создание типа документа 'ЭА 123'."""
        app.precondition.open_form_doc_type_create()
        app.precondition.data_entry_doc_type(doc_type_name=DocumentNotice.DOCUMENT_TYPE_EA_123)
        app.precondition.creation_type()

    def test_create_doc_type_with_2_fields(self, app, go_to_admin_panel):
        """Создание типа документа 'Тестовый тип документа с 2 дополнительными полями'."""
        pass

    def test_create_doc_type_ea_passport_rf(self, app, go_to_admin_panel):
        """Создание типа документа 'ЭА Паспорт гражданина РФ'."""
        pass

    def test_create_doc_type_with_different_extensions(self, app, go_to_admin_panel):
        """Создание типа документа 'Тип документа с разными расширениями'."""
        pass
