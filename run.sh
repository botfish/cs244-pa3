#!/bin/bash

# Note: Mininet must be run as root.  So invoke this shell script
# using sudo.

bwnet=10
delay=50 # RTT = 200ms
timestamp=$(date +"%d-%H-%M-%S")

for loss in 0 0.5 1 2; do
# for loss in 0 ; do
  dir=result/$timestamp/loss_$loss
  dg=10K64
  # Run spdy.py here...
  python spdy.py -b $bwnet -d $dir --dg $dg --delay $delay --loss $loss

  # Graphs go in the root folder, based on names in the assignment
  # python plot_tcpprobe.py -f $dir/cwnd.txt -o cwnd-q$qsize.png -p $iperf_port
  # python plot_queue.py -f $dir/q.txt -o buffer-q$qsize.png
  # python plot_ping.py -f $dir/ping.txt -o rtt-q$qsize.png
done
