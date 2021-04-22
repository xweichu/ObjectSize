import time
import rados
from multiprocessing import Process, Value, Pool
import os
import sys
import random


def read_data_to_objects_t(prefix, length, obj_size, object_num):

    cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
    cluster.connect()
    ioctx = cluster.open_ioctx('scbench')

    total_bytes = 0 

    for i in range(object_num):

        offset = random.randint(0,int(obj_size/length)-1) * length
        ioctx.read(prefix + str(i), length, offset)
        total_bytes = total_bytes + length 


    return total_bytes


def read_data_to_objects(read_size, thread_num, obj_size, object_num):

    process_target = read_data_to_objects_t
    pl = Pool(thread_num)
    arguments = []

    for i in range(thread_num):
        arguments.append(('Thread_' + str(i), read_size, obj_size, object_num))
    
    start = time.time()
    results = pl.starmap(process_target,arguments)
    stop = time.time()

    print(sum(results)/(stop-start)/1024/1024)


time.sleep(5)
# read_size, thread num, object size , object num
read_data_to_objects(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))