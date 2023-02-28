#!/bin/sh

loopCnt=$1
if [[ "X$loopCnt" == "X" ]]; then
loopCnt="500"
fi

for i in `seq 1 $loopCnt`; do
bash -x attach_develop.sh 0 
py_pid=`cat ./py_pid`
sleep 10 ; kill -2  $py_pid; sleep 1 ;  kill -9  $py_pid;
# wait $py_pid ; sleep 2
done

#tail -f search.log