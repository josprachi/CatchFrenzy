import pygame 
from pygame.locals import * 

winWidth=600
winHeight=480
color_CYAN=(0,255,255)
color_BLACK=(0,0,0)
pygame.init()

caption="Image Test"
pygame.display.set_caption(caption)

ship= pygame.image.load("ship.png")
pygame.display.set_icon(ship)

Game_Window=pygame.display.set_mode((winWidth,winHeight))
Game_Window.fill(color_CYAN)

bush=pygame.transform.scale((pygame.image.load("bush.png")),(50,50))
alphaBush=(pygame.image.load("bush.png")).convert()

bushes=[]
i=0
while i<10:
    bushes.append(bush.copy())
    i+=1

background= pygame.image.load("gameBkg.png")
background=pygame.transform.scale(background,(winWidth,winHeight))

y=winHeight*0.7
alphaBush.set_alpha(30)

while True:
    if y>0:
        y-=1
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()
     
    i=0
    Game_Window.blit(background, (0, 0))    
    Game_Window.blit(alphaBush,(winWidth*0.1,100))
    while i<len(bushes):        
        if i%2==0:
            Game_Window.blit(bushes[i],(winWidth*0.03,50*i))
        else:
            Game_Window.blit(bushes[i],(winWidth*0.83,50*i))  
        i+=1
        
    Game_Window.blit(ship,(winWidth*0.45,y))
    pygame.display.flip()
