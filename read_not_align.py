import os
thread_nums = [64]
obj_sizes = [16*1024*1024]
read_data_sizes = [16*1024, 256*1024, 4*1024*1024]

offsets = []
for i in range(20):
    offset = 1024 * i
    offsets.append(offset)

for obj_size in obj_sizes:
    for read_data_size in read_data_sizes:
        for thread_num in thread_nums:
            for offset in offsets:
                os.system('python3 read_test.py %s %s %s %s > %s' %(str(obj_size), str(read_data_size), str(thread_num), str(offset) , str(obj_size)+ '_' + str(read_data_size) + '_' + str(thread_num)+'_'+str(offset)))


re = open('result_not_align', 'w+')
for obj_size in obj_sizes:
    for read_data_size in read_data_sizes:
        for thread_num in thread_nums:
            for offset in offsets:
                f = open(str(obj_size)+ '_' + str(read_data_size) + '_' + str(thread_num)+'_'+str(offset))
                lines = f.readlines()
                total_bandwidth = float(lines[0])
                re.write(str(obj_size)+ ',' + str(read_data_size) + ',' + str(offset) + ',' + str(total_bandwidth) + '\n')