import numpy as np



x = np.array((0.0, 1.0, 2.0, 1.0, 2.3, 5.0, 6.0))
y = np.array((5.0, 5.5, 5.3, 4.0, 6.5, 5.0, 6.0))

p = np.transpose(np.concatenate((x, y)).reshape((2, 7)))
print(p)
intervall = np.arange(2,4)
print('Intervall = {}'.format(intervall))
print(np.delete(p, intervall, 0))

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

