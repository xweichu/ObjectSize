
data_path = '/Users/xweichu/Desktop/read_project_HDD/'
# PG_NUMs = [8,16,32,64,128,256]
PG_NUMs = [128]
Object_Sizes=['4K', '16K', '64K', '256K', '1M', '4M', '16M', '64M']
Threads_NUMs= [4, 8, 16, 32 , 64 , 128 , 256, 384]

results = []

for PG_NUM in PG_NUMs:
    for Threads_NUM in Threads_NUMs:
        for Object_Size in Object_Sizes:
            file_name = data_path + 'R_PG_' + str(PG_NUM) + '_T_' + str(Threads_NUM) + '_S_' + Object_Size
            f = open(file_name)
            lines = f.readlines()
            result = []
            result.append(PG_NUM)
            result.append(Threads_NUM)
            if Object_Size == '1M':
                result.append('1024K')
            elif Object_Size == '4M':
                result.append('4096K')
            elif Object_Size == '16M':
                result.append('16384K')
            elif Object_Size == '64M':
                result.append('65536K')
            else:
                result.append(Object_Size)

            for line in lines:
                if 'Bandwidth (MB/sec)' in line:
                    parts = line.split(' ')
                    result.append(float(parts[-1][0:-1]))
            
            results.append(result)


f = open('/Users/xweichu/Desktop/read_hdd_result.csv','w')
f.write('PGs Number, Threads Number, Object Size(KB), Bandwidth(MB/s)\n')
for result in results:
    f.write(str(result[0]) + ',' + str(result[1]) + ',' + str(result[2][0:-1]) + ',' + str(result[3]) + '\n')

f.close()

            