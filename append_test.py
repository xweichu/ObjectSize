import time
import rados
from multiprocessing import Process, Value, Pool
import os
import sys

def append_data_to_objects_t(prefix, bts, object_num):

    cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
    cluster.connect()
    ioctx = cluster.open_ioctx('scbench')

    total_bytes = 0 

    for i in range(object_num):
        ioctx.append(prefix + str(i), bts)
        total_bytes = total_bytes + len(bts) 


    return total_bytes


def append_data_to_objects(append_size, thread_num, object_num):
    f = open('./data', 'rb')
    bts = f.read()
    bts = bts[0:append_size]

    process_target = append_data_to_objects_t
    pl = Pool(thread_num)
    arguments = []

    for i in range(thread_num):
        arguments.append(('Thread_' + str(i), bts, object_num))
    
    start = time.time()
    results = pl.starmap(process_target,arguments)
    stop = time.time()

    print(sum(results)/(stop-start)/1024/1024)


time.sleep(5)
# append_size, thread num, object size , object num
append_data_to_objects(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))