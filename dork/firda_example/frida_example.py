import sys

from frida import core
from frida_tools.tracer import TracerApplication

#让frida-trace能单独被调用运行
# https://gitcode.net/fridaz/frida/-/commit/6ae5d35301c5d299a9a0f18077bb4a93801aef2c
# https://gitcode.net/fridaz/frida-tools/-/commit/83cfbad68ec38fb98999ae50699c216b633dc9cd

'''
where frida-trace
#D:/Python38/Scripts/frida-trace.exe

frida-trace   -i "!"  -f  dork.exe
'''
# sys.argv=['D:\\Python38\\Scripts\\frida-trace.exe', '-i', '!', '-f', 'dork.exe']
# sys.argv=['xxxx', '-i', '!', '-f', 'dork.exe']
#
# app = TracerApplication()
# app.run()



# from __future__ import print_function
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
