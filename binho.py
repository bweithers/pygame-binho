import pygame
from time import sleep
from sys import exit
from math import sin, cos, atan, atan2

pygame.init()
clock = pygame.time.Clock()

# SETUP VARS
screen_width = 1400
screen_height = 800
font = pygame.font.SysFont(None, 50)

# PYGAME SETUP
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Binho')
pygame.display.set_icon(pygame.image.load('D:\Personal Projects\pygame-binho\\assets\icon.png'))

# LOAD IMAGES
field_img = pygame.image.load('D:\Personal Projects\pygame-binho\\assets\\field.png')
field_img = pygame.transform.scale(field_img, (screen_width, screen_height))
peg_bounce = pygame.mixer.Sound('D:\Personal Projects\pygame-binho\\assets\star_bounce.wav')

#GAME VARS
FRICTION = 0.99
PEG_FRICTION = 0.75
EDGE_FRICTION = 0.75

class Player:
    def __init__(self,name):
        self.name = name
        self.score = 0

players = [Player('p1'), Player('p2')]

class Peg(pygame.sprite.Sprite):
    def __init__(self,side,index):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('D:\Personal Projects\pygame-binho\\assets\\peg.png'),(10,100))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width * 3/4, screen_height* 1/2)

class Ball(pygame.sprite.Sprite):
    def __repr__(self):
        return f'ball:{self.x}'
    
    def __init__(self, radius):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('D:\Personal Projects\pygame-binho\\assets\\ball.png'),(radius,radius)).convert_alpha()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        # self.rect = pygame.draw.circle(screen, color = (255,255,255), center = (0,0), radius=radius, width=0)
        self.radius = radius
        self.color = (255,255,255)
        self.reset_ball()

    def update(self):
        if pygame.sprite.spritecollideany(self, peg_group):
            self.dx *= -PEG_FRICTION
            self.dy *= -PEG_FRICTION
            peg_bounce.play()

        self.rect.x += self.dx
        self.rect.y += self.dy
        
        self.dx *= FRICTION
        self.dy *= FRICTION
        
        # top and bottom
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.dy *= -EDGE_FRICTION
            self.dx *= EDGE_FRICTION
        if self.rect.top <= 0:
            self.rect.top = 0
            self.dy *= -EDGE_FRICTION
            self.dx *= EDGE_FRICTION

        #goalcheck
        if self.rect.left <= 0:
            if 310 <= self.rect.center[1] <= 465:
                players[1].score += 1
                self.reset_ball()
                state = 'goal'
            else:
                self.rect.left = 0
                self.dx *= -1
        if players[1].score >= 7:
            state = 'gameover'
            return
        if self.rect.right >= screen_width:
            if 310 <= self.rect.center[1] <= 465:
                players[0].score += 1
                self.reset_ball()
                state = 'goal'
            else:
                self.rect.right = screen_width
                self.dx *= -1
        if players[0].score >= 7:
            state = 'gameover'
            return
    def pause(self):
        self.pdx, self.pdy = self.dx, self.dy
        self.dx, self.dy = 0,0
        return
    def play(self):
        self.dx, self.dy = self.pdx, self.pdy
        self.pdx, self.pdy = 0,0
        return
    def reset_ball(self):
        self.rect.center = (screen_width/2,screen_height/2)
        self.dx, self.dy = 0,0
        self.pdx, self.pdy = self.dx,self.dy
        return 
    def apply_force(self,fx,fy):
        power = 25
        self.dx += power*(fx/(abs(fx)+abs(fy)))
        self.dy += power*(fy/(abs(fx)+abs(fy)))
        
        print(self.dx, self.dy, (self.dx**2 + self.dy**2)**0.5)
        print()
        ang = atan2(self.dy,self.dx)
        print(ang, sin(ang), cos(ang))
        print()
        print()
        return


ball = Ball(50)
ball_group = pygame.sprite.Group()
ball_group.add(ball)

peg = Peg(0,0)
peg_group = pygame.sprite.Group()
peg_group.add(peg)

state = 'play'

def handle_kick():
    # power += 1
    x_diff = ball.rect.center[0] - pygame.mouse.get_pos()[0]
    y_diff = ball.rect.center[1] - pygame.mouse.get_pos()[1]
    # print(pygame.mouse.get_pos())
    ball.apply_force(x_diff,y_diff)

def draw_shapes():
    global state
    screen.blit(field_img,(0,0))
    screen.blit(font.render(str(players[0].score),True, (0,0,255)), (20, 20))
    screen.blit(font.render(str(players[1].score),True, (255,0,0)), (screen_width-40, 20))
    
    if state == 'play':
        pass
    
    if state == 'pause':
        screen.blit(font.render(str("PAUSE!"),True, (255,0,255)), (screen_width/2 - 62, screen_height/2 - 15))
    
    if state == 'goal':
        screen.blit(font.render(str("GOAL!"),True, (255,0,255)), (screen_width/2 - 50, screen_height/2))
        pygame.display.flip()
        sleep(.2)
        state = 'play'
    
    if state == 'gameover':
        screen.blit(font.render(str("GAME OVER!"),True, (255,0,255)), (screen_width/2 - 100, screen_height/2-100))
        

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == 'play':
                    ball.pause()
                    state = 'pause'
                elif state == 'pause':
                    ball.play()
                    state = 'play'
            # Easy gameover state for testing
            # if event.key == pygame.K_w:
            #     state = 'gameover'
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == 'play':
                handle_kick()
            ## TODO: RESET AFTER GAME
        if event.type == pygame.KEYUP:
            pass
    
    draw_shapes()
    peg_group.draw(screen)
    ball_group.draw(screen)
    ball_group.update()
    pygame.display.flip()
    clock.tick(144)