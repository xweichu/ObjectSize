import os
thread_nums = [64]
obj_sizes = [16*1024*1024]
read_data_sizes = [16*1024, 256*1024 , 4*1024*1024]

offsets = []
for i in range(65):
    offsets.append(1024*i)


for obj_size in obj_sizes:
    for thread_num in thread_nums:
        os.system('python3 populate_data.py %s %s %s' %(str(obj_size), str(thread_num), str(10)))
        for read_data_size in read_data_sizes:
            for offset in offsets:
                if read_data_size < obj_size:
                    # read_size, thread num, object size , object num
                    os.system('python3 not_align_read.py %s %s %s %s %s > %s' % (str(read_data_size), str(thread_num), str(obj_size), str(10) ,str(offset), str(obj_size)+ '_' + str(read_data_size) + '_' + str(thread_num) + '_' + str(offset)))


re = open('result', 'w+')
for obj_size in obj_sizes:
    for read_data_size in read_data_sizes:
        for thread_num in thread_nums:
            for offset in offsets:
                if read_data_size < obj_size:
                    f = open(str(obj_size)+ '_' + str(read_data_size) + '_' + str(thread_num) + '_' + str(offset))
                    lines = f.readlines()
                    total_bandwidth = float(lines[0])
                    re.write(str(obj_size)+ ',' + str(read_data_size) + ',' + str(thread_num) + ',' + str(offset) + ',' + str(total_bandwidth) + '\n')
