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
from typing import List

import frida
import frida_tools
import threading

from frida_tools.repl import main
from frida_tools.reactor import Reactor
from frida_tools.application import ConsoleApplication

import sys


_options=Namespace(device_id=None,   target=('file', ['/fridaAnlzAp/cgsecurity--testdisk/src/testdisk']),    args=['/fridaAnlzAp/cgsecurity--testdisk/hd.imgxx'],  user_scripts=['/fridaAnlzAp/frida_js/InterceptFnSym.js'],     logfile='1.log', )
_stop_requested:threading.Event = threading.Event()
app=ConsoleApplication(
    run_until_return=lambda reactor: _stop_requested.wait(),
    # on_stop=lambda x: _stop_requested.set()
    _options=_options
)
app._aux=["cwd=(string)/tmp/"]
app.run()
