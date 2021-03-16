
data_path = '/Users/xweichu/Desktop/OSD0/'
PG_NUMs = [8,16,32,64,128,256]
Object_Sizes=['4K', '16K', '64K', '256K', '1M', '4M', '16M', '64M']
Threads_NUMs= [32,64,128,256,512,1024]

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


f = open('/Users/xweichu/Desktop/osd0_result.csv','w')
for result in results:
    f.write(str(result[0]) + ',' + str(result[1]) + ',' + str(result[2]) + ',' + str(result[3]) + '\n')

f.close()

            