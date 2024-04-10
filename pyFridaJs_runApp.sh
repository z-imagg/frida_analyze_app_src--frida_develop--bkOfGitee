#!/usr/bin/env bash

#去此脚本所在目录
f=$(readlink -f ${BASH_SOURCE[0]})  ; d=$(dirname $f)
cd $d

#临时关闭Linux的ASLR(地址空间随机化) ， 否则 x.so 中的函数地址 每次都不同， 
#  参考  https://blog.csdn.net/counsellor/article/details/81543197
echo 0 | sudo tee   /proc/sys/kernel/randomize_va_space
cat  /proc/sys/kernel/randomize_va_space  #0

function get_bash_en_dbg() {
  bash_en_dbg=false; [[ $- == *x* ]] && bash_en_dbg=true #记录bash是否启用了调试模式
}

cd /fridaAnlzAp/frida_develop/

#安装frida py工具
# 临时关闭bash调试模式， 是 由于 miniconda 的 activate 脚本内容太大，从而减少视觉干扰
get_bash_en_dbg  #记录bash是否启用了调试模式
$bash_en_dbg && set +x #如果启用了调试模式, 则关闭调试模式
source /app/Miniconda3-py310_22.11.1-1/bin/activate
$bash_en_dbg && set -x #如果启用了调试模式, 则打开调试模式
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt

#删除旧日志
rm -frv *.log

python frida_run_app.py

md5sum frida-out-Pure-*.log > frida-out-Pure.md5sum.txt

#最终产物日志文件名举例： frida-out-Pure-1712031317.log  
#    其数字签名举例： frida-out-Pure-1712031317.log.md5sum.txt

#查看elf文件中符号名举例
# readelf --symbols  /fridaAnlzAp/cgsecurity--testdisk/src/testdisk  | grep main