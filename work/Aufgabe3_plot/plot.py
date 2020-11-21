#%%
import numpy as np
import matplotlib.pyplot as plt
import os

class SurfacePlotter:

    def __init__(self, filename):
        self.filename = filename
        self.xPointsList = list()
        self.yPointsList = list()
        self.timeList = list()
        self.nPointList = list()

    def read_srf_file(self):
        try:
            file = open(self.filename)
        except FileNotFoundError:
            print("Error: FileNotFound")
            return None
        
        if (self.filename.endswith(('.srf_save', '.srf')) == False):
            print('Error: WrongFileExtension')
            return None
        
        xPoints = None;
        yPoints = None;
        i=0
        j=0

        #Format abfrage noch inkludieren (erste zeile) und ob j==npoints
        for line in file:
            if 'surface:' in line:
                stringArray = line.split(' ')
                self.timeList.append(float(stringArray[1]))
                self.nPointList.append(int(stringArray[2]))
                xPoints = np.empty(self.nPointList[i], dtype=np.float64)
                yPoints = np.empty(self.nPointList[i], dtype=np.float64)
                self.xPointsList.append(xPoints)
                self.yPointsList.append(yPoints)
                i=i+1
                j=0
            else:
                stringArray = line.split(' ')
                xPoints[j] = float(stringArray[0])
                yPoints[j] = float(stringArray[1])
                j=j+1
        
        file.close()

        return True


    def on_key_press(self, event):
        print('you pressed', event.key)
        return None

    def plot_interactive(self):
        self.read_srf_file()
        fig = plt.figure()
        fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        plt.title('Time = ' + str(self.timeList[0]) + 's')
        plt.plot(self.xPointsList[0], self.yPointsList[0])
        plt.show()

        
    #Only for Debugging purposes, 
    # will get removed when rest of project completed   
    def plot_all_srf(self):
        self.read_srf_file()
        for x in range(len(self.xPointsList)):
            plt.figure(x)
            plt.title('Time = ' + str(self.timeList[x]) + 's')
            plt.plot(self.xPointsList[x],self.yPointsList[x])
            #plt.show()
        return None

    

def plot(filename):
    plotter = SurfacePlotter(filename)
    plotter.plot_all_srf()


#add sys.argv
if __name__ == '__main__':
    plot('trench.srf_save')



#%%
