#!/bin/sh


argIdx=$1
if [[ "X$argIdx" == "X" ]]; then
argIdx="0"
fi

argVal=$2
if [[ "X$argVal" == "X" ]]; then
argVal="#define"
fi

echo '''
#include <string>
using namespace std;
#define MAX_USER_CNT 10
class User{
private: 
int id;
string name;
}
''' > User.h

echo '''
#include "User.h"
#include <stdio.h>
int main(int argc, char **argv )
{
int i=0;
for(i=0; i< argc; i++){
printf("argi:%d,%s\n",i,argv[i]);
}
return 0;
}
''' > echo_args.c

#clang  -c  echo_args.c
#clang echo_args.o -o echo_args

echo -n '-c  echo_args.c -v' > clang_args.txt
#echo -n '_nothing,' > _funcNameLsIgnore_.txt
touch _funcNameLsIgnore_.txt
echo -n 'frida-,libpthread-' > _moduleNamePrefixListIgnore_.txt

echo -n "$argIdx" > _argSearch_argIndex_.txt
echo -n "$argVal" > _argSearch_target_.txt
# touch ${argIdx}_argSearch_result.txt



clang_real_path=$(readlink  -f `which clang`)
python attach_develop.py $clang_real_path   clang_args.txt  `pwd`  frida_js/develop.js _funcNameLsIgnore_.txt  2>&1 > search.log  &
#python attach_develop.py c:/Windows/notepad.exe  d:/1.txt  /pubx/instrmcpp/frida-agent-4instrmcpp/attach_operator_new__constructor.js _funcNameLsIgnore_.txt
pid=$!
echo -n $pid > ./py_pid