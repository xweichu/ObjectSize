import os
thread_nums = [4, 16, 64, 256]
obj_sizes = [4*1024, 64*1024, 1024*1024, 16*1024*1024, 64*1024*1024]
append_data_sizes = [4*1024, 64*1024, 1024*1024, 16*1024*1024, 64*1024*1024]

for obj_size in obj_sizes:
    for append_data_size in append_data_sizes:
        for thread_num in thread_nums:
            os.system('python3 append_test.py %s %s %s > %s' %(str(obj_size), str(append_data_size),str(thread_num) , str(obj_size)+ '_' + str(append_data_size) + '_' + str(thread_num)))


re = open('result', 'w+')
for obj_size in obj_sizes:
    for append_data_size in append_data_sizes:
        for thread_num in thread_nums:
            f = open(str(obj_size)+ '_' + str(append_data_size) + '_' + str(thread_num))
            lines = f.readlines()
            total_bandwidth = float(lines[0])
            re.write(str(obj_size)+ ',' + str(append_data_size) + ',' + str(thread_num) + ',' + str(total_bandwidth) + '\n')
