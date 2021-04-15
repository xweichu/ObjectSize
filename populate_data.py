import time
import rados
import random
from multiprocessing import Process, Value, Pool
import os
import sys
# agrs populate object size, append data size, thread number, time ) 
def populate_objects_t(prefix, bts, object_num):
    cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')

    cluster.connect()
    ioctx = cluster.open_ioctx('scbench')
    i = 0 
    start_time = time.time()

    for i in range(object_num):
        ioctx.write_full(prefix + str(i), bts)


def populate_objects(obj_size, thread_num, object_num):
    f = open('./data', 'rb')
    bts = f.read()
    bts = bts[0:obj_size]

    process_target = populate_objects_t
    processes = []

    for i in range(thread_num):
        p = Process(target=process_target, args=('Thread_' + str(i), bts, object_num))
        processes.append(p)
        p.start()
    
    # print('Thread Name, Number of objects populated, Bandwidth(MB/s)')
    for p in processes:
        p.join()

# Object Size, Thread Num, Object Num
populate_objects(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
