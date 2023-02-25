#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
usage example:
python attach_operator_new__constructor.py c:/Windows/notepad.exe  d:/1.txt  /pubx/instrmcpp/frida-agent-4instrmcpp/attach_operator_new__constructor.js

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
clang  -c  echo_args.c
clang echo_args.o -o echo_args
echo 'arg1 arg2' > _arg.txt
python attach_operator_new__constructor.py echo_args  _arg.txt  /pubx/instrmcpp/frida-agent-4instrmcpp/attach_operator_new__constructor.js

python D:\instrmcpp\firda_example\attach_operator_new__constructor.py  D:/instrmcpp/dork/cmake-build-debug/dork.exe
python D:\instrmcpp\firda_example\attach_operator_new__constructor.py  D:/llvm-home/llvm-project/build/Debug/bin/clang.exe -S -emit-llvm D:/instrmcpp/dork_simple/User.cpp
python D:\instrmcpp\firda_example\attach_operator_new__constructor.py  clang.exe -S -emit-llvm ./User.cpp
"""
#ref: https://www.anquanke.com/post/id/177597
from __future__ import print_function

from pathlib import Path
from typing import List

import frida
import frida_tools
import threading

from frida_tools.reactor import Reactor

from util import Util
import sys

def _assert(err:bool,errMsg:str):
    if err is None or err:
        raise Exception(errMsg)


class Application(object):
    def __init__(self):
        print(sys.argv)
        _assert(not len(sys.argv) >= 4, f"{__name__} dork_exe_path dork_arg_file js_path")
        dork_exe_path: str = sys.argv[1]  # /instrmcpp/dork/cmake-build-debug/dork.exe
        dork_arg_file: str = sys.argv[2]  # 给目标的参数 存放的文件路径
        js_path: str = sys.argv[3]  # "/frida-home/frida-agent-4instrmcpp/enumerateImports.js"

        _dork_arg_str: str = Util.read_text(dork_arg_file)  # 读取目标参数
        dork_exe_name: str = Path(dork_exe_path).name


        # self.dork_cmd_word_ls:List[str]= sys.argv[1:]
        #_dork_exe_full_path=["D:/llvm-home/llvm-project/build/Debug/bin/clang.exe","-S","-emit-llvm","D:/instrmcpp/dork_simple/User.cpp"]
        # want to run :"D:/llvm-home/llvm-project/build/Debug/bin/clang.exe -S -emit-llvm D:/instrmcpp/dork_simple/User.cpp"
        self.dork_exe_path:str=dork_exe_path
        self.dork_exe_name: str = dork_exe_name
        self._js_path:str=js_path
        self._dork_args:List[str]=list(filter(lambda k: k is not None and len(k) > 0, _dork_arg_str.split(' ')  ))
        self._stop_requested:threading.Event = threading.Event()
        self._reactor:frida_tools.reactor.Reactor = Reactor(run_until_return=lambda reactor: self._stop_requested.wait())

        self._device:frida.core.Device = frida.get_local_device()
        self._sessions = set()

        self._device.on("spawn-added", lambda child:
            self._reactor.schedule(lambda: self._on_delivered(child)))
    #     ValueError: Device does not have a signal named 'delivered', it only has: 'spawn-added', 'spawn-removed', 'child-added', 'child-removed', 'process-crashed', 'output', 'uninjected', 'lost'

    def run(self):
        # ._reactor.schedule(f) : 当前线程 启动新线程 新线程运行内容为f, 直到新线程运行完 才返回当前线程 : 即 主 异步调用 函数f 且 等 该函数f 返回
        self._reactor.schedule(lambda: self._start())

        self._reactor.run()

    def _start(self):
        print(f"✔ spawn(program={self.dork_exe_path}, argv={self._dork_args})" )
        pid:int = self._device.spawn(program=self.dork_exe_path, argv=self._dork_args)
        self._instrument(pid)

    def _stop_if_idle(self):
        if len(self._sessions) == 0:
            self._stop_requested.set()

    def _instrument(self, pid):
        print("✔ attach(pid={})".format(pid))
        session:frida.core.Session = self._device.attach(pid)
        session.on("detached", lambda reason:
            self._reactor.schedule(lambda: self._on_detached(pid, session, reason)))
        print("✔ enable_child_gating()")
        session.enable_child_gating()
        print("✔ create_script()")
        script_text:str=Util.read_text(self._js_path)#"/frida-home/frida-agent-4instrmcpp/attach_operator_new__constructor.js"
        script_text=script_text.replace("__dork_exe_full_path__", self.dork_exe_path)
        script:frida.core.Script = session.create_script(script_text)
        script.on("message", lambda message, data:
            self._reactor.schedule(lambda: self._on_message(pid, message)))
        print("✔ load()")
        script.load()
        print("✔ resume(pid={})".format(pid))
        self._device.resume(pid)
        self._sessions.add(session)

    def _on_delivered(self, child):
        print("⚡ delivered: {}".format(child))
        self._instrument(child.pid)

    def _on_detached(self, pid, session, reason):
        print("⚡ detached: pid={}, reason='{}'".format(pid, reason))
        self._sessions.remove(session)
        self._reactor.schedule(self._stop_if_idle, delay=0.5)

    def _on_message(self, pid, message):
        print("⚡ message: pid={}, payload={}".format(pid, message ))


app = Application()
app.run()