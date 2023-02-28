#!/bin/bash

test() {
    python3.11 -c "import $1"
    if [ $? != 0 ]; then
        python3.11 -m pip install $1
    fi
}

to_install="pygame numpy mediapipe pyautogui"

for module in ${to_install}; do
    test ${module}
done

python3.11 main.py
python3.11 gesture.py
