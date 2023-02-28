#!/bin/sh

loopCnt=$1
if [[ "X$loopCnt" == "X" ]]; then
loopCnt="500"
fi

for i in `seq 1 $loopCnt`; do
bash -x attach_develop.sh 0  > /dev/null &
pid=`cat ./py_pid`
(sleep 4 ; kill -2  $pid; sleep 1 ;  kill -9  $pid;) &
wait $pid ; sleep 2
done

#tail -f search.log