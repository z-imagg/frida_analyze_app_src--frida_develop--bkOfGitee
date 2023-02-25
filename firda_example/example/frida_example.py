
from frida import core
from util import Util
"""
注意本脚本 没有正确处理 dork.exe 的detach等, 所以即使停止本脚本 dork.exe依然不会退出、本脚本自身也不会退出. 
正确处理 dork.exe 的detach等, 请参照: 
    https://gitcode.net/pubz/instrmcpp/-/blob/frida_inject_dork_demo/firda_example/attach_operator_new__constructor.py
    即 https://gitcode.net/pubz/instrmcpp/-/blob/cfa54642b7ec1c800a607b6efe68716a6aeacedc/firda_example/attach_operator_new__constructor.py
"""

""" ref: 
https://frida.re/docs/javascript-api/
https://blog.csdn.net/Qwertyuiop2016/article/details/114284618
"""


# script_enumerateModules=Util.read_text("D:/frida-home/frida-agent-4instrmcpp/findFuncByName_using_DebugSymbol.js")
# script_enumerateModules=Util.read_text("D:/frida-home/frida-agent-4instrmcpp/enumerateExports.js")
# script_enumerateModules=Util.read_text("/frida-home/frida-agent-4instrmcpp/enumerateImports.js")
# script_enumerateModules=Util.read_text("D:/frida-home/frida-agent-4instrmcpp/enumerateSymbols.js")
# script_enumerateModules=Util.read_text("D:/frida-home/frida-agent-4instrmcpp/attach_main_ZUser.js")

import frida
import sys

assert len(sys.argv)>4
dork_exe_path:str=sys.argv[1] #/instrmcpp/dork/cmake-build-debug/dork.exe
dork_args_file:str=sys.argv[2] #给目标的参数 存放的文件路径
js_path:str=sys.argv[3] #"/frida-home/frida-agent-4instrmcpp/enumerateImports.js"

dork_args:str=Util.read_text(dork_args_file) #读取目标参数

script_enumerateModules=Util.read_text(js_path)
local:core.Device = frida.get_local_device()
pid:int = local.spawn(dork_exe_path,argv=dork_args.split(' '),stdio='pipe')
session:core.Session = local.attach(pid)
script:core.Script = session.create_script(script_enumerateModules )
# % int('00000001400011D1', 16)
def on_message(message, data):
    print(message)
script.on('message', on_message)
script.load()
sys.stdin.read()


