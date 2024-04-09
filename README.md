##  py驱动frida 跟踪 testdisk

testdisk编译、hd.img生成、testdisk运行，　　http://giteaz:3000/bal/cmd-wrap/src/tag/v2.2.simpl/build_testdisk.md

```bash
python frida_run_app.py
grep __@__@     app_log.txt  | wc -l 
# 6838
#日志行数较多可能是因为testdisk操作流程慢了或长了

#又运行一次
python frida_run_app.py
#快速走完testdisk操作流程，　获得日志行数明显变少了
grep __@__@ app_log.txt  | wc -l 
# 3252


```
