#!/bin/bash
usage() {
    echo "Usage: $0 [-c] [-r]"
    echo "  -c: create index only "
    echo "  -r: run test after index created"
    exit 1
}

# Check if no arguments are provided
if [ "$#" -eq 0 ]; then
    echo "No flags provided. Please see usage."
    usage
    exit 1
fi

err_exit() {
    echo "${0##*/}: $1" >&2
    exit 1
}

change_index_settings() {
    echo "Updating settings"
}

create_index_only() {
    echo "Create index only"
    change_index_settings
}

run_test_only() {
    echo "Running test only"
}

optargs=cr
while getopts "$optargs" arg; do
    case $arg in
    c) create_index_only ;;
	r) run_test_only ;;
    ?)
        usage
        exit 1
        ;;
    esac
done

# Needed for accessing multiple argument options or accessing non-option arguments after argument flags are processed
shift $((OPTIND - 1))

# Check if any non-option arguments remain
if [ "$#" -ne 0 ]; then
    echo "Error: Unexpected arguments: $*"
    usage
fi


