import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT=900,500
WIN= pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fugarii")
WHITE= (255,255,255)
FPS=60
RED=(255,0,0)
YELLOW=(255,255,0)
BLACK=(0,0,0)
HEALTH_FONT=pygame.font.SysFont("comicsans",40)
WINNER_FONT=pygame.font.SysFont("comicsans",100)

bullet_hit_sound=pygame.mixer.Sound(os.path.join("Assets","Grenade+1.mp3"))
bullet_fire_sound=pygame.mixer.Sound(os.path.join("Assets","Gun+Silencer.mp3"))
bullet_fire_sound.set_volume(0.01)
bullet_hit_sound.set_volume(0.01)
VEL=4
YELLOWHIT=pygame.USEREVENT +1
REDHIT=pygame.USEREVENT+2
MAXBULLETS=3
BULLETS_VEL=7
BORDER= pygame.Rect(WIDTH//2 - 5,0,10,HEIGHT)
NAVAWIDTH, NAVAHEIGHT = 50, 45
NAVAY= pygame.image.load(
    os.path.join('Assets','spaceship_yellow.png'))
NAVAR= pygame.image.load(
    os.path.join('Assets','spaceship_red.png'))
SPACE=pygame.transform.scale(
    pygame.image.load(os.path.join("Assets","space.png")),(WIDTH,HEIGHT))
NAVAY=pygame.transform.rotate(
    pygame.transform.scale(NAVAY,(NAVAWIDTH,NAVAHEIGHT)),90)
NAVAR=pygame.transform.rotate(
    pygame.transform.scale(NAVAR,(NAVAWIDTH,NAVAHEIGHT)),270)

def draw_window(red, yellow,red_bullets,yellow_bullets,REDHEALTH,YELLOWHEALTH):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    redhealthtext=HEALTH_FONT.render("Health:"+ str(REDHEALTH),1,WHITE)
    yellowhealthtext=HEALTH_FONT.render("Health:"+ str(YELLOWHEALTH),1,WHITE)
    WIN.blit(yellowhealthtext,(WIDTH-redhealthtext.get_width()-20,10))
    WIN.blit(redhealthtext,(10,10))
    WIN.blit(NAVAY,(yellow.x, yellow.y))
    WIN.blit(NAVAR,(red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    pygame.display.update()

def drawwinner(text):
    draw_text=WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, (WIDTH/2-draw_text.get_width()/2,HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)



def yellow_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL>0:
        yellow.x-=VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < WIDTH/2-yellow.width:
        yellow.x+=VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL>0:
        yellow.y-=VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL <HEIGHT-yellow.height:
        yellow.y+=VEL
def red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x -VEL> WIDTH/2+5:
        red.x-=VEL
    if keys_pressed[pygame.K_RIGHT] and red.x +VEL < WIDTH- red.width:
        red.x+=VEL
    if keys_pressed[pygame.K_UP] and red.y -VEL >0:
        red.y-=VEL
    if keys_pressed[pygame.K_DOWN] and red.y +VEL < HEIGHT-red.height:
        red.y+=VEL

def coliziuni(yellow_bullets,yellow,red,red_bullets):
    for bullet in yellow_bullets:
        bullet.x+= BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(REDHIT))
            yellow_bullets.remove(bullet)
        elif bullet.x>WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x-= BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOWHIT))
            red_bullets.remove(bullet)
        elif bullet.x<0:
            red_bullets.remove(bullet)

def main():
    red = pygame.Rect(700, 300, NAVAWIDTH, NAVAHEIGHT)
    yellow = pygame.Rect(100, 300, NAVAWIDTH, NAVAHEIGHT)
    clock = pygame.time.Clock()
    run=True
    REDHEALTH=10
    YELLOWHEALTH=10
    red_bullets =[]
    yellow_bullets =[]
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
            if event.type==pygame.KEYDOWN and len(yellow_bullets)<MAXBULLETS:
                if event.key==pygame.K_LCTRL:
                    bullet=pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2-2,10,5)
                    yellow_bullets.append(bullet)
                    bullet_fire_sound.play()
                if event.key==pygame.K_RCTRL and len(red_bullets)<MAXBULLETS:
                    bullet=pygame.Rect(red.x,red.y+red.height//2-2,10,5)
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()
            if event.type==REDHIT:
                YELLOWHEALTH-=1
                bullet_hit_sound.play()

            if event.type==YELLOWHIT:
                REDHEALTH-=1
                bullet_hit_sound.play()
        winnertext=""
        if REDHEALTH<=0:
            winnertext="RED Win"
        if YELLOWHEALTH<=0:
            winnertext="YELLOW Win"
        if winnertext!="":
            drawwinner(winnertext)
            break

        keys_pressed = pygame.key.get_pressed()
        draw_window(red,yellow,red_bullets,yellow_bullets,REDHEALTH,YELLOWHEALTH)
        coliziuni(yellow_bullets,yellow,red,red_bullets)
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed,red)

    main()

if __name__=="__main__":
    main()