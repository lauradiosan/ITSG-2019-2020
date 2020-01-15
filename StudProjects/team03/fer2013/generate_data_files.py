import numpy as np

def getY(index):
    t = [0, 0, 0, 0, 0, 0, 0]
    t[index] = 1
    return t

with open('generated.csv') as f:
    lines = f.readlines()[1:]
    x = []
    y = []
    for line in lines:
        q = line.split(',')
        nrs = list(map(float, q[1].split(' ')))
        a = []
        for i in range(48):
            a1 = []
            for j in range(48):
                a1.append([nrs[i * 48 + j]])
            a.append(a1)
        x.append(a)
        y.append(getY(int(q[0])))
    x = np.array(x)
    y = np.array(y)
    np.save('dataX.npy', x)
    np.save('dataY.npy', y)
