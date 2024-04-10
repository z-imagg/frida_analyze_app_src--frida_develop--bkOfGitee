#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
usage example:
python dork_exe_path dork_arg_file dork_cwd js_path
@see frida_run_app.sh

"""
#ref: https://www.anquanke.com/post/id/177597
from __future__ import print_function
from argparse import Namespace
import typing
from pathlib import Path
from typing import Callable, List

import frida
import frida_tools
import threading

from frida_tools.repl import main
from frida_tools.reactor import Reactor
from frida_tools.application import ConsoleApplication, await_enter

import sys


_options=Namespace(device_id=None, device_type=None, host=None, certificate=None, origin=None, token=None, keepalive_interval=None, session_transport='multiplexed', stun_server=None, relays=None, target=('file', ['/fridaAnlzAp/cgsecurity--testdisk/src/testdisk']), stdio='inherit', aux=[], realm='native', runtime=None, enable_debugger=False, squelch_crash=False, args=['/fridaAnlzAp/cgsecurity--testdisk/hd.imgxx'], options_file=None, user_scripts=['/fridaAnlzAp/frida_js/InterceptFnSym.js'], user_parameters=None, user_cmodule=None, toolchain='any', codeshare_uri=None, eval_items=None, quiet=False, timeout=0, on_spawn_complete='resume', logfile='1.log', eternalize=False, exit_on_error=False, autoperform=False, autoreload=True)

class MyConsoleApp(ConsoleApplication):
    def __init__(self, 
        run_until_return: Callable[[Reactor], None] = ..., 
        on_stop: Callable[[], None] | None = None, 
        args: List[str] | None = None,
        _options:Namespace=None
        ):
        super().__init__(
            run_until_return=run_until_return,
            on_stop=on_stop, 
            args=args,
            _options=_options
            )
        
    def _needs_target(self) -> bool:
        return True


_stop_requested:threading.Event = threading.Event()
app=MyConsoleApp(
    run_until_return=lambda reactor: _stop_requested.wait(),
    # on_stop=lambda x: _stop_requested.set()
    _options=_options
)

app._aux=["cwd=(string)/tmp/"]
app.run()
