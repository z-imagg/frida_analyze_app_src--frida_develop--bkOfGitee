#!/bin/sh


echo -n ' ' > _args.txt

#http://giteaz:3000/frida_analyze_app_src/frida_js/src/commit/b30e4e2cbf92a80f1abe92f7d1f1dc410ccabb6e/frida-trace.js

python frida_run_app.py /fridaAnlzAp/torch-cpp/v1.0.0/simple_nn.elf   _args.txt  `pwd`  /fridaAnlzAp/frida_js/frida-trace.js _funcNameLsIgnore_.txt  2>&1   | tee -a search.log
#python frida_run_app.py c:/Windows/notepad.exe  d:/1.txt  /pubx/instrmcpp/frida-agent-4instrmcpp/attach_operator_new__constructor.js _funcNameLsIgnore_.txt
pid=$!
echo -n $pid > ./py_pid