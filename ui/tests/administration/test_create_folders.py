import pytest
from pytest_testrail.plugin import pytestrail


class TestFolder:
    """
    Тесты для создания папок типов документов***
    """

    @pytest.mark.lp
    @pytestrail.case("C14985040")
    def test_create_folder(self, app, go_to_admin_panel, random_folder_name, random_group_name):
        """Тест создания папки для типов документа."""
        app.doc_type.open_form_to_create_folder()
        app.doc_type.data_entry_to_create_folder(folder_name=random_folder_name, group_name=random_group_name)
        app.doc_type.create_folder()

    @pytest.mark.lp
    @pytestrail.case("C14981822")
    def test_edit_folder(self, app, create_folder, random_second_group_name, random_new_folder_name):
        """Тест редактирования папки для типов документа."""
        app.doc_type.editing_folder(folder_name=create_folder)
        app.doc_type.add_second_group(second_group_name=random_second_group_name)
        app.doc_type.save_folder()
        app.doc_type.editing_folder(folder_name=create_folder)
        app.doc_type.rename_folder(new_folder_name=random_new_folder_name)
        app.doc_type.save_folder()
        app.doc_type.editing_folder(folder_name=random_new_folder_name)
        app.doc_type.checking_change_history(second_group_name=random_second_group_name)
