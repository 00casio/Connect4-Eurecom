#!/bin/bash

# echo "If you want to compile ai.cpp, don't forget to use the -03 flag."
# echo "For now, (without multithreading) g++ seems to produce better binary than clang++-16"
# echo "You can benchmark this by using the ai_benchmark.cpp program"

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

boost_lib="boost_$(echo ${com//.})"
ldconfig -p | grep ${boost_lib} 2>/dev/null 1>&2
if [ $? -eq 0 ]; then
  g++ -shared ai.cpp -o libai.so -O3 -I /usr/include/python3.11 -l "${boost_lib}" -fPIC
  ${com} main.py --no-camera --no-sound
else
  echo "Could not find the boost library on your machine, deactivating it" | tee >&2
  ${com} main.py --no-camera --no-sound --no-libai
fi
