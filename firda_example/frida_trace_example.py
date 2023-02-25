import sys

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
sys.argv=['xxxx', '-i', '!', '-f', 'C:/Windows/system32/notepad.exe -ccc']

app = TracerApplication()
app.run()