import pygame 
from pygame.locals import * 

winWidth=600
winHeight=480
color_CYAN=(0,255,255)

pygame.init()

caption="Empty Game Window"
pygame.display.set_caption(caption)

Game_Window=pygame.display.set_mode((winWidth,winHeight))
Game_Window.fill(color_CYAN)

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()

    pygame.display.update()