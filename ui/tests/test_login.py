import pytest
from pytest_testrail.plugin import pytestrail


class TestLoginPage:
    """
    Тесты для страницы авторизации ***
    Авторизация осуществляется через ***
    """

    @pytest.mark.lp
    @pytestrail.case("C17602758")
    def test_login_moffice(self, app, open_login_page):
        """Тест авторизации с валидными данными в домене MOFFICE."""
        app.login.entry_data_authorization()
        app.login.assertion_opening_search_page()
        app.login.assertion_user_name()

    @pytest.mark.lp
    @pytestrail.case("C15755533")
    def test_logout_from_live_space_panel(self, app, login_user, go_to_entities):
        """Тест логаута из аккаунта и возврата на ту же страницу после повторной авторизации."""
        app.login.logout_from_live_space_panel()
        app.login.entry_data_authorization()  # Повторная авторизация
        app.login.assertion_opening_search_page()
