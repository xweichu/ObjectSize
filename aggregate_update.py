import os
thread_nums = [4,8,16,32,64,128]
obj_sizes = [64*1024, 256*1024,  1024*1024, 4*1024*1024, 16*1024*1024, 64*1024*1024]
update_data_sizes = [4*1024, 16*1024, 64*1024, 256*1024 , 1024*1024, 4*1024*1024, 16*1024*1024]

for obj_size in obj_sizes:
    for thread_num in thread_nums:
        os.system('python3 populate_data.py %s %s %s' %(str(obj_size), str(thread_num), str(60)))
        for update_data_size in update_data_sizes:
            if update_data_size < obj_size:
                # update_size, thread num, object size , object num
                os.system('python3 update_test.py %s %s %s %s > %s' % (str(update_data_size), str(thread_num), str(obj_size), str(60) , str(obj_size)+ '_' + str(update_data_size) + '_' + str(thread_num)))


re = open('result', 'w+')
for obj_size in obj_sizes:
    for update_data_size in update_data_sizes:
        for thread_num in thread_nums:
            if update_data_size < obj_size:
                f = open(str(obj_size)+ '_' + str(update_data_size) + '_' + str(thread_num))
                lines = f.readlines()
                total_bandwidth = float(lines[0])
                re.write(str(obj_size)+ ',' + str(update_data_size) + ',' + str(thread_num) + ',' + str(total_bandwidth) + '\n')
