#!/usr/bin/env python3

with open('t', 'w') as f:
    for i in range(0, 10000000):
        f.write('wow' + str(i))

with open('/dev/shm/t', 'w') as f:
    for i in range(0, 10000000):
        f.write('wow' + str(i))
