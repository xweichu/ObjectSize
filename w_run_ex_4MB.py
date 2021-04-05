import time
import rados
import sys
import threading
from multiprocessing import Process


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


f = open('./test', 'rb')
bts = f.read()
bts = bts[0:4194304]

for i in range(256):
    re = write_data(bts,'test' + str(i),'scbench')

time.sleep(10)

worker_num = 256 
start_time = time.time()
process_target = write_partial_data
processes = []


obj_name = 'test'
bts = bts[0:1048576]
data_offset = 0 
ceph_pool = 'scbench'

for i in range(worker_num):
    data_offset = 10
    p = Process(target=process_target, args=(obj_name + str(i), bts, data_offset, ceph_pool))
    processes.append(p)
    p.start()


# Wait for the workers to finish
for p in processes:
    p.join()


stop_time = time.time()

# Calculate and print the throughput
bandwidth = worker_num /(stop_time - start_time)
print('Read bandwidth: ' + str(bandwidth) + ' MB/s.')

