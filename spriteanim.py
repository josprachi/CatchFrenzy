IDLE=0
WALK_LEFT=1
WALK_RIGHT=2
CATCH=3
DEAD=4

import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images_left = []  # List for left walking animation frames
        self.images_right = []  # List for right walking animation frames
        self.images_idle = []  # List for idle animation frames
        self.current_frame = 0
        self.animation_delay = 100
        self.last_update = pygame.time.get_ticks()
        self.is_idle = True
        self.animation=IDLE
        self.velocity=4

        # Load left walking animation frames
        self.images_left.append(pygame.image.load("walk1.png"))
        self.images_left.append(pygame.image.load("walk2.png"))
        self.images_left.append(pygame.image.load("walk3.png"))
        self.images_left.append(pygame.image.load("walk4.png"))
        self.images_left.append(pygame.image.load("walk5.png"))
        self.images_left.append(pygame.image.load("walk6.png"))

        # Load right walking animation frames
        self.images_right.append(pygame.image.load("rwalk1.png"))
        self.images_right.append(pygame.image.load("rwalk2.png"))
        self.images_right.append(pygame.image.load("rwalk3.png"))
        self.images_right.append(pygame.image.load("rwalk4.png"))
        self.images_right.append(pygame.image.load("rwalk5.png"))
        self.images_right.append(pygame.image.load("rwalk6.png"))

        # Load idle animation frames
        self.images_idle.append(pygame.image.load("ninja1.png"))
        self.images_idle.append(pygame.image.load("ninja2.png"))
        self.images_idle.append(pygame.image.load("ninja3.png"))
        self.images_idle.append(pygame.image.load("ninja4.png"))
        self.images_idle.append(pygame.image.load("ninja5.png"))

        self.image = self.images_idle[self.current_frame]
        self.rect = self.image.get_rect()
        

    def update(self):
        if pygame.time.get_ticks() - self.last_update > self.animation_delay:
            self.current_frame += 1
            if self.animation==IDLE:#self.is_idle:
                self.current_frame %= len(self.images_idle)
                self.image = self.images_idle[self.current_frame]
            else:
                if self.current_frame >= len(self.images_left) and self.current_frame >= len(self.images_right):
                    self.current_frame = 0
                #if self.current_frame < len(self.images_left):
                if self.animation==WALK_RIGHT:
                    self.image = self.images_right[self.current_frame]
                else:
                    self.image = self.images_left[self.current_frame]# - len(self.images_left)]
            self.last_update = pygame.time.get_ticks()

sprite = SpriteObject()

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                sprite.animation=WALK_LEFT
                sprite.is_idle = False
            elif event.key == K_RIGHT:
                sprite.animation=WALK_RIGHT
                sprite.is_idle = False
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                sprite.animation=IDLE
                sprite.is_idle = True
                sprite.current_frame = 0
                sprite.last_update = pygame.time.get_ticks()

    screen.fill((255, 255, 255))
    sprite.update()

    screen.fill((255, 255, 255))
    screen.blit(sprite.image, sprite.rect)
    pygame.display.flip()

pygame.quit()
