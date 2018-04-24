#!/bin/bash

if [[ "$(uname -s)" != 'Darwin' ]]; then
    if [[ $1 == run_tests ]]; then
        python3 -m coverage run run_tests.py
    else
        python3 -m codecov
    fi
else
    # test but don't upload coverage on mac
    if [[ $1 == run_tests ]]; then
        python3 run_tests.py
    fi
fi