#!/bin/bash

if [[ "$(uname -s)" == 'Darwin' ]]; then
    sw_vers
    curl -o python36.pkg https://www.python.org/ftp/python/3.6.5/python-3.6.5-macosx10.6.pkg
    sudo installer -verbose -pkg python36.pkg -target /
    which python3
fi
