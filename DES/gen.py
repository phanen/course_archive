# import random
# random.randrange(2**64)

from bitarray import bitarray
a = bytearray(b'')
b = bytearray([1, 2, 3])
c = bytearray(b'\x01\x02\x03')
d = bytearray('runoob', 'utf-8')
e = bytearray(b'runoob')
print(a)
print(b)
print(c)
print(d)
print(e)
for i in d:
    print(i)
for i in e:
    print(i)
