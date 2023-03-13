#!/bin/bash

com="python3.11"
python3.11 -c ""
if [ $? -ne 0 ]; then
  python3.10 -c ""
  if [ $? -eq 0 ]; then
  echo "Using python 3.10"
  com="python3.10"
  else
    echo "Could not find correct python version"
    exit 1
  fi
else
  echo "Using python 3.11"
fi

test() {
    $1 -c "import $2" 1>/dev/null 2>&1
    if [ $? != 0 ]; then
        $1 -m pip install -U $2
    fi
}

to_install="pygame numpy mediapipe pyautogui playsound pygobject protobuf==3.20.1"

for module in ${to_install}; do
    test ${com} ${module}
done

${com} main.py
