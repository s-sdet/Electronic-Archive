import logging
from api.fixtures.file.file import File
from api.fixtures.document.document import Document
from api.fixtures.document_version.document_version import DocumentVersion


class Assertions:
    """Проверки нужный полей после создания, сохранения, удаления документов."""

    @staticmethod
    def assert_successful_saving_document(res=None):
        """Проверка значений в теле ответа после сохранения документа."""
        assert isinstance(res['result']['documentId'], str) is True  # Значение 'documentId' == строка
        assert isinstance(res['result']['documentVersionId'], str) is True   # Значение 'documentVersionId' == строка
        assert res['result']['version'] == 1  # Номер версии созданного документа == 1

    @staticmethod
    def assert_metadata_by_document_id(res=None, res_doc_id=None):
        """Проверка метаданных версии документа в ответе на запрос выдачи информации о документе."""
        assert res['result']['documentId'] == res_doc_id['result']['id']
        assert res_doc_id['result']['documentVersions'][0]['documentProperties'] == \
               Document.json_data_for_saving_document()['documentProperties']

    @staticmethod
    def assert_metadata_by_document_version_id(res=None, res_doc_ver_id=None):
        """Проверка метаданных версии документа в ответе на запрос выдачи информации о версии документа."""
        assert res['result']['documentVersionId'] == res_doc_ver_id['result']['id']
        assert res_doc_ver_id['result']['documentProperties'] == Document.json_data_for_saving_document()[
            'documentProperties']

    @staticmethod
    def assert_actual_version_document_by_document_id(res=None, res_act_ver=None):
        """Проверка получения актуальной версии документа по document ID после его создания."""
        assert res_act_ver['result']['id'] == res['result']['documentVersionId']
        assert res_act_ver['result']['documentId'] == res['result']['documentId']
        assert res_act_ver['result']['version'] == res['result']['version']
        assert res_act_ver['result']['expireDate'] == \
               Document.for_saving_document_with_date()['expireDate']
        assert res_act_ver['result']['sourceDate'] == \
               Document.for_saving_document_with_date()['sourceDate']
        assert res_act_ver['result']['documentProperties'] == \
               Document.for_saving_document_with_date()['documentProperties']
        assert res_act_ver['result']['files'] == \
               Document.for_saving_document_with_date()['files']

    @staticmethod
    def assert_document_version_information(document=None, document_version=None, info_version=None):
        """Проверка информации о версии документа."""
        assert info_version['result']['id'] == document_version['result']['id']
        assert info_version['result']['documentId'] == document['result']['documentId']
        assert info_version['result']['version'] == 2
        assert info_version['result']['expireDate'] == DocumentVersion.for_creating_minor_version()['expireDate']
        assert info_version['result']['sourceDate'] == DocumentVersion.for_creating_minor_version()['sourceDate']
        assert info_version['result']['documentProperties'] == \
               DocumentVersion.for_creating_minor_version()['documentProperties']
        assert info_version['result']['createdByUserId'] is not None
        assert info_version['result']['files'] == DocumentVersion.for_creating_minor_version()['files']

    @staticmethod
    def assert_search_document_type_by_document_name(res=None, name=None):
        """
        Проверка поиска типа документа по части названия типа документа:
            1. Проверяем связан ли тип документа с какой-либо папкой;
            2. Проверяем есть ли нужные символы в названии документа.
        """
        for key in res['result']['data']:
            if key['parentFolderId'] is None:
                assert name in key['name'].lower()
                logging.info(f"Документ {key['name']} связан с какой-либо папкой")
            else:
                assert name in key['name'].lower()
                logging.info(f"Документ {key['name']} не связан с какой-либо папкой")

    @staticmethod
    def assert_get_document_ist_versions_files_by_document_id(document=None, first_doc_ver=None, second_doc_ver=None,
                                                              get_doc=None, create_document_type=None):
        """Проверка получения документа со списком его версий и файлов по documentId"""
        assert get_doc['result']['id'] == document['result']['documentId']
        assert get_doc['result']['documentVersions'][0]['documentId'] == document['result']['documentId']
        assert get_doc['result']['documentVersions'][1]['documentId'] == document['result']['documentId']
        assert get_doc['result']['documentVersions'][2]['documentId'] == document['result']['documentId']
        assert get_doc['result']['documentTypeId'] == create_document_type["result"]["id"]
        assert get_doc['result']['name'] is None
        assert 'createdByUserId' in get_doc['result']
        assert get_doc['result']['documentVersions'][0]['id'] == second_doc_ver['result']['id']
        assert get_doc['result']['documentVersions'][1]['id'] == first_doc_ver['result']['id']
        assert get_doc['result']['documentVersions'][2]['id'] == document['result']['documentVersionId']
        assert get_doc['result']['documentVersions'][0]['version'] == 3
        assert get_doc['result']['documentVersions'][1]['version'] == 2
        assert get_doc['result']['documentVersions'][2]['version'] == 1
        assert get_doc['result']['documentVersions'][0]['expireDate'] == "2023-08-07T09:18:17.4770000"
        assert get_doc['result']['documentVersions'][1]['expireDate'] == "2023-08-07T09:18:17.4770000"
        assert get_doc['result']['documentVersions'][2]['expireDate'] == "2023-08-07T11:00:46.1310000"
        assert get_doc['result']['documentVersions'][0]['sourceDate'] == "2023-08-07T09:18:17.4770000"
        assert get_doc['result']['documentVersions'][1]['sourceDate'] == "2023-08-07T09:18:17.4770000"
        assert get_doc['result']['documentVersions'][2]['sourceDate'] == "2023-08-07T11:00:46.1310000"
        assert get_doc['result']['documentVersions'][0]['isActual'] is True
        assert get_doc['result']['documentVersions'][1]['isActual'] is False
        assert get_doc['result']['documentVersions'][2]['isActual'] is False
        assert get_doc['result']['documentVersions'][0]['documentProperties'] == {}
        assert get_doc['result']['documentVersions'][1]['documentProperties'] == {}
        assert get_doc['result']['documentVersions'][2]['documentProperties'] == {}
        assert get_doc['result']['documentVersions'][0]['files'] == []
        assert get_doc['result']['documentVersions'][1]['files'] == []
        assert get_doc['result']['documentVersions'][2]['files'] == []

    @staticmethod
    def assert_upload_two_files_to_document_version(res=None, doc_ver_id=None):
        """Проверка прикрепления двух файлов к версии документа с вычислением хеша файла."""
        assert len(res['result']['files']) == 2
        assert res['result']['files'][0]['name'] == File.open_file()[0][1][0]
        assert res['result']['files'][1]['name'] == File.open_file()[1][1][0]
        assert (res['result']['files'][0]['documentVersionId'] and
                res['result']['files'][1]['documentVersionId'] == doc_ver_id)

    @staticmethod
    def assert_document_version_actual(self, doc_api=None, create_doc=None, version_number=None):
        """Получение информации о документе и проверка, что версия документа имеет признак актуальности."""
        get_info = Document.get_data_by_document_id(self=self, url_api=doc_api,
                                                    doc_id=create_doc['result']['documentId'])
        assert get_info['result']['documentVersions'][version_number]['isActual'] is True

    @staticmethod
    def assertion_metadata_about_document_version(res=None, file=None):
        """Проверка метаданных в созданной версии документа."""
        assert res["result"]["expireDate"] == Document.data_for_creating_document_indicating_file_id()["expireDate"]
        assert res["result"]["sourceDate"] == Document.data_for_creating_document_indicating_file_id()["sourceDate"]
        assert res["result"]["documentProperties"]["Date"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["Date"]
        assert res["result"]["documentProperties"]["String"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["String"]
        assert res["result"]["documentProperties"]["Boolean"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["Boolean"]
        assert res["result"]["documentProperties"]["Decimal"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["Decimal"]
        assert res["result"]["documentProperties"]["Integer"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["Integer"]
        assert res["result"]["documentProperties"]["DateTime"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["DateTime"]
        assert res["result"]["documentProperties"]["Dictionary"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["Dictionary"]
        assert res["result"]["documentProperties"]["StringArray"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["StringArray"]
        assert res["result"]["files"][0]["id"] == file["result"]["files"][0]["id"]
        assert res["result"]["files"][0]["name"] == File.open_file()[0][1][0]

    @staticmethod
    def assertion_metadata_about_document(res=None, file=None):
        """Проверка метаданных в созданной версии документа."""
        assert res["result"]["documentVersions"][0]["documentProperties"]["Date"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["Date"]
        assert res["result"]["documentVersions"][0]["documentProperties"]["String"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["String"]
        assert res["result"]["documentVersions"][0]["documentProperties"]["Boolean"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["Boolean"]
        assert res["result"]["documentVersions"][0]["documentProperties"]["Decimal"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["Decimal"]
        assert res["result"]["documentVersions"][0]["documentProperties"]["Integer"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["Integer"]
        assert res["result"]["documentVersions"][0]["documentProperties"]["DateTime"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["DateTime"]
        assert res["result"]["documentVersions"][0]["documentProperties"]["Dictionary"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["Dictionary"]
        assert res["result"]["documentVersions"][0]["documentProperties"]["StringArray"] == \
               Document.data_for_creating_document_indicating_file_id()["documentProperties"]["StringArray"]
        assert res["result"]["documentVersions"][0]["files"][0]["id"] == file["result"]["files"][0]["id"]

    @staticmethod
    def assertion_information_about_created_document_and_its_version(doc=None, file=None, doc_type_id=None, num=None):
        """Проверка информации о созданном документе и его созданной версии."""
        assert doc["result"]["documentTypeId"] == doc_type_id
        assert doc["result"]["documentVersions"][0]["id"] == file["result"]["files"][num]["documentVersionId"]
        assert doc["result"]["documentVersions"][0]["files"][0]["id"] == file["result"]["files"][num]["id"]

    @staticmethod
    def assertion_download_file(res=None):
        """Проверка загрузки файла с указанием типа документа."""
        assert isinstance(res['result']['files'][0]["id"], str) is True
        assert res["result"]["files"][0]["name"] == File.open_file()[0][1][0]
        assert isinstance(res['result']['files'][0]["documentId"], str) is True
        assert isinstance(res['result']['files'][0]["documentVersionId"], str) is True

    @staticmethod
    def assertion_download_3_files(res=None):
        """Проверка загрузки 3 разных файлов с указанием типа документа."""
        for num in range(0, 3):
            assert isinstance(res['result']['files'][num]["id"], str) is True
            assert res["result"]["files"][num]["name"] == File.open_file()[num][1][0]
            assert isinstance(res['result']['files'][num]["documentId"], str) is True
            assert isinstance(res['result']['files'][num]["documentVersionId"], str) is True

    @staticmethod
    def assertion_document_version_and_file_information(res=None):
        """Проверка наличия нужных полей в документе, версии и файле."""
        assert "id" in res["result"]
        assert "documentId" in res["result"]["documentVersions"][0]
        assert "documentTypeId" in res["result"]
        assert "name" in res["result"]
        assert "createdByUserId" in res["result"]
        assert "id" in res["result"]["documentVersions"][0]
        assert "version" in res["result"]["documentVersions"][0]
        assert "expireDate" in res["result"]["documentVersions"][0]
        assert "sourceDate" in res["result"]["documentVersions"][0]
        assert "isActual" in res["result"]["documentVersions"][0]
        assert "documentProperties" in res["result"]["documentVersions"][0]
        assert "files" in res["result"]["documentVersions"][0]
        assert "documentEntities" in res["result"]

    @staticmethod
    def assertion_linked_documents(res=None):
        """Проверка связанных документов дочернего и родителя."""
        assert "documents" in res["result"]
        assert "id" in res["result"]["documents"][0]
        assert "documentLinkId" in res["result"]["documents"][0]
        assert "documentTypeId" in res["result"]["documents"][0]
        assert "id" in res["result"]["documents"][0]["documentType"]
        assert "okzRequestNumber" in res["result"]["documents"][0]
        assert "debitCardNumber" in res["result"]["documents"][0]
        assert "accountNumber" in res["result"]["documents"][0]
        assert "crmClientId" in res["result"]["documents"][0]
        assert "applicationId" in res["result"]["documents"][0]
        assert "creditContractNumber" in res["result"]["documents"][0]
        assert "allowExtraFileTypes" in res["result"]["documents"][0]["documentType"]
        assert "allowExtraPropertyTypes" in res["result"]["documents"][0]["documentType"]
        assert "name" in res["result"]["documents"][0]["documentType"]
        assert "parentFolderId" in res["result"]["documents"][0]["documentType"]

    @staticmethod
    def assertion_modified_on_in_documents(res=None, doc_type_id=None):
        """Проверка, что в каждом документе отображается параметр "Дата изменения" (modifiedOn)."""
        for doc in res["result"]["data"]:
            assert doc["documentTypeId"] == doc_type_id
            assert "modifiedOn" in doc

    @staticmethod
    def assertion_id_uploaded_files_is_equal_id_files_in_document(res=None):
        """Проверка, что id загруженных файлов равны id прикрепленных файлов при создании документа и его версии."""
        assert "id" in res["result"]["documentVersions"][0]["files"][0]
        assert "id" in res["result"]["documentVersions"][0]["files"][1]
        assert "id" in res["result"]["documentVersions"][0]["files"][2]

    @staticmethod
    def assertion_id_uploaded_files_is_equal_id_files_in_document_version(res=None, doc=None):
        """Проверка, что id загруженных файлов равны id прикрепленных файлов для данной версии документа."""
        assert res["result"]["documentId"] == doc["result"]["documentId"]
        assert "id" in res["result"]["files"][0]
        assert "id" in res["result"]["files"][1]
        assert "id" in res["result"]["files"][2]

    @staticmethod
    def assertion_creation_document_type(res=None):
        """Проверка создания типа документа."""
        assert "id" in res["result"]
        assert res["success"] is True

    @staticmethod
    def assert_get_document_by_id_with_all_versions(res=None):
        """Проверка всех полей при получении документа по ID."""
        assert "id" in res["result"]
        assert "name" in res["result"]
        assert "isActual" not in res["result"]
        assert "documentTypeId" in res["result"]
        assert "files" in res["result"]
        assert "id" in res["result"]["files"][0]
        assert res["result"]["files"][0]["isSigned"] is False
        assert "documentEntities" not in res["result"]
