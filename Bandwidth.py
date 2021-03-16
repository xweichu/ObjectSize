import os
import sys
import time

run_time = 30
PG_NUMs = [8,16,32,64,128,256]
Object_Sizes=['4K', '16K', '64K', '256K', '1M', '4M', '16M', '64M']
Threads_NUMs= [32,64,128,256,512,1024]

for PG_NUM in PG_NUMs:
    for Threads_NUM in Threads_NUMs:
        for Object_Size in Object_Sizes:
            os.system('ceph osd pool create scbench ' + str(PG_NUM) + ' ' + str(PG_NUM))
            time.sleep(10)
            print('PG_' + str(PG_NUM) + '_T_' + str(Threads_NUM) + '_S_' + Object_Size)
            os.system('rados bench -p scbench -b ' + Object_Size + '  -t '+ str(Threads_NUM) +'  ' + str(run_time) + '  write --no-cleanup > PG_' + str(PG_NUM) + '_T_' + str(Threads_NUM) + '_S_' + Object_Size)
            os.system('rados cleanup -p scbench')
            os.system('ceph osd pool delete scbench scbench --yes-i-really-really-mean-it')
            