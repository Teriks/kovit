#!/bin/bash

if [[ "$(uname -s)" == 'Darwin' ]]; then
    sw_vers
    curl -o python36.pkg https://www.python.org/ftp/python/3.6.5/python-3.6.5-macosx10.6.pkg
    installer -pkg python36.pkg -target /
fi
