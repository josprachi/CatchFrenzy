import pygame
from pygame.locals import *

import random

WIDTH = 1280
HEIGHT = 960
RockCount = [0]
isGameRunning = False
ANIM_IDLE=0
ANIM_WALK_LEFT=1
ANIM_WALK_RIGHT=2
ANIM_CATCH=3
ANIM_DEAD=4

    # Custom event type
PLAYER_DEAD_EVENT = pygame.USEREVENT + 1
class Player(pygame.sprite.Sprite):
    @classmethod
    def load_images(cls):
        cls.images = [
            pygame.image.load('walk1.png').convert_alpha(),
            pygame.image.load('walk2.png').convert_alpha(),
            pygame.image.load('walk3.png').convert_alpha(),
            pygame.image.load('walk4.png').convert_alpha(),
            pygame.image.load('walk5.png').convert_alpha(),
            pygame.image.load('walk6.png').convert_alpha()]

        cls.rWalkImages = [
        	pygame.image.load('rwalk1.png').convert_alpha(),
            pygame.image.load('rwalk2.png').convert_alpha(),
            pygame.image.load('rwalk3.png').convert_alpha(),
            pygame.image.load('rwalk4.png').convert_alpha(),
            pygame.image.load('rwalk5.png').convert_alpha(),
            pygame.image.load('rwalk6.png').convert_alpha()]

        cls.idleImages = [
        	pygame.image.load('ninja1.png').convert_alpha(),
            pygame.image.load('ninja2.png').convert_alpha(),
            pygame.image.load('ninja3.png').convert_alpha(),
            pygame.image.load('ninja5.png').convert_alpha()]

        cls.catchImages = [
        	pygame.image.load('catch1.png').convert_alpha(),
            pygame.image.load('catch2.png').convert_alpha(),
            pygame.image.load('catch3.png').convert_alpha()] 

        cls.deadImages = [
            pygame.image.load('dead1.png').convert_alpha(),
            pygame.image.load('dead2.png').convert_alpha(),
            pygame.image.load('dead3.png').convert_alpha()]                
 

    def  __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.animation_delay = 100
        self.last_update = pygame.time.get_ticks()
        self.is_idle = True
        self.animation=ANIM_IDLE

        self.velocity = 100
        self.image = self.idleImages[self.current_frame]
        self.rect = pygame.Rect(x, y, w, h)
        self.parentWidth=0
        self.catchCounter=2
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def move_left(self):
        if self.rect.x > self.velocity:
            self.image = self.images[self.current_frame]
            self.rect.x -= self.velocity
 
    def move_right(self):
        if self.rect.x < self.parentWidth - self.rect.width - self.velocity:
            self.image = self.rWalkImages[self.current_frame]
            self.rect.x += self.velocity        

    def update(self):
        if pygame.time.get_ticks() - self.last_update > self.animation_delay:
            self.current_frame += 1
            if self.animation==ANIM_IDLE:
                self.catchCounter=2
                self.current_frame %= len(self.idleImages)
                self.image = self.idleImages[self.current_frame]
            elif self.animation==ANIM_CATCH:
                self.current_frame %= len(self.catchImages)
                self.image = self.catchImages[self.current_frame]
                if self.current_frame==0:
                    self.animation=ANIM_IDLE
            elif self.animation==ANIM_DEAD:
                self.current_frame %= len(self.deadImages)
                self.image = self.deadImages[self.current_frame]                            
            else:
                if self.current_frame >= len(self.images) and self.current_frame >= len(self.rWalkImages):
                    self.current_frame = 0  
                if self.animation==ANIM_WALK_RIGHT:
                    #print("moveright2")
                    self.move_right()
                    self.image= self.rWalkImages[self.current_frame]
                else:
                    self.move_left()
                    self.image = self.images[self.current_frame]# - len(self.images_left)]
            self.last_update = pygame.time.get_ticks()        
            
