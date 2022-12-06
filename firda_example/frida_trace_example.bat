#python 3.8

set PATH=D:\Python38;D:\Python38\Scripts;%PATH%

@rem pip mirror
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip install --upgrade pip

pip install frida-tools

@REM cd D:\instrmcpp\dork\firda_example\

@REM frida-trace  -i "*" -f D:\instrmcpp\dork\cmake-build-debug\dork.exe
@REM generate many js script

frida-trace -X "frida_agent.dll" -X "ucrtbased.dll"  -X "vcruntime140d.dll"  -X "vcruntime140_1d.dll" -X "apphelp.dll"  -X "KernelBase.dll"  -X "kernel32.dll"  -X "ntdll.dll"    -I "*"  -f D:\instrmcpp\dork\cmake-build-debug\dork.exe
frida-trace  -a "dork.exe!0x00007FF7B36E18B0" -f  dork.exe


C:\Windows\System32\ucrtbased.dll
C:\Windows\System32\vcruntime140d.dll
C:\Windows\System32\vcruntime140_1d.dll
C:\Windows\System32\apphelp.dll
C:\Windows\System32\KernelBase.dll
C:\Windows\System32\kernel32.dll
C:\Windows\System32\ntdll.dll

frida-trace  -i "sub_1400018B0" -f D:\instrmcpp\dork\cmake-build-debug\dork.exe
