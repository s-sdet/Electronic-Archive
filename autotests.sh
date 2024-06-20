#!/usr/bin/env bash

set -e

case $1 in
"api"|"ui")
  echo "--- start $1 autotest ---"
  cd autotests
  pip3 install -r requirements.txt
  pytest $1 \
    --testrail \
    --tr-no-ssl-cert-check \
    --tr-url=${TR_URL} \
    --tr-email=${TR_EMAIL} \
    --tr-password=${TR_PASSWORD} \
    --tr-testrun-assignedto-id=${TR_TESTRUN_ASSIGNEDTO_ID} \
    --tr-testrun-project-id=${TR_TESTRUN_PROJECT_ID} \
    --tr-testrun-name="${TR_TESTRUN_NAME}" \
    --tr-testrun-suite-id=${TR_TESTRUN_SUITE_ID}
  echo '--- end autotest ---'
  exit 0;;
*)
  echo "no arguments (api or ui)"
  exit 1;;
esac
