#!/bin/sh

loopCnt=$1
if [[ "X$loopCnt" == "X" ]]; then
loopCnt="500"
fi

for i in `seq 1 $loopCnt`; do
bash -x attach_develop.sh 0 2>&1 > search.log &
pid=$!
sleep 4
kill -2 $pid
done

#tail -f search.log