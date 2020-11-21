#%%
import numpy as np
import matplotlib.pyplot as plt
import os


def read_srf_file(filename):
    try:
        file = open(filename)
    except FileNotFoundError:
        print("Error: FileNotFound")
        return None
    
    if (filename.endswith(('.srf_save', '.srf')) == False):
        print('Error: WrongFileEnding')
        return None
    
    time = list()
    npoints = list()
    xpoints = list()
    ypoints = list()
    xpoint = None;
    ypoint = None;
    i=0
    j=0

    for line in file:
        if 'surface:' in line:
            stringArray = line.split(' ')
            time.append(float(stringArray[1]))
            npoints.append(int(stringArray[2]))
            xpoint = np.empty(npoints[i], dtype=np.float64)
            ypoint = np.empty(npoints[i], dtype=np.float64)
            xpoints.append(xpoint)
            ypoints.append(ypoint)
            #print(xpoints)

            #print(stringArray)
            #print(time)
            #print(npoints)
            #if i==1:
               # break
            i=i+1
            j=0
        else:
            stringArray = line.split(' ')
            xpoint[j] = float(stringArray[0])
            ypoint[j] = float(stringArray[1])
            j=j+1

    return xpoints, ypoints

    

    
def plot_srf(xval, yval):
    
    for x in range(len(xval)):
        plt.figure(x)
        plt.plot(xval[x],yval[x])
    return None

    


if __name__ == '__main__':
    xval, yval = read_srf_file('trench.srf_save')
    plot_srf(xval, yval)

# %%
