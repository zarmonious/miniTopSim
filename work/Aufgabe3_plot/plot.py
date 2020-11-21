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
        self.currentSurface = 0;
        self.forwardDirectory = True;
        self.length = 0
        self.aspectRatioAuto = True;
        plt.rcParams['keymap.fullscreen'] = ['ctrl+f']
        plt.rcParams['keymap.yscale'] = ['ctrl+l']
        plt.rcParams['keymap.home'] = ['h','home']
        plt.rcParams['keymap.all_axes'] = ''
        plt.rcParams['keymap.save'] = ['ctrl+s']
        plt.rcParams['keymap.quit'] = ['ctrl+w','cmd+w']

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
        self.length = i
        file.close()

        return True


    def on_key_press(self, event):

        if(event.key == 'l'):
            plt.clf()
            lastElementIndex = self.length - 1
            self.currentSurface = lastElementIndex
            plt.plot(self.xPointsList[lastElementIndex], self.yPointsList[lastElementIndex])
            plt.title('Time = ' + str(self.timeList[lastElementIndex]) + 's')
            event.canvas.draw()


        elif(event.key == 'f'):
            plt.clf()
            self.currentSurface = 0
            plt.plot(self.xPointsList[0], self.yPointsList[0])
            plt.title('Time = ' + str(self.timeList[0]) + 's')
            event.canvas.draw()
        

        elif(event.key == ' '):
            if(self.forwardDirectory == True):
                self.currentSurface = self.currentSurface + 1
                if(self.currentSurface == self.length):
                    self.currentSurface = 0

            else:
                self.currentSurface = self.currentSurface -1
                if(self.currentSurface == -1):
                    self.currentSurface == self.length -1
            plt.clf()
            plt.plot(self.xPointsList[self.currentSurface], self.yPointsList[self.currentSurface])
            plt.title('Time = ' + str(self.timeList[self.currentSurface]) + 's')
            event.canvas.draw()


        elif(event.key == 'r'):
            self.forwardDirectory = not self.forwardDirectory

        #WIP
        elif(event.key == 'a'):
            #plt.axes().set_aspect('auto', 'box')
            return 
        
        elif(event.key == 'd'):
            return

        
        elif(event.key == 's'):
            return
        
        elif(event.key == 'b'):
            return

        
        elif(event.key == 'q'):
            return
        
        elif(event.key.isnumeric() == True):
            return

        else:
            return  None





        
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
        for x in range(self.length):
            plt.figure(x)
            plt.title('Time = ' + str(self.timeList[x]) + 's')
            plt.plot(self.xPointsList[x],self.yPointsList[x])
            #plt.show()
        return None

    

def plot(filename):
    plotter = SurfacePlotter(filename)
    plotter.plot_interactive()


#add sys.argv
if __name__ == '__main__':
    plot('trench.srf_save')


#%%
