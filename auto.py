import os
import sys

source_file = sys.argv[1]
output_file = sys.argv[2]

os.system('grep PG4lock '+ source_file  +' -B 6 -C 6 > lock_addresses')
os.system('grep Callstack lock_addresses > lock_addresses.1')
os.system('mv lock_addresses.1 lock_addresses')

f = open('lock_addresses')
lines = f.readlines()
pg_locks = set()
for line in lines:
    parts = line.split(',')
    part = parts[3]
    parts = part.split(' ')
    part = parts[2]
    pg_locks.add(part)

overall_total_acquires_finisher = 0
overall_total_acquires_osd = 0
overall_total_contended_finisher = 0
overall_total_contended_osd = 0
overall_total_wait_time_finsiher = 0
overall_total_wait_time_osd = 0

f = open(source_file)
lines = f.readlines()
for line in lines:
    parts = line.split(',')
    if len(parts) != 4:
        continue
    parts = parts[3]
    if parts[1:-1] in pg_locks and 'lock_acquired' in line and 'finisher' in line:
        overall_total_acquires_finisher += 1
        continue
    if parts[1:-1] in pg_locks and 'lock_acquired' in line and 'tp_osd_tp' in line:
        overall_total_acquires_osd += 1
        continue
    if parts[1:-1] in pg_locks and 'lock_contended' in line and 'finisher' in line:
        overall_total_contended_finisher += 1
        continue
    if parts[1:-1] in pg_locks and 'lock_contended' in line and 'tp_osd_tp' in line:
        overall_total_contended_osd += 1
        continue

os.system('sudo rm lock_addresses')

os.system("grep 'Mutex Address' " + source_file + " -A 5000 >" + output_file)

pg_locks = list(pg_locks)
total_wait_time_finisher = {}
total_wait_time_osd = {}
for pg_lock in pg_locks:
    f = open(output_file)
    lines = f.readlines()
    total_time_finisher = 0
    total_time_osd = 0
    for line in lines:
        if pg_lock in line and 'finisher' in line:
            parts = line.split(',')
            total_time_finisher = total_time_finisher +  int(parts[3])
            continue
        if pg_lock in line and 'tp_osd_tp' in line:
            parts = line.split(',')
            total_time_osd = total_time_osd +  int(parts[3])
    f.close()
    total_wait_time_finisher[pg_lock] = total_time_finisher
    total_wait_time_osd[pg_lock] = total_time_osd


for pg_lock in pg_locks:
    overall_total_wait_time_finsiher += total_wait_time_finisher[pg_lock]
    overall_total_wait_time_osd += total_wait_time_osd[pg_lock]

print('Thread_Name, PG_lock_acquires, PG_lock_contentions, Total_wait_time, Average_wait_time')
if overall_total_wait_time_finsiher !=0:
    print('finisher,' + str(overall_total_acquires_finisher) + ',' + str(overall_total_contended_finisher)+ ',' +  str(overall_total_wait_time_finsiher)+ ',' +  str(overall_total_wait_time_finsiher/overall_total_contended_finisher))
else:
    print('finisher,' + str(overall_total_acquires_finisher) + ',' + str(overall_total_contended_finisher)+ ',' +  str(overall_total_wait_time_finsiher)+ ',' +  str(0))

if overall_total_wait_time_osd !=0:
    print('tp_osd_tp,' + str(overall_total_acquires_osd)+ ',' +  str(overall_total_contended_osd)+ ',' +  str(overall_total_wait_time_osd)+ ',' +  str(overall_total_wait_time_osd/overall_total_contended_osd))
else:
    print('tp_osd_tp,' + str(overall_total_acquires_osd)+ ',' +  str(overall_total_contended_osd)+ ',' +  str(overall_total_wait_time_osd)+ ',' +  str(0))

print('')
print('Number of PG locks used:' + str(len(pg_locks)))


