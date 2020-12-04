import numpy as np
from time import time as t


Start_Time = t()
x = np.array((0.0, 1.0, 2.0, 1.0, 2.3, 5.0, 6.0))
y = np.array((5.0, 5.5, 5.3, 4.0, 6.5, 5.0, 6.0))

p = np.transpose(np.concatenate((x, y)).reshape((2, 7)))
print(p)
print(np.size(p))
intervall = np.arange(2,4)
print('Intervall = {}'.format(intervall))
print(np.delete(p, intervall, 0))
i=0
print(np.array((3, 4)))
test = np.array((3, 4))
test = np.reshape(test,(1, 2))
print(test.shape)
while i < 10000:
    i += 1

newpoint = np.array([99, 99])
print(newpoint)

p = np.insert(p, 2, newpoint, axis=0)
print(p)

#intervall = np.arange(3, 5)
#for point in intervall:
#    print(point)
#    deloopedsurface = np.delete(p, point)
#    print(deloopedsurface)
#    print('XXXXXXXXXXXXXXXXXXXXXX')
print('Size of p = {}'.format(np.size(p)/2))


testbool = True
print(testbool)
testbool = False
print(testbool)

Stop_Time = t()
print('++++++++++++++++')
print(Stop_Time-Start_Time)
print('//////////////////////')
print(x)
x = np.delete(x, (1,3,5),axis=0)
print(x)