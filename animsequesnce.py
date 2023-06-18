import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images_animation1 = []  # List for first animation frames
        self.images_animation2 = []
        #self.images = []  # List for second animation frames
        self.current_frame = 0
        self.animation_delay = 100
        self.last_update = pygame.time.get_ticks()
        self.animation1_count = 0
        self.switch_animation_count = 5
        self.animation=0

        # Load first animation frames
        self.images_animation1.append(pygame.image.load("catch1.png").convert())
        self.images_animation1.append(pygame.image.load("catch2.png").convert())
        self.images_animation1.append(pygame.image.load("catch3.png").convert())

        # Load second animation frames
        self.images_animation2.append(pygame.image.load("ninja1.png").convert())
        self.images_animation2.append(pygame.image.load("ninja2.png").convert())
        self.images_animation2.append(pygame.image.load("ninja3.png").convert())
        self.images_animation2.append(pygame.image.load("ninja4.png").convert())
        self.images_animation2.append(pygame.image.load("ninja5.png").convert())

        self.image = self.images_animation1[self.current_frame]
        self.rect = self.image.get_rect()

    def update(self):
        if pygame.time.get_ticks() - self.last_update > self.animation_delay:
            self.current_frame += 1
            if self.current_frame >= len(self.images_animation1):
                self.current_frame = 0
                self.animation1_count += 1
                if self.animation1_count == self.switch_animation_count:
                    self.images = self.images_animation2
            self.image = self.images[self.current_frame]
            self.last_update = pygame.time.get_ticks()

sprite = SpriteObject()

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    sprite.update()

    screen.fill((255, 255, 255))
    screen.blit(sprite.image, sprite.rect)
    pygame.display.flip()

pygame.quit()
