#!/bin/bash

# echo "If you want to compile ai.cpp, don't forget to use the -O3 flag."
# echo "If possible, try to use clang++-16 because the binary produced are the fastest amongst all"
# echo "You can benchmark this by using the ai/ai_benchmark.py program"

# Find correct Python version
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

# Install packages
${com} -m pip install -r requirements.txt

# Change python headers location based on OS
python_ver=$(${com} -c "from sys import version_info as v; print(f'{v[0]}.{v[1]}')")
n=$(uname -s)
if [ $? -ne 0 ]; then
  echo "You are most probably on windows, or your installation has a lot of problems"
  exit
elif [ "$n" ==  "Darwin" ]; then # MacOS
  PYTHON_HEADERS="/Library/Frameworks/Python.framework/Versions/${python_ver}/include/python${python_ver} -std=c++17 -undefined dynamic_lookup"
else # *UNIX
  PYTHON_HEADERS="/usr/include/python${python_ver}"
fi

# If swig is present, use it for the AI
swig -version 2>/dev/null 1>&2
if [ $? -eq 0 ]; then
  swig -Wall -python -c++ -o ai/ai_wrap.cxx ai/ai.i
  g++ -shared -O3 -fPIC ai/ai.cpp ai/ai_wrap.cxx -o ai/_libai.so -I ${PYTHON_HEADERS}
  ${com} main.py --no-camera --no-sound
else
  echo "Could not find swig, deactivating it for now. Please install it" | tee >&2
  ${com} main.py --no-camera --no-sound --no-libai
fi
