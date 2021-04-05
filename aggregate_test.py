

f = open('test')
lines = f.readlines()
total_objects = 0
total_bandwidth = 0
for line in lines:
    parts = line.split(',')
    obj_num = int(parts[1])
    total_objects = total_objects + obj_num
    bandwidth = float(parts[2])
    total_bandwidth = total_bandwidth + bandwidth

re.write('test' + ':' + 'Total objects created: %d, aggregated bandwidth is: %f MB/s \n' % (total_objects, total_bandwidth))
print('Total objects created: %d, aggregated bandwidth is: %f MB/s' % (total_objects, total_bandwidth))