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
        print('Error: WrongFileExtension')
        return None
    
    time = list()
    npoints = list()
    xPointsList = list()
    yPointsList = list()
    xpoints = None;
    ypoints = None;
    i=0
    j=0

    #Format abfrage noch inkludieren (erste zeile) und ob j==npoints
    for line in file:
        if 'surface:' in line:
            stringArray = line.split(' ')
            time.append(float(stringArray[1]))
            npoints.append(int(stringArray[2]))
            xpoints = np.empty(npoints[i], dtype=np.float64)
            ypoints = np.empty(npoints[i], dtype=np.float64)
            xPointsList.append(xpoints)
            yPointsList.append(ypoints)
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
            xpoints[j] = float(stringArray[0])
            ypoints[j] = float(stringArray[1])
            j=j+1
    
    file.close()

    return xPointsList, yPointsList, time


def on_key_press(event):
    print('you pressed', event.key)
    return None

def plot_interactive(xval, yval, time):
    fig = plt.figure()
    fig.canvas.mpl_connect('key_press_event', on_key_press)
    plt.title('Time = ' + str(time[0]) + 's')
    plt.plot(xval[0],yval[0])
    plt.show()
    
def plot_all_srf(xval, yval,time ):
    for x in range(len(xval)):
        plt.figure(x)
        plt.title('Time = ' + str(time[x]) + 's')
        plt.plot(xval[x],yval[x])
    return None

    


if __name__ == '__main__':
    xval, yval, time = read_srf_file('trench.srf_save')
    #plot_all_srf(xval, yval, time)
    plot_interactive(xval,yval, time)

#%%
