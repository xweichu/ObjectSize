import os
import sys
import time

run_time = 20
PG_NUMs = [128]
Threads_NUMs= [128]

sizes = []
for i in range(32):
    sizes.append(4096 + 4*i)

Object_Sizes = []
for size in sizes:
    Object_Sizes.append(str(size) + 'K')



for PG_NUM in PG_NUMs:
    for Threads_NUM in Threads_NUMs:
        for Object_Size in Object_Sizes:
            os.system('ceph osd pool create scbench ' + str(PG_NUM) + ' ' + str(PG_NUM))
            time.sleep(10)
            print('PG_' + str(PG_NUM) + '_T_' + str(Threads_NUM) + '_S_' + Object_Size)
            os.system('rados bench -p scbench -b ' + Object_Size + '  -t '+ str(Threads_NUM) +'  ' + str(run_time) + '  write --no-cleanup > PG_' + str(PG_NUM) + '_T_' + str(Threads_NUM) + '_S_' + Object_Size)
            os.system('rados cleanup -p scbench')
            os.system('ceph osd pool delete scbench scbench --yes-i-really-really-mean-it')
            