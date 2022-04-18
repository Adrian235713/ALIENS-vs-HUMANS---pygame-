import pygame
import os
pygame.font.init()

# -----------------------------------------------------------------
WIDTH, HEIGHT = 900, 500
WIN  = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
 
ALIEN_HIT = pygame.USEREVENT + 1
HUMAN_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)
 
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 5, HEIGHT)
FPS = 120
MOVEMENT = 5
BULLET_MOVEMENT = 9
pygame.display.set_caption("ALIENS vs HUMANS !!!")
# -----------------------------------------------------------------
WIDTH_SHIP, HEIGH_SHIP = 60, 50
ALIEN_SHIP_IMG = pygame.image.load(os.path.join('Assets','alien_ship.png'))
ALIEN_SHIP = pygame.transform.rotate(
    pygame.transform.scale(ALIEN_SHIP_IMG, (WIDTH_SHIP,HEIGH_SHIP)) , 270)
HUMAN_SHIP_IMG = pygame.image.load(os.path.join('Assets','human_ship.png'))
HUMAN_SHIP =pygame.transform.rotate(
    pygame.transform.scale(HUMAN_SHIP_IMG, (WIDTH_SHIP,HEIGH_SHIP)), 90)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets','background.jpg')),
    (WIDTH, HEIGHT))
# -----------------------------------------------------------------
def draw_window(human, alien, alien_bullets, human_bullets, alien_h, human_h):

    WIN.blit(BACKGROUND, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(ALIEN_SHIP, (alien.x,alien.y))
    WIN.blit(HUMAN_SHIP, (human.x,human.y))

    alien_health_text = HEALTH_FONT.render("HEALTH: " + str(alien_h),1,WHITE)
    human_health_text = HEALTH_FONT.render("HEALTH: " + str(human_h),1,WHITE)
    WIN.blit(alien_health_text, (600, 0))
    WIN.blit(human_health_text, (50, 0))
 
    for bullet in alien_bullets:
        pygame.draw.rect(WIN, RED, bullet)
 
    for bullet in human_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
 
    pygame.display.update()
# -----------------------------------------------------------------
def alien_movment(keys_pres,alien):
    if keys_pres[pygame.K_LEFT] and alien.x - MOVEMENT > 0:
        alien.x -= MOVEMENT
    elif keys_pres[pygame.K_RIGHT] and  alien.x + MOVEMENT + alien.width < BORDER.x:
        alien.x += MOVEMENT
    elif keys_pres[pygame.K_UP] and alien.y - MOVEMENT > 0:
        alien.y -= MOVEMENT
    elif keys_pres[pygame.K_DOWN] and  alien.y + MOVEMENT + alien.height < HEIGHT:
        alien.y += MOVEMENT
# -----------------------------------------------------------------  
def human_movment(keys_pres, human):
    if keys_pres[pygame.K_a] and human.x - MOVEMENT > BORDER.x + BORDER.width:
        human.x -= MOVEMENT
    elif keys_pres[pygame.K_d] and  human.x + MOVEMENT + human.width < WIDTH:
        human.x += MOVEMENT
    elif keys_pres[pygame.K_w] and human.y - MOVEMENT > 0:
        human.y -= MOVEMENT
    elif keys_pres[pygame.K_s] and  human.y + MOVEMENT + human.height < HEIGHT:
        human.y += MOVEMENT
# -----------------------------------------------------------------
def handle_bullets(alien_bullets, human_bullets, alien, human):
    for bullet in alien_bullets:
        bullet.x += BULLET_MOVEMENT
        if human.colliderect(bullet):
            pygame.event.post(pygame.event.Event(HUMAN_HIT))
            alien_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            alien_bullets.remove(bullet)
 
    for bullet in human_bullets:
        bullet.x -= BULLET_MOVEMENT
        if alien.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ALIEN_HIT))
            human_bullets.remove(bullet)

        elif bullet.x < 0:
            human_bullets.remove(bullet)
# -----------------------------------------------------------------
def winner_end(inf):
    text = WINNER_FONT.render(inf, 1, WHITE)
    WIN.blit(text, (WIDTH//4,HEIGHT//4))
    pygame.display.update()
    pygame.time.wait(2000)

# -----------------------------------------------------------------
def main():
    human = pygame.Rect(700, 300, WIDTH_SHIP, HEIGH_SHIP)
    alien = pygame.Rect(100, 300, WIDTH_SHIP, HEIGH_SHIP)
    clock = pygame.time.Clock()
    run = True

    alien_bullets = []
    human_bullets = []

    alien_h = 13
    human_h = 13

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
 
            if event.type == pygame.QUIT:
                run = False
                pygame.quit() 
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RALT:
                    bullet = pygame.Rect(alien.x + alien.width, alien.y + alien.height//2,10,5)
                    alien_bullets.append(bullet)

                if event.key == pygame.K_LALT:
                    bullet = pygame.Rect(human.x, human.y + human.height//2,10,5)
                    human_bullets.append(bullet)

            if event.type == ALIEN_HIT:
                alien_h -= 1
    
            if event.type == HUMAN_HIT:
                human_h -= 1
        
        winner = ""
        if alien_h <= 0:
            winner = "HUMANS WINN !!!"
        if human_h <= 0:
            winner = "ALIENS WINN !!!"
        if winner != "":
            winner_end(winner)
            break



        print(alien_bullets,human_bullets)
 
        keys_pres = pygame.key.get_pressed()
        human_movment(keys_pres, human)
        alien_movment(keys_pres,alien)
       
        handle_bullets(alien_bullets,human_bullets, alien, human)
 
        draw_window(human, alien, alien_bullets, human_bullets, alien_h, human_h)
 
    main() 

# -----------------------------------------------------------------
if __name__ == "__main__":
    main()
# -----------------------------------------------------------------
