#!/bin/sh

#python attach_develop.py c:/Windows/notepad.exe  d:/1.txt  /pubx/instrmcpp/frida-agent-4instrmcpp/attach_operator_new__constructor.js _funcNameLsIgnore_.txt
echo '''
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
clang_real_path=$(readlink  -f `which clang`)
python attach_develop.py $clang_real_path   clang_args.txt  `pwd`  frida_js/develop.js _funcNameLsIgnore_.txt



