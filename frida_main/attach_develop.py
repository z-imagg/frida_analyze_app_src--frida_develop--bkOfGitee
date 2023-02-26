#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
usage example:
python dork_exe_path dork_arg_file dork_cwd js_path
@see attach_develop.sh

"""
#ref: https://www.anquanke.com/post/id/177597
from __future__ import print_function

from pathlib import Path
from typing import List

import frida
import frida_tools
import threading

from frida_tools.reactor import Reactor

from FileUtil import Util
import sys

from LambdaUtil import LambdaUtil


def _assert(err:bool,errMsg:str):
    if err is None or err:
        raise Exception(errMsg)


class Application(object):
    def __init__(self):
        print(sys.argv)
        _assert(not len(sys.argv) >= 5, f"{__name__} dork_exe_path dork_arg_file dork_cwd js_path ")
        self.dork_exe_path: str = sys.argv[1]  # /instrmcpp/dork/cmake-build-debug/dork.exe
        self.dork_exe_name: str = Path(self.dork_exe_path).name

        _dork_arg_file: str = sys.argv[2]  # 给目标的参数 存放的文件路径
        _dork_arg_str: str = Util.read_text(_dork_arg_file)  # 读取目标参数
        self._dork_args: List[str] =LambdaUtil.lsFilter(_dork_arg_str.split(' '),lambda k: k is not None and len(k) > 0)
        self._dork_args: List[str] =LambdaUtil.ls2ls(self._dork_args,lambda k:k.strip())

        self.dork_cwd:str=sys.argv[3]
        self._js_path:str= sys.argv[4]  # "/frida-home/frida-agent-4instrmcpp/enumerateImports.js"

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
        print(f"✔ spawn(program={self.dork_exe_path}, argv={self._dork_args},cwd={self.dork_cwd})" )
        pid:int = self._device.spawn(program=self.dork_exe_path, argv=self._dork_args,cwd=self.dork_cwd,stdio="pipe")
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
        script_text=script_text.replace("dork.exe", self.dork_exe_name)
        script_text=script_text.replace("__dork_exe_full_path__", self.dork_exe_path)
        print(f"script_text:{script_text}")
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