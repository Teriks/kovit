#!/bin/bash

if [[ "$(uname -s)" == 'Darwin' ]]; then
    sw_vers
    
    git clone --depth 1 --branch v1.2.3 https://github.com/pyenv/pyenv ~/.pyenv
    
    PYENV_ROOT="$HOME/.pyenv"
    PATH="$PYENV_ROOT/bin:$PATH"
    
    eval "$(pyenv init -)"

    pyenv install 3.6.5
    pyenv global 3.6.5

    pyenv rehash
fi
