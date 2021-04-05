import time
import rados
import sys
import threading
from multiprocessing import Process
import os

def append_data(name, bts, ceph_pool):

    try:
        cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
        cluster.connect()
        ioctx = cluster.open_ioctx(ceph_pool)
        ioctx.append(name, bts)
        ioctx.close()
        cluster.shutdown()
    except Exception as e:
        return str(e)

    return True


def write_partial_data(name, bts, data_offset, ceph_pool):

    try:
        cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
        cluster.connect()
        ioctx = cluster.open_ioctx(ceph_pool)
        ioctx.write(name, data = bts, offset = data_offset)
        ioctx.close()
        cluster.shutdown()
    except Exception as e:
        return str(e)

    return True


def write_data(buff_bytes, name,  ceph_pool):

    try:
        cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
        cluster.connect()
        ioctx = cluster.open_ioctx(ceph_pool)
        ioctx.write_full(name, buff_bytes)
        ioctx.close()
        cluster.shutdown()
    except Exception as e:
        return str(e)

    return True

def read_data(name, data_len, data_offset, ceph_pool):
    try:
        cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
        cluster.connect()
        ioctx = cluster.open_ioctx(ceph_pool)
        data = ioctx.read(name, length = data_len, offset = data_offset)
        ioctx.close()
        cluster.shutdown()
        return data
    except Exception as e:
        #print(e)
        return str(e)
    return None

def remove_data(name, ceph_pool):
    try:
        cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
        cluster.connect()
        ioctx = cluster.open_ioctx(ceph_pool)
        ioctx.remove_object(name)
        ioctx.close()
        cluster.shutdown()
    except Exception as e:
        return str(e)

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
            ioctx.append(prefix + str(i), bts)
            i = i + 1
            elapsed_time = time.time() - start_time
            if elapsed_time > tm:
                ioctx.close()
                cluster.shutdown()
                break
        except Exception as e:
            print(str(e))
            print(prefix + ',' + str(i) + ',' + str((i)*len(bts) / (time.time() -start_time )/ 1024/1024))
            return str(e)
    print(prefix + ',' + str(i) + ',' + str((i)*len(bts) / (time.time() -start_time )/ 1024/1024))

def append_data_to_objects(append_size, thread_num, tm):
    f = open('./data', 'rb')
    bts = f.read()
    bts = bts[0:append_size]

    process_target = append_data_to_objects_t
    processes = []

    for i in range(thread_num):
        p = Process(target=process_target, args=('Thread_' + str(i), bts, tm))
        processes.append(p)
        p.start()
    
    # print('Thread Name, Number of objects populated, Bandwidth(MB/s)')
    for p in processes:
        p.join()

os.system('ceph osd pool delete scbench scbench --yes-i-really-really-mean-it')
os.system('ceph osd pool create scbench 128 128')
time.sleep(10)
populate_objects(int(sys.argv[1]), int(sys.argv[3]), 60)
time.sleep(10)
append_data_to_objects(int(sys.argv[2]), int(sys.argv[3]), 60)
