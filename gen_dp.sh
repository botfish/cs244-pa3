#!/bin/bash
time=10
dtime=10
rm -rf dg/100B64.com_/
rm -rf dg/1K64.com_/
rm -rf dg/10K64.com_/
rm -rf dg/100K64.com_/
rm -rf dg/10K2.com_/
rm -rf dg/10K8.com_/
rm -rf dg/10K16.com_/
rm -rf dg/10K32.com_/
rm -rf dg/10K64.com_/
rm -rf dg/10K128.com_/
python gen_dp.py -S -1 -N 64 -O dg/100B64.com_/ -T $time -DT $dtime
python gen_dp.py -S 1 -N 64 -O dg/1K64.com_/ -T $time -DT $dtime
python gen_dp.py -S 10 -N 64 -O dg/10K64.com_/ -T $time -DT $dtime
python gen_dp.py -S 100 -N 64 -O dg/100K64.com_/ -T $time -DT $dtime
python gen_dp.py -S 10 -N 2 -O dg/10K2.com_/ -T $time -DT $dtime
python gen_dp.py -S 10 -N 8 -O dg/10K8.com_/ -T $time -DT $dtime
python gen_dp.py -S 10 -N 16 -O dg/10K16.com_/ -T $time -DT $dtime
python gen_dp.py -S 10 -N 32 -O dg/10K32.com_/ -T $time -DT $dtime
python gen_dp.py -S 10 -N 64 -O dg/10K64.com_/ -T $time -DT $dtime
python gen_dp.py -S 10 -N 128 -O dg/10K128.com_/ -T $time -DT $dtime
# python gen_dp.py -S -1 -N 64 -O dg/100B64.com_/
# python gen_dp.py -S 1 -N 64 -O dg/1K64.com_/
# python gen_dp.py -S 10 -N 64 -O dg/10K64.com_/
# python gen_dp.py -S 100 -N 64 -O dg/100K64.com_/
# python gen_dp.py -S 10 -N 2 -O dg/10K2.com_/
# python gen_dp.py -S 10 -N 8 -O dg/10K8.com_/
# python gen_dp.py -S 10 -N 16 -O dg/10K16.com_/
# python gen_dp.py -S 10 -N 32 -O dg/10K32.com_/
# python gen_dp.py -S 10 -N 64 -O dg/10K64.com_/
# python gen_dp.py -S 10 -N 128 -O dg/10K128.com_/
