
from frida import core


""" ref: 
https://frida.re/docs/javascript-api/
https://blog.csdn.net/Qwertyuiop2016/article/details/114284618
"""


import frida
import sys

#device = frida.get_device_manager().enumerate_devices()
local:core.Device = frida.get_local_device()
# a = local.get_process('hello.exe')
# print(a)
pid:int = local.spawn("dork.exe")
session = local.attach(pid)
script = session.create_script("""
var modules = Process.enumerateModules();
for (let module of modules) {
    send(module);
}
"""
# % int('00000001400011D1', 16)
                               )
# start .text 00000001400011D1 00000005   R . . . . . .
def on_message(message, data):
    print(message)
script.on('message', on_message)
script.load()
sys.stdin.read()