class Bomb(pygame.sprite.Sprite):
    @classmethod
    def load_images(cls):
        cls.blastTextures = [
            pygame.image.load('blast1.png').convert_alpha(),
            pygame.image.load('blast2.png').convert_alpha(),
            pygame.image.load('blast3.png').convert_alpha(),
            pygame.image.load('blast4.png').convert_alpha(),
            pygame.image.load('blast5.png').convert_alpha(),
            pygame.image.load('blast6.png').convert_alpha(),
        ]
    def __init__(self,texture,x,y,w,h,parent_):        
        super(Bomb,self).__init__()
        self.image = texture
        self.rect = Rect(x,y,w,h)
        self.rect.x = random.randrange(100,WIDTH - self.rect.width)
        #self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 15)
        self.speedx = random.randrange(-3, 3)
        self.collected = False
        self.animation_delay=200
        self.isBlastPlaying=False
        self.blastFrame_index = 0
        self.animation_last_update = pygame.time.get_ticks()
        self.animFrame=self.blastTextures[0]
        self.parent=parent_

    def update(self):
        self.rect.y += self.speedy
        if (self.rect.top > HEIGHT + 10) or (self.collected):
            if self.isBlastPlaying:
                self.animateBlast()
                
            else:
                print("blast not playing")
                self.resetPosition()

    def resetPosition(self):
        self.rect.x = random.randrange(100,WIDTH - (self.rect.width*1.5))
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 15)
        self.collected = False
                
    def draw(self, surface):        
        if self.isBlastPlaying: 
            surface.blit(self.animFrame, self.rect)
        else:
            surface.blit(self.image, self.rect)
            
    def animateBlast(self):
        self.speedy=0                
        if pygame.time.get_ticks() - self.animation_last_update > self.animation_delay:
            self.blastFrame_index += 1
            self.animation_last_update = pygame.time.get_ticks()
            if self.blastFrame_index >= len(self.blastTextures):
                self.blastFrame_index=0
                self.isBlastPlaying = False
                self.parent.life-=10
                if self.parent.life<10:
                    self.parent.gameOver = True
                    pygame.event.post(pygame.event.Event(PLAYER_DEAD_EVENT))
                self.resetPosition()

            self.animFrame=self.blastTextures[self.blastFrame_index]
       

class Star(pygame.sprite.Sprite):
    @classmethod
    def load_images(cls):
        cls.BombTexture = pygame.image.load('rock.png').convert_alpha()
    def __init__(self,texture,x,y,w,h):
        super(Star,self).__init__()
        self.image = texture
        self.rect = Rect(x,y,w,h)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.collected = False
    def update(self):
        self.rect.y += self.speedy
        if (self.rect.top > HEIGHT + 10) or (self.collected):
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 15)
            self.collected = False
    def draw(self, surface):
        surface.blit(self.image, self.rect)
                
    
class Menu(pygame.sprite.Sprite):
    @classmethod
    def load_images(cls):
        cls.MenuTexture = pygame.image.load('hudboard.png').convert_alpha()
        
        cls.PlayTextures = [
            pygame.image.load('start.png').convert_alpha(),
            pygame.image.load('startPressed.png').convert_alpha(),
            
        ]
        
        cls.PauseTextures = [
            pygame.image.load('PauseBtn.png').convert_alpha(),
            pygame.image.load('PauseBtn_Red.png').convert_alpha(),
            pygame.image.load('PauseBtn_Grey.png').convert_alpha(),
        ]
        cls.RestartTextures = [
            pygame.image.load('RestartBtn.png').convert_alpha(),
            pygame.image.load('RestartBtn_Red.png').convert_alpha(),
            pygame.image.load('RestartBtn_Grey.png').convert_alpha(),
        ]

    def __init__(self,x = 0, y = 0, width = 1, height = 1):
        super(Menu,self).__init__()
        sound_enabled = True
        self.image=self.MenuTexture
        self.image=pygame.transform.scale(self.MenuTexture,(WIDTH/2,HEIGHT/2))        
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.width = width
        self.height = height
        self.rect = self.MenuTexture.get_rect()        
        self.rect.x= WIDTH/4
        self.rect.y= HEIGHT/4


        self.play_button_center = (100, 50)
        self.play_button_radius = self.PlayTextures[0].get_rect().size[0]
        self.play_button_state = "normal"
        self.playButtonRect=self.PlayTextures[0].get_rect()
        self.playButtonRect.x=(WIDTH-self.playButtonRect.width)//2
        self.playButtonRect.y=(HEIGHT-self.playButtonRect.height)//2
        #self.playClickRect=self.PlayTextures[0].get_rect()
        #self.playButtonRect.x=self.rect.x+self.rect.width/9
        #self.playButtonRect.y=self.rect.y+self.rect.height/6.5


             
       
    def handle_mouse_click(self, pos):
        if self.playButtonRect.collidepoint(pos):
            self.on_play_button_click()
    def on_play_button_click(self):
        print("Play button clicked")
    
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        if self.play_button_state == "normal":            
            surface.blit(self.PlayTextures[0], (self.playButtonRect.x,self.playButtonRect.y))
        elif self.play_button_state == "pressed":
            surface.blit(self.PlayTextures[1], (self.playButtonRect.x,self.playButtonRect.y))
            
        
class HUD(pygame.sprite.Sprite):
    @classmethod
    def load_images(cls):
        cls.BkgTexture = pygame.image.load('HudBar.png').convert_alpha()
        cls.BkgTexture=pygame.transform.scale(cls.BkgTexture,(WIDTH,HEIGHT/8))
        cls.ClockImg = pygame.image.load('Clock.png').convert_alpha()
        cls.ClockImg = pygame.transform.scale(cls.ClockImg,(50,50))
        cls.SoundTextures = [
            pygame.image.load('sound.png').convert_alpha(),
            pygame.image.load('soundPressed.png').convert_alpha(),
            
        ]

    def __init__(self,x = 0, y = 0, width = 1, height = 1):
        super(HUD,self).__init__()		
        self.image = self.BkgTexture
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.sound_button_center = (100, 100)
        self.sound_button_radius = 25
        self.sound_button_state = "normal"
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        self.image.blit(self.ClockImg,(self.image.get_width()*0.5,20))
        if self.sound_button_state == "normal":
            self.image.blit(self.SoundTextures[0], (0,0))
        elif self.sound_button_state == "pressed":
            self.image.blit(self.SoundTextures[1], (0,0))



