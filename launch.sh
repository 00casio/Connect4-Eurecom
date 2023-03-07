#!/bin/bash

p311=$(python -c "import sys; print(sys.version_info[:2])")

if [ "$p311" == "(3, 11)" ]; then
  echo "Using python 3.11"
elif [ "$p311" == "(3, 10)" ]; then
  echo "Using python 3.10"
else
  echo "Could not find correct python version"
  exit 1
fi

test() {
    python -c "import $1"
    if [ $? != 0 ]; then
        python -m pip install $1
    fi
}

to_install="pygame numpy mediapipe pyautogui random math"

for module in ${to_install}; do
    test ${module}
done

python main.py
