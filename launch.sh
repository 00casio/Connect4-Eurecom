#!/bin/bash

test() {
    python3.11 -c "import $1"
    if [ $? != 0 ]; then
        python3.11 -m pip install $1
}
