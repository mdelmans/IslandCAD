'''
Created on Sep 24, 2012
Author: Mihails Delmans
Description:
Creates Fractal Islands based on specified algorithm. 
'''


from __future__ import division
import pygame._view
import pygame , sys
from pygame.locals import *
from Backstage import *
from Algorithms import Fractal
from math import fabs,sqrt,atan,pi,copysign


LINE_ON = False
NET_ON = True
MODE = INIT
xpos,ypos = 0,0
fpsClock = pygame.time.Clock()
eventF = dict()

############# INIT pygame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((display_W,display_H))
fonts = pygame.font.Font('freesansbold.ttf', 32)
pygame.display.set_caption("Fractals Editor")

############ Init Units
lLength = Label(fonts,'0.00',RED,BLACK,(100,50))
lAngle =  Label(fonts,'0.00',RED,BLACK,(200,50))

dField = DrawField((600,600),(100,100),100)

bInitiator = Button(BLUE,A_BLUE,fonts,'Initiator',BLACK,(200,100),(800,0))
bGenerator = Button(BLUE,A_BLUE,fonts,'Generator',BLACK,(200,100),(800,105))
bRender    = Button(BLUE,A_BLUE,fonts,'Render',BLACK,(200,100),(800,210))
bKoch = Button(GREEN,LGREEN,fonts,'Koch',BLACK,(80,50), (920,350))
bPoya = Button(GREEN,LGREEN,fonts,'Poya',BLACK,(80,50), (920,410))
bChezaro = Button(GREEN,LGREEN,fonts,'Chezaro',BLACK,(200,50), (800,470))
bHunter = Button(GREEN,LGREEN,fonts,'Hunter',BLACK,(200,50), (800,530))

render_options = [bKoch,bPoya,bChezaro,bHunter]

for rbutton in render_options:
    rbutton.visible = False

menu = [bInitiator,bGenerator,bRender]


initiator = Line(RED,4)
generator = Line(RED,4)
render = Line(BLUE,1,points = False)

bInitiator.activate()
initiator.visible = True
generator.visible = False
blines = dict({bInitiator:initiator, bGenerator:generator, bRender:render})

############ Init event functions
def mouseup(event):
    global LINE_ON
    global fractal
    if event.button == LEFT:
        if dField.isUnderMouse():
            for line in [initiator,generator]:
                if line.visible:
                    if not LINE_ON:
                        lLength.setText('0.00')
                        lAngle.setText('0.00')
                        if len(line.points) < 2:
                            LINE_ON = True
                        line.clear()
                    line.addPoint((xpos,ypos))
            
        inactive_mbuttons = []
        if [button.isClicked() for button in menu].count(True) == 1:
            for button in menu:
                if button.isClicked():
                    button.activate()
                    blines[button].visible = True
                    if (button == bInitiator) or (button == bGenerator):
                        dField.visible = True
                        for rbutton in render_options:
                            rbutton.visible = False
                    else:
                        dField.visible = False
                        for rbutton in render_options:
                            rbutton.visible = True
                            rbutton.deactivate()
                        fractal = None
                else:
                    inactive_mbuttons.append(button)
                     
                
            for sec_button in inactive_mbuttons:
                sec_button.deactivate()
                blines[sec_button].visible = False
       
        inactive_buttons = []
        if [button.isClicked() for button in render_options].count(True) == 1:
            for pos,button in enumerate(render_options):
                if button.isClicked():
                    button.activate()
                    fractal = Fractal(initiator.matrix(dField.rect),generator.matrix(dField.rect),pos) 
                else:   inactive_buttons.append(button)
                
            for sec_button in inactive_buttons:
                sec_button.deactivate()
            
            
        
eventF[MOUSEBUTTONUP] = mouseup


def pquit(event):
    pygame.quit()
    sys.exit()

eventF[QUIT] = pquit

def keydown(event):
    global LINE_ON
    if initiator.visible or generator.visible:
                if event.key == K_RETURN or event.key == K_ESCAPE:
                    LINE_ON =False
                
                elif event.key == K_LALT:
                    dField.NET_ON = False
######### Render

    if render.visible:
        if event.key == K_RETURN:
            if fractal != None: 
                fractal.step()
                render.points = fractal.getPoints(dField.rect)
######### Common            
                
    if event.key == K_EQUALS:
        mods = pygame.key.get_mods()
        if mods == 64 and dField.net_step < 100 :
            dField.net_step*=2
                        
    elif event.key == K_MINUS:
        mods = pygame.key.get_mods()
        if mods == 64 and dField.net_step > 25:
            dField.net_step//= 2
            
eventF[KEYDOWN] = keydown
def keyup(event):
    if event.key == K_LALT:
        dField.NET_ON = True
        
eventF[KEYUP] = keyup


############# Main Cycle
while True:
    
    if dField.isUnderMouse():
        xpos, ypos = dField.getMousePos()
        
############ Draw display, labels        
    DISPLAYSURF.fill(BLACK)
    dField.draw(DISPLAYSURF)
    lLength.draw(DISPLAYSURF)
    lAngle.draw(DISPLAYSURF)
    
############ Draw Line 

    for line in [initiator,generator,render]:
        if line.visible:   
            line.draw(DISPLAYSURF)
            
############ Draw Buttons

    bInitiator.draw(DISPLAYSURF)
    bGenerator.draw(DISPLAYSURF)
    bRender.draw(DISPLAYSURF)
    bKoch.draw(DISPLAYSURF)
    bPoya.draw(DISPLAYSURF)
    bChezaro.draw(DISPLAYSURF)
    bHunter.draw(DISPLAYSURF)
    
########### Handle events    

    for event in pygame.event.get():
        if event.type in eventF:
            eventF[event.type](event)

########### Update labels            

    if LINE_ON:
        for line in [initiator,generator,render]:
            if line.visible:
                lLength.setText(str(round(sqrt((line.points[-1][0]-xpos)**2 + (line.points[-1][1] - ypos)**2),2)))
                if line.points[-1][0] != xpos :
                    lAngle.setText(str(round(-atan((ypos-line.points[-1][1])/(xpos-line.points[-1][0]))*360/(2*pi),2)))
                else:
                    lAngle.setText(str(copysign(90.0,line.points[-1][1]-ypos)))
                pygame.draw.line(DISPLAYSURF,line.color,line.points[-1],(xpos,ypos) ,line.width)
    
    pygame.display.update()
    fpsClock.tick(FPS)
     
