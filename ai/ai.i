/* file: sample.i */
%module libai
%{
// #define SWIG_FILE_WITH_INIT
#include "ai.h"
%}

%include ai.h
