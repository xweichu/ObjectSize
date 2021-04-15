import os
thread_nums = [4, 16, 64, 256]
obj_sizes = [64*1024, 256*1024,  1024*1024, 4*1024*1024, 16*1024*1024, 64*1024*1024]
read_data_sizes = [4*1024, 16*1024, 64*1024, 256*1024 , 1024*1024, 4*1024*1024, 16*1024*1024]

for obj_size in obj_sizes:
    for read_data_size in read_data_sizes:
        for thread_num in thread_nums:
            if read_data_size < obj_size:
                os.system('python3 read_test.py %s %s %s %s > %s' %(str(obj_size), str(read_data_size),str(thread_num), 0 , str(obj_size)+ '_' + str(read_data_size) + '_' + str(thread_num)))


re = open('result', 'w+')
for obj_size in obj_sizes:
    for read_data_size in read_data_sizes:
        for thread_num in thread_nums:
            if read_data_size < obj_size:
                f = open(str(obj_size)+ '_' + str(read_data_size) + '_' + str(thread_num))
                lines = f.readlines()
                total_bandwidth = float(lines[0])
                re.write(str(obj_size)+ ',' + str(read_data_size) + ',' + str(thread_num) + ',' + str(total_bandwidth) + '\n')
