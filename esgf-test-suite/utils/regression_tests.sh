#!/bin/bash

readonly BASE_DIR_PATH="$(pwd)"
SCRIPT_PARENT_DIR_PATH="$(dirname $0)"; cd "${SCRIPT_PARENT_DIR_PATH}"
readonly SCRIPT_PARENT_DIR_PATH="$(pwd)" ; cd "${BASE_DIR_PATH}"

readonly MAX_RUN=${1:-1}
readonly TEST_DIR_PATH="${BASE_DIR_PATH}/tmp"

set -u

function test_suite
{
  echo "> test the ${1} nodes"
  for run in $(eval echo "{1..${MAX_RUN}}") ; do
    echo -n "  > try #${run}: "
    err_output_file_path="${TEST_DIR_PATH}/${1}_${run}.output"
    html_report_file_path="${TEST_DIR_PATH}/${1}_${run}.html"

    python esgf-test.py -v --nocapture --nologcapture --tc-file "${2}" "${3}" \
      --with-html --html-file="${html_report_file_path}" --with-id \
      1>"${err_output_file_path}" 2>&1

    if [ ${?} -ne 0 ]; then
      echo -e "\033[31mKO\033[0m"
      xdg-open "${html_report_file_path}"
    else
      echo -e "\033[32mok\033[0m"
    fi
  done
}

mkdir -p "${TEST_DIR_PATH}"
rm -f ${TEST_DIR_PATH}/*
cd "${SCRIPT_PARENT_DIR_PATH}/.."

test_suite "production"  "my_config_prod.ini" '-a '!compute,!slcs,!cog_create_user''
test_suite "integration" "my_config_int.ini"  '-a '!compute,!cog_create_user''
test_suite "development" "my_config_dev.ini"  '-a '!compute,!cog_create_user''
test_suite "llnl" "my_config_llnl.ini"  '-a '!compute,!slcs_django_admin_login,!cog_root_login,!cog_create_user''
test_suite "dkrz" "my_config_dkrz.ini"  '-a '!compute,!slcs_django_admin_login,!cog_root_login,!cog_create_user''