class Scene:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Catch Frenzy: Ninja Edition')
        self.initState()
        Player.load_images()
        Bomb.load_images()
        HUD.load_images()
        Menu.load_images()
        self.loadAssets()

    def initState(self):
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)        
        self.surface = pygame.display.set_mode(self.rect.size)
        self.clock = pygame.time.Clock()
        self.life = 30#100
        self.gameOver = False
        self.gamePaused = True
        self.showHUDTime=0
        self.showHUDDelay=60
        self.showMainmenu=False
    # Function to handle custom events
    
    def loadAssets(self):
        self.background = pygame.image.load('bg1.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, self.rect.size)
        self.foreground = pygame.image.load('ground1.png')
        self.foreground = pygame.transform.scale(self.foreground, self.rect.size)
        self.heartImg = pygame.image.load('heart.png').convert_alpha()
        self.heartImg = pygame.transform.scale(self.heartImg,(50,50))
        self.player = Player(300, HEIGHT-400, 64, 64)
        self.player.parentWidth=self.rect.width
        self.bombSprite = Bomb(pygame.image.load('bomb.png').convert_alpha(),10, 100, 64, 64,self)
        self.starSprite = Star(pygame.image.load('rock.png').convert_alpha(),400, 100, 64, 64)

        self.HUD = HUD (300, 300, 64, 64)
        self.menu= Menu(300, 300, 64, 64)

        self.Scorefont = pygame.font.SysFont(None, 42)
        self.Scoretext = self.Scorefont.render("0", True,(255,0,0))
        #self.Lifefont = pygame.font.SysFont(None, 42)
        self.Lifetext = self.Scorefont.render("X "+str(self.life/10), True,(255,0,0))

    def set_Pausegame(self):
        self.pauseGame = not self.pauseGame

    def set_GameOver(self):
        self.gameOver= not self.gameOver

    def renderScene_(self):                    
        # drawing
            self.surface.blit(self.background, (0,0))
            self.player.draw(self.surface)
            if self.gameOver and self.showMainmenu:
                self.menu.draw(self.surface)
            else:                
                self.bombSprite.draw(self.surface)
                self.starSprite.draw(self.surface)
            self.HUD.draw(self.surface)        
            self.surface.blit(self.Scoretext,(20,20))
            self.surface.blit(self.heartImg,(WIDTH*0.8,20))
            self.Lifetext = self.Scorefont.render("X "+str(self.life/10), True,(255,0,0))
            self.surface.blit(self.foreground, (0,0))
            self.surface.blit(self.Lifetext,(WIDTH*0.8,20))
 
            # draw code here
 
            pygame.display.flip()
    def on_mouse_down(pos, button):
        self.handle_mouse_down(pos)
        

    def handle_mouse_down(self, pos):
        self.HUD.handle_mouse_click(pos)       

    def mainloop(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == PLAYER_DEAD_EVENT:
                    self.player.animation=ANIM_DEAD                                        
                    self.gameOver = True
                    self.showHUDTime=0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                       if self.menu.playButtonRect.collidepoint(event.pos):
                            print("Button clicked!")    
                elif self.gameOver == False and self.bombSprite.isBlastPlaying== False:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a or event.key == K_LEFT:                        
                            self.player.animation=ANIM_WALK_LEFT
                        elif event.key == pygame.K_d or event.key == K_RIGHT:                        
                            self.player.animation=ANIM_WALK_RIGHT
                    elif event.type == KEYUP:                    
                        self.player.animation=ANIM_IDLE                    
                        self.player.current_frame = 0
                        self.player.last_update = pygame.time.get_ticks()
                      


            if pygame.sprite.collide_mask(self.player, self.starSprite):
                self.starSprite.collected = True
                RockCount[0] += 1
                self.Scoretext = self.Scorefont.render(str(RockCount[0]), True,(255,0,0))
                self.player.animation=ANIM_CATCH

            if pygame.sprite.collide_mask(self.player,self.bombSprite):
                self.bombSprite.collected = True
                self.bombSprite.isBlastPlaying=True                                                         
               
 
            ticks = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            self.player.update()            
            self.bombSprite.update()            
            self.starSprite.update()
            if self.gameOver:
                self.showHUDTime +=1
                if self.showHUDTime>self.showHUDDelay:                    
                    self.showMainmenu=True
       
            # drawing
            self.renderScene_()
            self.clock.tick(60)


 
if __name__ == '__main__':
    scene = Scene()
    scene.mainloop()
    pygame.quit()
