'''
Created on 14/10/2017

@author: nathan
'''

class imageData(object):
    '''
    classdocs
    '''
    
    def __init__(self, name, size):
        self.name = name;        
        self.size = size;
        
    def setDomainColor(self, domainColor, numApp):
        self.domainColor = domainColor;
        self.numApp = numApp;    
    
    def __str__(self, *args, **kwargs):
        return self.name+";"+str(self.domainColor)+";"+str(self.numApp)+";"+str(self.size);