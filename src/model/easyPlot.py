'''
Created on 12/10/2017

@author: nathan
'''
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d, Axes3D


class dotsPlot2D(object):
    '''
    classdocs
    '''
    
    def __init__(self, title, xTitle, yTitle):
        '''
        Constructor
        '''
        fig, ax = plt.subplots();
        self.ax = ax;       
        plt.title(title);
        plt.xlabel(xTitle);
        plt.ylabel(yTitle);
        self.cont = 1;
      
    def addDot(self, x, y, group):
        #for d in data:            
            #self.ax.scatter(self.cont, d, label = group);
        #for a in range(len(x)):
        #    self.ax.scatter(x[a], y[a], label = group);
        self.ax.scatter(x, y, label = group);
        self.cont+=1;
    
    def plot(self):        
        plt.grid();
        plt.legend();
        plt.savefig("plot2D.png");
        plt.show();
        
'''
classe para plotagem 3d
'''
class dotsPlot3D(object):
    '''
    classdocs
    '''    
    
    def __init__(self, title, xTitle, yTitle, zTitle):
        fig = plt.figure();        
        self.ax = fig.add_subplot(111, projection = '3d');
        #ax = fig.gca(projection='3d');
        #ax = Axes3D(fig)        
        self.ax.set_xlabel(xTitle);
        self.ax.set_ylabel(yTitle);
        self.ax.set_zlabel(zTitle);    
      
    def addDot(self, x, y, z, group):
        self.ax.scatter(x, y, z, label=group)
    
    def plot(self):        
        plt.grid();        
        plt.legend();
        plt.show();
        plt.savefig("plot.png");
       

class histogram(object):
    
    def __init__(self,name, file, title, xTitle, yTitle, red, green, blue, x):   
        plt.plot(x, red, color = "red", label = "red");
        plt.plot(x, green, color = "green", label = "green");
        plt.plot(x, blue, color = "blue", label = "blue");
        plt.grid(True);
        plt.xlabel(xTitle);
        plt.ylabel(yTitle);
        plt.title(title+"-"+file);
        plt.legend();
        plt.savefig(name);
        plt.close();
        #plt.show();



        