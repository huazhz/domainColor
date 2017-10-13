'''
Created on 12/10/2017

@author: nathan
'''
from matplotlib import pyplot as plt

class dotsPlot(object):
    '''
    classdocs
    '''    
    x = [];
    y = [];
    def __init__(self, title, xTitle, yTitle):
        '''
        Constructor
        '''
        #plt.plot([1,2,3,4], [1,4,9,16], 'ro')
        fig, ax = plt.subplots();
        self.ax = ax;       
        plt.title(title);
        plt.xlabel(xTitle);
        plt.ylabel(yTitle);
        self.cont = 1;
    
    def addDot(self, x, y, group):
        self.ax.scatter(x, y, label = group);
        self.x.append(x);
        self.y.append(y);
    
    def addDot2(self, x, y, group):
        #for d in data:            
            #self.ax.scatter(self.cont, d, label = group);
        #for a in range(len(x)):
        #    self.ax.scatter(x[a], y[a], label = group);
        self.ax.scatter(x, y, label = group);
        self.cont+=1;        

        
    def plot(self):
        #plt.scatter(self.x, self.y);        
        plt.grid();
        plt.legend();
        plt.show();
        
        