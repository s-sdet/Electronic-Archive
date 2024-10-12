from pytest_testrail.plugin import pytestrail


class TestsGraphicSign:
    """Тесты взаимодействия с графическими подписями на документах."""

    @pytestrail.case("C20479337")
    def test_setting_stamp_on_a_document(self, app, auth):
        """Тест добавления штампа на файл с расширением PDF."""
        res = app.graphic_sign.add_graphic_sign(data=app.graphic_sign.data_for_add_graphic_sign())
        assert res["content-type"] == "application/pdf"

    @pytestrail.case("C20479424")
    def test_invalid_setting_stamp_on_a_document(self, app, auth, specific_files="upload_file.png", status_code=400,
                                                 error="PDF files only"):
        """Негативный тест добавления штампа на файл с расширением != PDF."""
        res = app.graphic_sign.invalid_add_graphic_sign(data=app.graphic_sign.data_for_add_graphic_sign(),
                                                        specific_files=specific_files, status_code=status_code)
        assert res["error"] == error
