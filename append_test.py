import time
import rados
from multiprocessing import Process, Value, Pool
import os
import sys

# agrs populate object size, append data size, thread number, time ) 
def populate_objects_t(prefix, bts, tm):
    cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
    cluster.connect()
    ioctx = cluster.open_ioctx('scbench')
    i = 0 
    start_time = time.time()
    while True:
        ioctx.write_full(prefix + str(i), bts)
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > tm:
            ioctx.close()
            cluster.shutdown()
            break
        i = i + 1
    # print(prefix + ' populated ' + str(i + 1) + ' objects with size '+ str(len(bts)) + ' bytes, and the bandwith is ' + str( (i+1)*len(bts) / (time.time() -start_time )/ 1024/1024) + ' MB/s')
    # print(prefix + ',' + str(i+1) + ',' + str((i+1)*len(bts) / (time.time() -start_time )/ 1024/1024))


def populate_objects(obj_size, thread_num, tm):
    f = open('./data', 'rb')
    bts = f.read()
    bts = bts[0:obj_size]

    process_target = populate_objects_t
    processes = []

    for i in range(thread_num):
        p = Process(target=process_target, args=('Thread_' + str(i), bts, tm))
        processes.append(p)
        p.start()
    
    # print('Thread Name, Number of objects populated, Bandwidth(MB/s)')
    for p in processes:
        p.join()


def append_data_to_objects_t(prefix, bts, tm):

    cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
    cluster.connect()
    ioctx = cluster.open_ioctx('scbench')
    i = 0 
    start_time = time.time()
    while True:
        try:
            ioctx.stat(prefix + str(i))
            ioctx.append(prefix + str(i), bts)
            i = i + 1
            elapsed_time = time.time() - start_time
            if elapsed_time > tm:
                ioctx.close()
                cluster.shutdown()
                break
        except Exception as e:
            return ((i)*len(bts))

    return ((i)*len(bts))


def append_data_to_objects(append_size, thread_num, tm):
    f = open('./data', 'rb')
    bts = f.read()
    bts = bts[0:append_size]

    process_target = append_data_to_objects_t
    pl = Pool(thread_num)
    arguments = []

    for i in range(thread_num):
        arguments.append(('Thread_' + str(i), bts, tm))
    
    start = time.time()
    results = pl.starmap(process_target,arguments)
    stop = time.time()

    print(sum(results)/(stop-start)/1024/1024)


os.system('ceph osd pool delete scbench scbench --yes-i-really-really-mean-it')
os.system('ceph osd pool create scbench 128 128')
time.sleep(10)
populate_objects(int(sys.argv[1]), int(sys.argv[3]), 20)
time.sleep(3)
append_data_to_objects(int(sys.argv[2]), int(sys.argv[3]), 20)
