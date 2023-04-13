#!/bin/bash

# echo "If you want to compile ai.cpp, don't forget to use the -O3 flag."
# echo "If possible, try to use clang++-16 because the binary produced are the fastest amongst all"
# echo "You can benchmark this by using the ai/ai_benchmark.py program"

test_python() {
  if [ "$1" == "" ]; then
    echo "Could not find any correct python version, quitting now" | tee >&2
    return 1
  fi
  $1 -c "" 2>/dev/null 1>&2
  if [ $? -ne 0 ]; then
    echo "Could not find $1" | tee >&2
    shift
    test_python "$@"
  else
    echo "Using $($1 --version)" | tee >&2
    echo "$1"
  fi
}
com=$(test_python "python" "python3.11" "python3.10" "python3.9")
if [ "${com}" == "" ]; then exit; fi

install_pypi() {
  $1 -c "import $2" 2>/dev/null 1>&2
  if [ $? != 0 ]; then
    $1 -m pip install -U $2
  fi
}
to_install="pygame numpy mediapipe pyautogui playsound pygobject protobuf==3.20.1"
for module in ${to_install}; do
  install_pypi ${com} ${module}
done

python_ver=$(${com} -c "from sys import version_info as v; print(f'python{v[0]}.{v[1]}')")
swig -version 2>/dev/null 1>&2
if [ $? -eq 0 ]; then
  swig -Wall -python -c++ -o ai/ai_wrap.cxx ai/ai.i
  g++ -shared -O3 -fPIC ai/ai.cpp ai/ai_wrap.cxx -o ai/_libai.so -I /usr/include/${python_ver}
  ${com} main.py --no-camera --no-sound
else
  echo "Could not find swig, deactivating it for now. Please install it" | tee >&2
  ${com} main.py --no-camera --no-sound --no-libai
fi
