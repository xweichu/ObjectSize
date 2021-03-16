
data_path = '/Users/xweichu/Desktop/not_align_4MB/'

run_time = 20
PG_NUMs = [128]
Threads_NUMs= [128]

sizes = []
for i in range(32):
    sizes.append(4096 + 4*i)

Object_Sizes = []
for size in sizes:
    Object_Sizes.append(str(size) + 'K')

results = []

for PG_NUM in PG_NUMs:
    for Threads_NUM in Threads_NUMs:
        for Object_Size in Object_Sizes:
            file_name = data_path + 'PG_' + str(PG_NUM) + '_T_' + str(Threads_NUM) + '_S_' + Object_Size
            f = open(file_name)
            lines = f.readlines()
            result = []
            result.append(PG_NUM)
            result.append(Threads_NUM)
            result.append(Object_Size)
            for line in lines:
                if 'Bandwidth (MB/sec)' in line:
                    parts = line.split(' ')
                    result.append(float(parts[-1][0:-1]))
            
            results.append(result)


f = open('/Users/xweichu/Desktop/not_aligned_HDD_4M_result.csv','w')
for result in results:
    f.write(str(result[0]) + ',' + str(result[1]) + ',' + str(result[2]) + ',' + str(result[3]) + '\n')

f.close()

            