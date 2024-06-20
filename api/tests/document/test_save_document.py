import pytest
from pytest_testrail.plugin import pytestrail
from api.fixtures.document.document import Document
from api.fixtures.document_type.document_type import DocumentType
from api.fixtures.assertions import Assertions
from api.fixtures.file.file import File
from api.data.constants import ApiVersions, DocumentTypeNotice, DocumentNotice


class TestsSaveDocument:
    """Тесты сохранения/создания документов."""

    doc_type = DocumentTypeNotice()

    @pytest.mark.lp
    @pytestrail.case("C17499110")
    def test_save_document_and_version_with_additional_metadata(self, app, auth):
        """Тест сохранения документа и версии с указанием дополнительных метаданных."""
        res = app.doc.save_document(
            url_api=Document.URL_API_V3_DOCUMENT,
            header=auth,
            data=Document.json_data_for_saving_document()
        )
        Assertions.assert_successful_saving_document(res=res)

        # Проверка отображения метаданных ВЕРСИИ документа в ответе на запрос на выдачу информации о документе
        res_doc_id = app.doc.get_data_by_document_id(
            url_api=Document.URL_API_V3_DOCUMENT,
            doc_id=res['result']['documentId']
        )
        Assertions.assert_metadata_by_document_id(res=res, res_doc_id=res_doc_id)

        # Проверка отображения метаданных ВЕРСИИ документа в ответе на запрос на выдачу информации о ВЕРСИИ документа
        res_doc_ver_id = app.doc.get_data_by_document_version_id(
            url_api=Document.URL_API_V3_DOCUMENT_VERSION_ID,
            doc_ver_id=res['result']['documentVersionId']
        )
        Assertions.assert_metadata_by_document_version_id(res=res, res_doc_ver_id=res_doc_ver_id)

    @pytest.mark.lp
    @pytestrail.case("C19002138", "C18986124")
    @pytest.mark.parametrize("api_file, api_doc", [("api/v2.0/", "api/v2.0/Document/"),
                                                   ("api/v3.0/", "api/v3.0/Document/")])
    def test_upload_file_and_save_document_with_version_and_additional_metadata(self, app, auth, api_file, api_doc):
        """
        Тест сохранения документа и версии с прикреплением файлов, указанием дат начала и окончания действия и
        указанием дополнительных метаданных.
        :param api_file: Версия API файла;
        :param api_doc: Версия API документа;
        """

        # Загрузка файла в систему
        file = app.file.upload_files(api_version=api_file, quantity_files=1,
                                     data=File.data_upload_file_with_calculate_hash_and_document_typeid(
                                         calculate_hash=True))

        # Создание документа и его версии с указанием id загруженного в систему файла, дополнительных метаданных,
        # дат добавления документа и версии в систему-источник и даты окончания действия
        create_doc = app.doc.save_document(
            data=app.doc.data_for_creating_document_indicating_file_id(file_id=file["result"]["files"][0]["id"]),
            url_api=api_doc)
        Assertions.assert_successful_saving_document(res=create_doc)

        # Получение и проверка информации о созданной версии документа
        version = app.doc_ver.get_info_about_document_version(api_version=api_file,
                                                              doc_ver_id=create_doc["result"]["documentVersionId"])
        Assertions.assertion_metadata_about_document_version(res=version, file=file)

        # Получение и проверка информации о созданном документе
        document = app.doc.get_doc_info_by_doc_id(api_version=api_file, doc_id=create_doc["result"]["documentId"])
        Assertions.assertion_metadata_about_document(res=document, file=file)

    @pytest.mark.lp
    @pytestrail.case("C19709330")
    def test_creating_document_and_3_versions_with_attach_3_files(self, app, auth, api_version=Document.API_V3,
                                                                  doc_type_id="9d833179-a681-7fbc-63c5-019e1e95a967"):
        """
        Тест создания документа, 3 версий с прикреплением 3 файлов и передаче id типа документа
        :param api_version: Версия API;
        :param doc_type_id: Тестовый тип документа с файлами в каждом документе;
        """

        # Загрузка 3 разных файлов с указанием типа документа
        file = app.file.upload_files(api_version=api_version, quantity_files=3,
                                     data=File.data_upload_file_with_calculate_hash_and_document_typeid(
                                         calculate_hash=True, doc_type_id=doc_type_id))
        Assertions.assertion_download_3_files(res=file)

        # Получение информации о каждом созданном документе и его созданной версии, передавая id созданных документов
        for num in range(0, 3):
            doc = app.doc.get_doc_info_by_doc_id(api_version=api_version,
                                                 doc_id=file["result"]["files"][num]["documentId"])
            Assertions.assertion_information_about_created_document_and_its_version(doc=doc, file=file,
                                                                                    doc_type_id=doc_type_id, num=num)

    @pytest.mark.lp
    @pytestrail.case("C19709326")
    def test_creating_document_and_its_version_with_attach_1_file(self, app, auth, api_version=Document.API_V3,
                                                                  doc_type_id="9d833179-a681-7fbc-63c5-019e1e95a967"):
        """
        Тест создания документа, его версий с прикреплением 1 файла и передаче id типа документа
        :param api_version: Версия API;
        :param doc_type_id: Тестовый тип документа с файлами в каждом документе;
        """

        # Загрузка файла с указанием типа документа
        file = app.file.upload_files(api_version=api_version, quantity_files=1,
                                     data=File.data_upload_file_with_calculate_hash_and_document_typeid(
                                         calculate_hash=True, doc_type_id=doc_type_id))
        Assertions.assertion_download_file(res=file)

        # Получение информации о созданном документе, его созданной версии, передав id созданного документа
        doc = app.doc.get_doc_info_by_doc_id(api_version=api_version, doc_id=file["result"]["files"][0]["documentId"])
        Assertions.assertion_information_about_created_document_and_its_version(doc=doc, file=file,
                                                                                doc_type_id=doc_type_id, num=0)

    @pytestrail.case("C17498614")
    def test_creating_document_and_version_with_expire_date(self, app, auth):
        """Тест успешного создания документа и версии с указанием даты окончания действия."""
        create_doc = app.doc.create_document(url_api=ApiVersions.API_V3,
                                             data=Document.data_for_creating_document_whit_expire_date(
                                                 doc_type_id=DocumentTypeNotice.DOC_TYPE_ID,
                                                 expire_date=DocumentTypeNotice.EXPIRE_DATE))
        Assertions.assert_successful_saving_document(res=create_doc)

        # Проверка отображение id созданного документа к версии в ответе на запрос выдачи информации о версии документе
        get_doc_ver = app.doc_ver.get_info_about_document_version(api_version=ApiVersions.API_V3,
                                                                  doc_ver_id=create_doc["result"]["documentVersionId"])
        assert get_doc_ver["result"]["id"] == create_doc["result"]["documentVersionId"]
        assert get_doc_ver["result"]["expireDate"] == DocumentTypeNotice.EXPIRE_DATE

        # Проверка отображение даты окончания действия ВЕРСИИ документа в ответе на запрос выдачи информации о документе
        get_doc = app.doc.get_doc_info_by_doc_id(api_version=ApiVersions.API_V3,
                                                 doc_id=create_doc["result"]["documentId"])
        assert get_doc["result"]["documentVersions"][0]["expireDate"] == DocumentTypeNotice.EXPIRE_DATE

    @pytestrail.case("C17499125")
    @pytest.mark.xfail(reason="Ожидаемый 400. Связанно с багом LP-1331.")
    def test_creating_document_and_its_version_with_an_end_date_earlier_than_current_date(self, app, auth):
        """
        Негативный тест отображения ошибки при сохранении документа и версии с датой окончания действия РАНЕЕ
        текущей даты.
        """
        app.doc.create_document(response=400, url_api=ApiVersions.API_V3,
                                data=Document.data_for_creating_document_whit_expire_date(
                                    doc_type_id=DocumentTypeNotice.DOC_TYPE_ID,
                                    expire_date=DocumentTypeNotice.EXPIRE_DATE))

    @pytestrail.case("C17499129")
    @pytest.mark.xfail(reason="Ожидаемый 400. Связанно с багом LP-1331.")
    def test_creating_document_and_its_version_with_a_creation_date_earlier_than_current_date(self, app, auth):
        """
        Негативный тест отображения ошибки при сохранении документа и версии с датой создания в системе-источнике
        РАНЕЕ текущей даты.
        """
        app.doc.create_document(response=400, url_api=ApiVersions.API_V3,
                                data=Document.data_for_creating_document_whit_source_date(
                                    doc_type_id=DocumentTypeNotice.DOC_TYPE_ID,
                                    source_date=DocumentTypeNotice.SOURCE_DATE))

    @pytestrail.case("C17499118")
    def test_creating_document_and_version_with_creation_source_date_in_source_system(self, app, auth):
        """Успешное создания документа и версии с указанием даты создания в системе-источнике."""
        res = app.doc.create_document(url_api=ApiVersions.API_V3,
                                      data=Document.data_for_creating_document_whit_source_date(
                                          doc_type_id=DocumentTypeNotice.DOC_TYPE_ID,
                                          source_date=DocumentTypeNotice.SOURCE_DATE))
        Assertions.assert_successful_saving_document(res=res)

        # Получение информации о версии созданного документа по ID версии созданного документа
        get_doc_ver = app.doc_ver.get_info_about_document_version(api_version=ApiVersions.API_V3,
                                                                  doc_ver_id=res['result']['documentVersionId'])
        # Проверка id созданного документа и даты к версии на запрос получения информации о ВЕРСИИ документа
        assert get_doc_ver["result"]["id"] == res["result"]["documentVersionId"]
        assert get_doc_ver["result"]["sourceDate"] == DocumentTypeNotice.SOURCE_DATE

        # Получение информации о созданном документа по ID созданного документа
        get_doc_info = app.doc.get_doc_info_by_doc_id(api_version=ApiVersions.API_V3,
                                                      doc_id=res["result"]["documentId"])
        # Проверка даты создания в системе-источнике версии документа на запрос информации о документе
        assert get_doc_info["result"]["documentVersions"][0]["sourceDate"] == DocumentTypeNotice.SOURCE_DATE

    @pytestrail.case("C17499133")
    def test_creating_document_and_its_version_indicating_existing_files_in_system(self, app, auth):
        """
        Тест создания документа и его версии с указанием существующих в системе файлов с типом файлов для данного
        типа документов.
        """
        # Загрузка трех файлов с вычислением хеша файлов и без указания ID типа документа.
        files = app.file.upload_files(api_version=ApiVersions.API_V3, quantity_files=3,
                                      data=File.data_upload_file_with_calculate_hash(calculate_hash=True))

        # Создание документа и его версии с указанием загруженных ранее в систему файлов.
        doc = app.doc.create_document(url_api=ApiVersions.API_V3,
                                      data=Document.data_for_creating_document_and_its_version_with_id_files_in_system(
                                          doc_type_id=DocumentNotice.DOC_TYPE_ID,
                                          first_file=files["result"]["files"][0]["id"],
                                          second_file=files["result"]["files"][1]["id"],
                                          third_file=files["result"]["files"][2]["id"]))
        # Проверка присвоения id документа, id версии документа, присвоение номера версии документа равного 1.
        Assertions.assert_successful_saving_document(res=doc)

        # Проверка ID прикрепленных файлов данной версии документа в ответе на запрос на выдачи информации о документе.
        doc_info = app.doc.get_doc_info_by_doc_id(api_version=ApiVersions.API_V3, doc_id=doc["result"]["documentId"])
        Assertions.assertion_id_uploaded_files_is_equal_id_files_in_document(res=doc_info)

        # Проверка отображение id созданного документа к версии в ответе на выдачу информации о версии документа
        get_doc_ver = app.doc_ver.get_info_about_document_version(api_version=ApiVersions.API_V3,
                                                                  doc_ver_id=doc["result"]["documentVersionId"])
        Assertions.assertion_id_uploaded_files_is_equal_id_files_in_document_version(res=get_doc_ver, doc=doc)

    @pytestrail.case("C20771031", "C20771032", "C20771033", "C20771034", "C20771035")
    @pytest.mark.parametrize("doc_type_name, metadata_type_name, display_name, metadata_type, doc_name, "
                             "doc_metadata_type, metadata_type_value, regular_expression, regular_expression_value",
                             Document.DATA_FOR_CREATE_DOCUMENT_WITH_REQUIRED_METADATA_TYPE)
    def test_create_document_with_required_metadata_type(self, app, auth, doc_type_name, metadata_type_name,
                                                         display_name, metadata_type, doc_name, doc_metadata_type,
                                                         metadata_type_value, regular_expression,
                                                         regular_expression_value):
        """
        Тесты на создание документов с обязательным типом метаданных:
        "C20771031" - обязательный тип метаданных Number;
        "C20771032" - обязательный тип метаданных DateTime;
        "C20771033" - обязательный тип метаданных string_1 (регулярное выражение с числами);
        "C20771034" - обязательный тип метаданных String (регулярное выражение почта);
        "C20771035" - обязательный тип метаданных Boolean;
        """
        doc_type = app.doc_type.create_doc_type(url_api=ApiVersions.API_V4, header=auth,
                                                data=DocumentType.data_to_create_document_type_with_metadata_type(
                                                    doc_type_name=doc_type_name, metadata_type_name=metadata_type_name,
                                                    display_name=display_name, metadata_type=metadata_type,
                                                    regular_expression=regular_expression,
                                                    regular_expression_value=regular_expression_value
                                                ))
        doc = app.doc.create_document(url_api=ApiVersions.API_V4, header=auth,
                                      data=Document.data_for_creating_document_with_required_metadata_type(
                                          doc_type_id=doc_type["result"]["id"], name=doc_name,
                                          metadata_type=doc_metadata_type, metadata_type_value=metadata_type_value))
        assert "documentId" and "documentVersionId" in doc["result"]
        assert doc["result"]["name"] == doc_name

    @pytestrail.case("C20771030")
    @pytest.mark.parametrize("doc_type_name, doc_name, metadata_type, metadata_type_value",
                             Document.DATA_FOR_CREATE_DOCUMENT_WITHOUT_FILE_TYPE_AND_METADATA_TYPE)
    def test_create_document_with_document_type_without_file_type_and_metadata_type(self, app, auth, doc_type_name,
                                                                                    doc_name, metadata_type,
                                                                                    metadata_type_value):
        """Тест создания документа с указанием типа документа без типа файла и типа метаданных."""
        doc_type = app.doc_type.create_doc_type(url_api=ApiVersions.API_V4, header=auth,
                                                data=DocumentType.data_for_create_document_type_without_metadata_type(
                                                    doc_type_name=doc_type_name))
        doc = app.doc.create_document(header=auth,
                                      data=Document.data_for_creating_document_with_required_metadata_type(
                                          doc_type_id=doc_type["result"]["id"], name=doc_name,
                                          metadata_type=metadata_type, metadata_type_value=metadata_type_value))
        assert "documentId" and "documentVersionId" in doc["result"]
        assert doc["result"]["name"] == doc_name
