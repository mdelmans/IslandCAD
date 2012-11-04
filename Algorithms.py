'''
Created on Sep 12, 2012
Author: Mihails Delmans
Description:
Describes fractal construction algorithms.
'''
from numpy import *
from math import sqrt,pi,atan
KOCH = 0
POYA = 1
CHEZARO = 2
HUNTER = 3

LEFT = 0
RIGHT = 1


class Fractal:
    
    def __init__(self,initiator,generator,ftype):
        self. r = []
        self.initiator = array(initiator).T
        self.snowflake = array(initiator).T
        self.left = array(generator).T
        
        rigth = [[point[0],-point[1]] for point in generator]
        self.right = array(rigth).T
    
     
        self.counter = 0
        self.type = ftype
        self.firstside = LEFT
        
    def step(self):
        newflake = array([[],[]])
        
        for a,b in zip( self.snowflake[:,:-1].T, self.snowflake[:,1:].T ):
            self.r.append(sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2))
            
        for i in range(self.snowflake.shape[1]-1):
            x1 = self.snowflake[0,i]
            y1 = self.snowflake[1,i]
            x2 = self.snowflake[0,i+1]
            y2 = self.snowflake[1,i+1]
            cosp = (x2-x1) / sqrt( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) )
            sinp = (y2-y1) / sqrt( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) )
            if newflake.shape!= (2,0): newflake = delete(newflake,-1,1)
            if self.type == KOCH:
                inpiece = dot(array([[cosp,-sinp],[sinp,cosp]]),self.left*self.r[i]) + [[x1],[y1]]
            if self.type == POYA:
                if (i+self.firstside) % 2 == 0:
                    inpiece = dot(array([[cosp,-sinp],[sinp,cosp]]),self.left*self.r[i]) + [[x1],[y1]]    
                else:
                    inpiece = dot(array([[cosp,-sinp],[sinp,cosp]]),self.right*self.r[i]) + [[x1],[y1]]
            elif self.type == CHEZARO:
                
                if (self.firstside) % 2 == 0:
                    inpiece = dot(array([[cosp,-sinp],[sinp,cosp]]),self.left*self.r[i]) + [[x1],[y1]] 
                else:
                    inpiece = dot(array([[cosp,-sinp],[sinp,cosp]]),self.right*self.r[i]) + [[x1],[y1]] 
            elif self.type == HUNTER:
                if ((i+1) % 2 == 0) or (self.counter == 0):
                    inpiece = dot(array([[cosp,-sinp],[sinp,cosp]]),self.left*self.r[i]) + [[x1],[y1]]    
                else:
                    inpiece = dot(array([[cosp,-sinp],[sinp,cosp]]),self.right*self.r[i]) + [[x1],[y1]]
                    
                                                                                
                                    
            newflake = hstack((newflake,inpiece))
        if self.type == POYA or self.type == CHEZARO:
            self.firstside =-~(-self.firstside)
        self.snowflake = newflake
        self.r = []
        
        self.counter+= 1
    def getPoints(self,rect):
        return [(round(x*rect.width)+rect.left,-round(y*rect.width)+rect.top+rect.height//2) for x,y in zip(self.snowflake.T[:,0],self.snowflake.T[:,1])]

