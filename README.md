##  frida 跟踪 clang 编译过程 并能正常结束 但没有正常产生编译结果文件 echo_args.o
```bash
mkdir /pubx/; cd /pubx/
git clone git@gitcode.net:pubz/instrmcpp.git

cd /pubx/instrmcpp/frida_main/
bash -x attach_develop.sh 
```

1.  运行"bash -x attach_develop.sh"会结束不了, ctrl+c 结束, 并多次运行 "bash -x attach_develop.sh", 大约4到5次后, 本行运行可以正常结束, 不过并未产生编译结果文件echo_args.o; 

2. 运行"bash -x attach_develop.sh"正常结束时产生的文件 frida_main/_funcNameLsIgnore_.txt 内容如下:
```text
,_ZN4llvm3sys7Process18UseANSIEscapeCodesEb,_ZN4llvm3opt6OptionD1Ev,_ZN4llvm18format_object_base4homeEv,_ZN4llvm3sys4path6nativeERNS_15SmallVectorImplIcEE,_ZN4llvm7APFloat18semanticsPrecisionERKNS_12fltSemanticsE,_ZN4llvm10CallbackVH6anchorEv
```

3.  多次运行"bash -x attach_develop.sh"能正常结束的具体过程说明：
>> 每次运行 "bash -x attach_develop.sh" 遇到frida attach出错的函数名会写入文件 frida_main/_funcNameLsIgnore_.txt,   下次运行 从该文件读函数名从而忽略上次报错的函数名, 如此几次下来 即不再报错了
