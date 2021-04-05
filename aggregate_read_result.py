import os
obj_sizes = [64*1024*1024]
read_sizes = [4*1024, 16*1024, 64*1024, 256*1024, 1024*1024, 4*1024*1024, 16*1024*1024]

for obj_size in obj_sizes:
    for read_size in read_sizes:
        os.system('python3 partial_read.py %s %s > %s' %(str(obj_size), str(read_size), str(obj_size) + '_' + str(read_size)))


re = open('result', 'w+')
for obj_size in obj_sizes:
    for read_size in read_sizes:

        f = open(str(obj_size)+ '_' + str(read_size))
        lines = f.readlines()
        total_objects = 0
        total_bandwidth = 0
        for line in lines:
            parts = line.split(',')
            obj_num = int(parts[1])
            total_objects = total_objects + obj_num
            bandwidth = float(parts[2])
            total_bandwidth = total_bandwidth + bandwidth

        re.write(str(obj_size)+ '_' + str(read_size) + ':' + 'Total objects created: %d, aggregated bandwidth is: %f MB/s \n' % (total_objects, total_bandwidth))
        # print('Total objects created: %d, aggregated bandwidth is: %f MB/s' % (total_objects, total_bandwidth))
