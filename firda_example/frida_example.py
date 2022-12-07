
from frida import core
from util import Util

""" ref: 
https://frida.re/docs/javascript-api/
https://blog.csdn.net/Qwertyuiop2016/article/details/114284618
"""


script_enumerateModules=Util.read_text("D:/frida-home/frida-agent-4instrmcpp/findFuncByName_using_DebugSymbol.js")

import frida
import sys

local:core.Device = frida.get_local_device()
pid:int = local.spawn("D:/instrmcpp/dork/cmake-build-debug/dork.exe",stdio='inherit')
session:core.Session = local.attach(pid)
script:core.Script = session.create_script(script_enumerateModules )
# % int('00000001400011D1', 16)
def on_message(message, data):
    print(message)
script.on('message', on_message)
script.load()
sys.stdin.read()


