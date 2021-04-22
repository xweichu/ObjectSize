import os
thread_nums = [64]
obj_sizes = [16*1024*1024]
update_data_sizes = [16*1024, 256*1024 , 4*1024*1024]

offsets = []
for i in range(12):
    offsets.append(1024*i)


for obj_size in obj_sizes:
    for thread_num in thread_nums:
        os.system('python3 populate_data.py %s %s %s' %(str(obj_size), str(thread_num), str(25)))
        for update_data_size in update_data_sizes:
            for offset in offsets:
                if update_data_size < obj_size:
                    # update_size, thread num, object size , object num
                    os.system('python3 not_align_update.py %s %s %s %s %s > %s' % (str(update_data_size), str(thread_num), str(obj_size), str(25) ,str(offset), str(obj_size)+ '_' + str(update_data_size) + '_' + str(thread_num) + '_' + str(offset)))


re = open('result', 'w+')
for obj_size in obj_sizes:
    for update_data_size in update_data_sizes:
        for thread_num in thread_nums:
            for offset in offsets:
                if update_data_size < obj_size:
                    f = open(str(obj_size)+ '_' + str(update_data_size) + '_' + str(thread_num) + '_' + str(offset))
                    lines = f.readlines()
                    total_bandwidth = float(lines[0])
                    re.write(str(obj_size)+ ',' + str(update_data_size) + ',' + str(thread_num) + ',' + str(offset) + ',' + str(total_bandwidth) + '\n')
