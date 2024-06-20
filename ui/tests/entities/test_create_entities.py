from pytest_testrail.plugin import pytestrail
from ui.fixtures.pages.entities.entities import CreateEntitiesModel


class TestCreateEntities:
    """
    Тесты для создания документов
    https://electronicarchive-frontend-afds.dev.akbars.ru/entities/create
    """

    @pytestrail.case("C15723466")
    def test_create_entity(self, app, login_user, go_to_entities):
        """
        Тест создания сущности.
        :param go_to_entities: Переход в раздел Сущности.
        """
        data = CreateEntitiesModel.random_valid_data_for_entity()
        app.entities.fill_entity_type_creation_form(data=data)
