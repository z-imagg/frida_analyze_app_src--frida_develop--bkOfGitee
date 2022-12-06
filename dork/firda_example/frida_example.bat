#python 3.8

set PATH=D:\Python38;D:\Python38\Scripts;%PATH%

@rem pip mirror
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip install --upgrade pip

pip install frida-tools

@REM cd D:\instrmcpp\dork\firda_example\
frida-trace  -i "*" -f D:\instrmcpp\dork\cmake-build-debug\dork.exe
@REM generate many js script