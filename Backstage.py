'''
Created on Sep 22, 2012
Author: Mihails Delmans
Description:
Collection of helper functions.
'''
from __future__ import division
import pygame
from numpy import array

############## Colors
#        R   G   B      
GREEN = (10, 200, 20)
LGREEN = (20, 250, 40)
DGREY = ( 50, 50, 50)
GREY =  (128,128,128)
RED =   (255, 10, 10)
BLACK = (  0,  0,  0)
BLUE =  ( 20, 20,128)
A_BLUE =( 50, 50,255)

############# Vars
LEFT = 1
FPS = 30
display_H = 800
display_W = 1000
net_step = 100
########### Mode

INIT = 0
GENE = 1
REND = 2

class DrawField:
    def __init__(self, size, pos, net_step, color = BLACK, colorshift = False):
        self.color = color
        self.SURF = pygame.Surface((size[0]+1,size[1]+1))
        self.rect = pygame.Rect(pos[0],pos[1],size[0]+1,size[1]+1)
        self.NET_ON = True
        self.net_step = net_step
        self.visible = True
        self.colorshift = colorshift

    def draw(self, CANVAS):
        if self.visible:
            self.SURF.fill(self.color)
        
            x = 0
            for x in range (0,self.rect.width,self.net_step):
                pygame.draw.line(self.SURF,GREY,(x,0),(x,self.rect.height),1)
                
    
            y = 0
            for y in range (0,self.rect.height,self.net_step):
                pygame.draw.line(self.SURF,GREY,(0,y),(self.rect.width,y),1)
                y+=net_step
                
            pygame.draw.line(self.SURF,DGREY,(self.rect.width/2+1,1),(self.rect.width/2+1,self.rect.height+1),4)
            pygame.draw.line(self.SURF,DGREY,(1,self.rect.height/2+1),(self.rect.width+1,self.rect.height/2+1),4)
            CANVAS.blit(self.SURF,self.rect)
    
    def isUnderMouse(self):
        if self.visible:
            return self.rect.collidepoint(pygame.mouse.get_pos())
        else: return False
    
    def getMousePos(self):
            pos = (pygame.mouse.get_pos()[0]-self.rect.left,pygame.mouse.get_pos()[1]-self.rect.top)
            posx, posy = 0,0
            if self.NET_ON == True:
                if pos[0] - (pos[0] // self.net_step) * self.net_step <= (self.net_step // 10):
                    posx = (pos[0] // self.net_step) * self.net_step
                    
                elif (pos[0] // self.net_step + 1) * self.net_step - pos[0] <= (self.net_step // 10):
                    posx = (pos[0] // self.net_step + 1) * self.net_step
                    
                else:
                    posx = pos[0]
                    
                if pos[1] - (pos[1] // self.net_step) * self.net_step <= (self.net_step // 10):
                    posy = (pos[1] // self.net_step) * self.net_step
                elif (pos[1] // self.net_step + 1) * self.net_step - pos[1] <= (self.net_step // 10):
                    posy = (pos[1] // self.net_step + 1) * self.net_step
                else:
                    posy = pos[1]
                return posx+self.rect.left, posy+self.rect.top
            else:
                return pygame.mouse.get_pos()

        
class Button:
    def __init__(self,color,active_color,font,text,textcolor,size,pos):
        self.active_color = active_color
        self.color = color
        self.textcolor = textcolor
        self.font = font
        self.text = text
        
        self.visible = True
        
        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
        
        TEXTSURF = font.render(text,True,textcolor,color)
        self.textRect = TEXTSURF.get_rect()
        self.textRect.center = (size[0]//2,size[1]//2)
        
        self.SURF = pygame.Surface(size)
        self.SURF.fill(color)
        self.SURF.blit(TEXTSURF,self.textRect)
        
    def isClicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def activate(self):
        TEXTSURF = self.font.render(self.text,True,self.textcolor,self.active_color)
        self.SURF.fill(self.active_color)
        self.SURF.blit(TEXTSURF,self.textRect)
        
    def deactivate(self):
        TEXTSURF = self.font.render(self.text,True,self.textcolor,self.color)
        self.SURF.fill(self.color)
        self.SURF.blit(TEXTSURF,self.textRect)
        
    def draw(self, CANVAS):
        if self.visible:
            CANVAS.blit(self.SURF,self.rect)

class Label:
    def __init__(self,font,text,textcolor,bgcolor,pos):
        self.textcolor = textcolor
        self.bgcolor = bgcolor
        self.font = font
        
        self.SURF = font.render(text,True,textcolor,bgcolor)
        
        self.rect = self.SURF.get_rect()
        self.rect.top = pos[1]
        self.rect.left = pos[0]
        
    def draw(self, CANVAS):
        CANVAS.blit(self.SURF,self.rect)
    
    def setText(self,text):
        self.SURF = self.font.render(text,True,self.textcolor,self.bgcolor)
        self.rect.size = self.font.size(text)
        
        
class Line:
    def __init__(self,color,width,points = True):
        self.visible = False
        self.points = []
        self.color = color
        self.width = width
        self.points_on = points
    def draw (self,CANVAS):
        if len(self.points) > 1: 
            pygame.draw.lines(CANVAS,self.color,False,self.points,self.width)
            if self.points_on:
                for point in self.points:
                    pygame.draw.circle(CANVAS,self.color,(int(point[0]),int(point[1])),int(self.width*1.5),0)
    def addPoint (self,point):
        self.points.append(point)
    
    def clear(self):
        self.points = []
        
    def matrix(self,fRect):
        return [[round ( (x - fRect.left)/fRect.width , 3),round ( (fRect.height/2-(y-fRect.top))/fRect.width , 3)] for (x,y) in self.points ]
                
        
        
        