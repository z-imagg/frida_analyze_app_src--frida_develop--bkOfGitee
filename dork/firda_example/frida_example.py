
from frida import core


""" ref: 
https://frida.re/docs/javascript-api/
https://blog.csdn.net/Qwertyuiop2016/article/details/114284618
"""


def read_text(fpath:str):
    with open(fpath,"r") as f:
        return f.read()
script_enumerateModules=read_text("./script/enumerateModules.js")

import frida
import sys

local:core.Device = frida.get_local_device()
pid:int = local.spawn("dork.exe")
session:core.Session = local.attach(pid)
script = session.create_script(script_enumerateModules )
# % int('00000001400011D1', 16)
def on_message(message, data):
    print(message)
script.on('message', on_message)
script.load()
sys.stdin.read()


