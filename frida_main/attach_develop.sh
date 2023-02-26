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
echo -n '_ZN4llvm3sys7Process18UseANSIEscapeCodesEb,_ZN4llvm3opt6OptionD1Ev,_ZN4llvm18format_object_base4homeEv,_ZN4llvm3sys4path6nativeERNS_15SmallVectorImplIcEE,_ZN4llvm7APFloat18semanticsPrecisionERKNS_12fltSemanticsE,_ZN4llvm10CallbackVH6anchorEv,_ZN4llvm18RefCountedBaseVPTR6anchorEv,_ZNK4llvm4Type20getVectorNumElementsEv,LLVMInitializeCppBackendTargetMC,_ZN4llvm2cl11StringSaver6anchorEv,pthread_mutexattr_destroy,pthread_rwlock_destroy,_ZSt20__throw_length_errorPKc,__cxa_finalize,waitpid,_ZN4llvm15SmallPtrSetImpl16shrink_and_clearEv,_ZSt17__throw_bad_allocv,uncompress,_ZSt17__throw_bad_allocv,crc32,exit,sigprocmask,pthread_join,sin,_ZNKSt15basic_stringbufIcSt11char_traitsIcESaIcEE3strEv,_ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base,strlen,sigfillset,_ZNSi5seekgElSt12_Ios_Seekdir,ftruncate' > _funcNameLsIgnore_.txt
clang_real_path=$(readlink  -f `which clang`)
python attach_develop.py $clang_real_path   clang_args.txt  `pwd`  frida_js/develop.js _funcNameLsIgnore_.txt



