import os
import sys

source_file = sys.argv[1]
output_file = sys.argv[2]

os.system('grep PG4lock '+ source_file  +' -B 6 -C 6 > lock_addresses')
os.system('grep lock_contended lock_addresses > lock_addresses.1')
os.system('mv lock_addresses.1 lock_addresses')

f = open('lock_addresses')
lines = f.readlines()
pg_locks = set()
for line in lines:
    parts = line.split(',')
    pg_locks.add(parts[3][1:-1])

pg_locks = list(pg_locks)

total_acquires = {}
total_contended = {}
for pg_lock in pg_locks:
    os.system('grep lock_acquire ' + source_file + '|grep ' + pg_lock +' >' + pg_lock)
    f = open(pg_lock)
    lines = f.readlines()
    total_acquires[pg_lock] = len(lines)
    f.close()
    os.system('grep lock_contended ' + source_file + '|grep ' + pg_lock +' >' + pg_lock)
    f = open(pg_lock)
    lines = f.readlines()
    total_contended[pg_lock] = len(lines)
    f.close()
    os.system('sudo rm ' + pg_lock)

os.system('sudo rm lock_addresses')

os.system("grep 'Mutex Address' " + source_file + " -A 5000 >" + output_file)

avg_wait_time = {}

for pg_lock in pg_locks:
    f = open(output_file)
    lines = f.readlines()
    total_time = 0
    for line in lines:
        if pg_lock in line:
            parts = line.split(',')
            total_time = total_time +  int(parts[3])
    f.close()
    avg_time = total_time / total_contended[pg_lock]
    avg_wait_time[pg_lock] = avg_time



print(total_acquires)
print(total_contended)
print(avg_wait_time)

overall_total_acquires = 0
overall_total_contended = 0
overall_avg_wait_time = 0

total_wait_time = 0
for pg_lock in pg_locks:
    overall_total_acquires += total_acquires[pg_lock]
    overall_total_contended += total_contended[pg_lock]
    total_wait_time += avg_wait_time[pg_lock] * total_contended[pg_lock]

overall_avg_wait_time = total_wait_time / overall_total_contended

print('overall_total_acquires:' + str(overall_total_acquires))
print('overall_total_contended:' + str(overall_total_contended))
print('overall_contention_ratio:' + str(overall_total_contended/overall_total_acquires))
print('overall_avg_wait_time:' + str(overall_avg_wait_time))


