#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
usage example:
python dork_exe_path dork_arg_file dork_cwd js_path
@see frida_run_app.sh

"""
#ref: https://www.anquanke.com/post/id/177597
from __future__ import print_function
import typing
from pathlib import Path
from typing import List

import frida
import frida_tools
import threading

from frida_tools.repl import main
from frida_tools.reactor import Reactor

from FileUtil import Util
import sys

from LambdaUtil import LambdaUtil

import time
def abs_ms_int_from1970():
    _abs_ms_float_from1970:float=time.time()
    _abs_ms_int_from1970:int=int(_abs_ms_float_from1970)
    return _abs_ms_int_from1970

def _assert(err:bool,errMsg:str):
    if err is None or err:
        raise Exception(errMsg)


class Application(object):
    def __init__(self):
        now_abs_ms:int=abs_ms_int_from1970()
        self.app_log_f=open(f"./frida-out-NotBusz-{now_abs_ms}.log","w")
        self.app_fnCallLog_f=open(f"./frida-out-Pure-{now_abs_ms}.log","w")
        print(sys.argv)
        # _assert(not len(sys.argv) >= 5, f"{__name__} dork_exe_path dork_arg_file dork_cwd js_path ")
        self.dork_exe_path: str = "/fridaAnlzAp/cgsecurity--testdisk/src/testdisk"  # /instrmcpp/dork/cmake-build-debug/dork.exe
        self.dork_exe_name: str = "testdisk"

        #hd.img　生成　参考:  http://giteaz:3000/bal/cmd-wrap/src/tag/v2.2.simpl/build_testdisk.md
        self._dork_args: List[str] =[self.dork_exe_path, "/fridaAnlzAp/cgsecurity--testdisk/hd.img"]

        self.dork_cwd:str="/tmp/"
        self._js_path:str= "/fridaAnlzAp/frida_js/InterceptFnSym.js"

        self._stop_requested:threading.Event = threading.Event()
        self._reactor:frida_tools.reactor.Reactor = Reactor(run_until_return=lambda reactor: self._stop_requested.wait())

        self._device:frida.core.Device = frida.get_local_device()
        self._sessions = set()

        # self._device.on("spawn-added", lambda child:
        #     self._reactor.schedule(lambda: self._on_delivered(child)))
    #     ValueError: Device does not have a signal named 'delivered', it only has: 'spawn-added', 'spawn-removed', 'child-added', 'child-removed', 'process-crashed', 'output', 'uninjected', 'lost'

    def _on_delivered(self, child):
        print("x delivered: {}".format(child))
        self._instrument(child.pid)

    def _stop_if_idle(self):
        if len(self._sessions) == 0:
            self._stop_requested.set()

    def _instrument(self, pid):
        print("y attach(pid={})".format(pid))
        session:frida.core.Session = self._device.attach(pid)
        
        session.on("detached", lambda reason:
            self._reactor.schedule(lambda: self._on_detached(pid, session, reason)))
        print("y enable_child_gating()")
        
        print("y create_script()")
        script_text:str=Util.read_text(self._js_path)#"/frida-home/frida-agent-4instrmcpp/attach_operator_new__constructor.js"
        # script_text=script_text.replace("_dork_exe_", self.dork_exe_name)
        # script_text=script_text.replace("__dork_exe_full_path__", self.dork_exe_path)
        # print(f"script_text:{script_text}")
        script:frida.core.Script = session.create_script(script_text)
        script.on("message", lambda message, data:
            self._reactor.schedule(lambda: self._on_message(pid, message,data)))  
        #_on_message的方法签名　参见　frida_js的send方法签名
        # send方法签名　在 /fridaAnlzAp/frida_js/node_modules/@types/frida-gum/index.d.ts
        print("y load()")
        script.load()
        
        session.enable_child_gating()
        print("y resume(pid={})".format(pid))
        self._device.resume(pid)
        self._sessions.add(session)

    def _on_detached(self, pid, session, reason):
        print("x detached: pid={}, reason='{}'".format(pid, reason))
        self._sessions.remove(session)
        self._reactor.schedule(self._stop_if_idle, delay=0.5)
        
        #关闭日志文件
        self.app_log_f.close()
        self.app_log_f=None
        self.app_fnCallLog_f.close()
        self.app_fnCallLog_f=None


    FnCallLogLinePrefix = "\n__@__@";

    def _on_message(self, pid, message:typing.Dict[str,typing.Any],data:bytes):
        #_on_message的方法签名　参见　frida_js的send方法签名
        # send方法签名　在 /fridaAnlzAp/frida_js/node_modules/@types/frida-gum/index.d.ts
        assert message is not None
        assert message.__contains__("payload")
        payload:str=message["payload"]
        if payload.startswith(Application.FnCallLogLinePrefix):#若是fnCallIdLog
            payload=payload.replace(Application.FnCallLogLinePrefix,"")
            print(payload,file=self.app_fnCallLog_f)
        else:    
            print("x message: pid={}, payload={}".format(pid, message ),file=self.app_log_f)
        pass
        
################################
    def run(self):
        # ._reactor.schedule(f) : 当前线程 启动新线程 新线程运行内容为f, 直到新线程运行完 才返回当前线程 : 即 主 异步调用 函数f 且 等 该函数f 返回
        self._reactor.schedule(lambda: self._start())

        self._reactor.run()
        
    def _start(self):
        print(f"y spawn(program={self.dork_exe_path}, argv={self._dork_args},cwd={self.dork_cwd})" )
        pid:int = self._device.spawn(program=self.dork_exe_path, argv=self._dork_args,cwd=self.dork_cwd,stdio="inherit")
        self._instrument(pid)

app = Application()
app.run()