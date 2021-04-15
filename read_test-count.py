import time
import rados
import random
from multiprocessing import Process, Value, Pool
import os
import sys

# agrs populate object size, append data size, thread number, time ) 
def populate_objects_t(prefix, bts):
    cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')

    cluster.connect()
    ioctx = cluster.open_ioctx('scbench')
    i = 0 
    start_time = time.time()

    for i in range(1600):
        ioctx.write_full(prefix + str(i), bts)


def populate_objects(obj_size, thread_num):
    f = open('./data', 'rb')
    bts = f.read()
    bts = bts[0:obj_size]

    process_target = populate_objects_t
    processes = []

    for i in range(thread_num):
        p = Process(target=process_target, args=('Thread_' + str(i), bts))
        processes.append(p)
        p.start()
    
    # print('Thread Name, Number of objects populated, Bandwidth(MB/s)')
    for p in processes:
        p.join()


def read_data_to_objects_t(prefix, length, obj_size):

    cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
    cluster.connect()
    ioctx = cluster.open_ioctx('scbench')

    i = 0 
    total_bytes = 0 

    for i in range(1600):
        offset = random.randint(0,int(obj_size/length)) * length
        bts = ioctx.read(prefix + str(i), length, offset)
        if len(bts) == length:
            total_bytes = total_bytes + len(bts)

    return total_bytes


def read_data_to_objects(length, thread_num, obj_size):

    process_target = read_data_to_objects_t
    pl = Pool(thread_num)
    arguments = []

    for i in range(thread_num):
        arguments.append(('Thread_' + str(i), length, obj_size))
    
    start = time.time()
    results = pl.starmap(process_target,arguments)
    stop = time.time()

    print(sum(results)/(stop-start)/1024/1024)


os.system('ceph osd pool delete scbench scbench --yes-i-really-really-mean-it')
os.system('ceph osd pool create scbench 128 128')
time.sleep(10)
populate_objects(int(sys.argv[1]), int(sys.argv[3]))
time.sleep(5)
read_data_to_objects(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[1]))
time.sleep(5)
