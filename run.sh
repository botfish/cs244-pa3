#!/bin/bash

# Note: Mininet must be run as root.  So invoke this shell script
# using sudo.

bwnet=10
delay=50 # RTT = 200ms
timestamp=$(date +"%d-%H-%M-%S")

# Figure 3 experiments
for loss in 0 0.5 1 2; do
  dir=result/$timestamp/loss_$loss
  python spdy.py -b $bwnet -d $dir --delay $delay --loss $loss
done

declare -a arr=("100B64" "1K64" "10K64" "100K64")
for i in "${arr[@]}"; do
  dir=result/$timestamp/objsize_$i
  echo $i
  python spdy.py -b $bwnet -d $dir --delay $delay --dg $i
done

declare -a arr=("10K2" "10K8" "10K16" "10K32" "10K64" "10K128")
for i in "${arr[@]}"; do
  dir=result/$timestamp/objnum_$i
  echo $i
  python spdy.py -b $bwnet -d $dir --delay $delay --dg $i
done

# graph the results for Figure 3
python figure3_plot.py -d result/$timestamp/ -o result/$timestamp

Figure 7 experiments
for graph in dg/www*/; do
    graph=${graph%*/}
    graph=${graph##*/}
    dir=result/$timestamp/retransmissions/$graph
    python spdy.py -b $bwnet -d $dir --delay $delay --dg $graph
done
echo $timestamp
