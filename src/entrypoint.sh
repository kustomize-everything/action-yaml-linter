#!/bin/bash

parse_inputs() {

    yamllint_file_or_dir=""
    if [ "${INPUT_YAMLLINT_FILE_OR_DIR}" != "" ]; then
        yamllint_file_or_dir="${INPUT_YAMLLINT_FILE_OR_DIR}"
    fi

    yamllint_strict=''
    if [ "${INPUT_YAMLLINT_STRICT}" == "1" ] || [ "${INPUT_YAMLLINT_STRICT}" == "true" ]; then
        yamllint_strict="--strict"
    fi

    yamllint_config_filepath=''
    if [ -n "${INPUT_YAMLLINT_CONFIG_FILEPATH}" ]; then
        yamllint_config_filepath="--config-file ${INPUT_YAMLLINT_CONFIG_FILEPATH}"
    fi

    yamllint_config_datapath=''
    if [ -n "${INPUT_YAMLLINT_CONFIG_DATAPATH}" ]; then
        yamllint_config_datapath="--config-data ${INPUT_YAMLLINT_CONFIG_DATAPATH}"
    fi

    yamllint_format=''
    if [ -n "${INPUT_YAMLLINT_FORMAT}" ]; then
        yamllint_format="--format ${INPUT_YAMLLINT_FORMAT}"
    fi

    yamllint_comment=0
    if [[ "${INPUT_YAMLLINT_COMMENT}" == "0" || "${INPUT_YAMLLINT_COMMENT}" == "false" ]]; then
        yamllint_comment="0"
    fi

    if [[ "${INPUT_YAMLLINT_COMMENT}" == "1" || "${INPUT_YAMLLINT_COMMENT}" == "true" ]]; then
        yamllint_comment="1"
    fi

    # These are required parameters for yaml_lint()
    export yamllint_file_or_dir
    export yamllint_strict
    export yamllint_config_filepath
    export yamllint_config_datapath
    export yamllint_format
    export yamllint_comment

}

main() {

    scriptDir=$(dirname "${0}")
    # shellcheck disable=SC1091
    source "${scriptDir}/yaml_lint.sh"
    parse_inputs

    yaml_lint

}

main "${*}"
