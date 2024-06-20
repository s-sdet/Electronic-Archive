ARG docker_registry="***"
FROM ${docker_registry}/docker/testrail/autotests-web/testrail-autotests-web:latest
#FROM ${docker_registry}/docker/testrail/autotests-api/testrail-autotests-api:latest
ENV TEST_KEY="test"

COPY . /afds-autotests

WORKDIR /afds-autotests

RUN chmod -R 777 /afds-autotests
RUN pip install -r requirements.txt -i https://***/artifactory/api/pypi/pypi/simple --trusted-host ***

CMD pytest --headless ui/