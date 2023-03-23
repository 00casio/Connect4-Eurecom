#!/bin/bash

echo "If you want to compile ai.cpp, don't forget to use the -03 flag."
echo "For now, (without multithreading) g++ seems to produce better binary than clang++-16"
echo "We will need to benchmark that properly"

python3.11 -c "" 2>/dev/null 1>&2
if [ $? -ne 0 ]; then
  python3.10 -c "" 2>/dev/null 1>&2
  if [ $? -ne 0 ]; then
    python3.9 -c "" 2>/dev/null 1>&2
    if [ $? -eq 0 ]; then
      echo "Using python 3.9"
      com="python3.9"
    else
      echo "Could not find correct python version"
      exit 1
    fi
  else
    echo "Using python 3.10"
    com="python3.10"
  fi
else
  echo "Using python 3.11"
  com="python3.11"
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

${com} main.py --no-camera --no-sound
