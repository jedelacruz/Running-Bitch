import pygame
import pygame.mixer
from random import randint
from sys import exit

def display_score(start_time, font, screen):
    scoreTime = int(pygame.time.get_ticks() - start_time) // 1000
    scoreTime_surface = font.render(f"Score: {scoreTime}", True, pygame.Color("Black"))
    scoreTime_rectangle = scoreTime_surface.get_rect(center=(400, 40))
    screen.blit(scoreTime_surface, scoreTime_rectangle)
    return scoreTime

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rectangle in obstacle_list:
            obstacle_rectangle.x -= 6

            if obstacle_rectangle.bottom == 300: screen.blit(snail_surface,obstacle_rectangle)
            else: screen.blit(bird_surface,obstacle_rectangle)

            #screen.blit(snail_surface,obstacle_rectangle)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else: return[]

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rectangle in obstacles:
            if player.colliderect(obstacle_rectangle):
                return False
    return True

# Initialize pygame and other variables
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Running Bitch")
clock = pygame.time.Clock()
font = pygame.font.Font("RUN/font/Pixeltype.ttf", 50)
game_active = True
start_time = 0
bg_Music = pygame.mixer.Sound("RUN/audio/music.wav")
bg_Music.set_volume(0.1)
bg_Music.play(loops= -1)
fail_Music = pygame.mixer.Sound("RUN/audio/fail.mp3")
fail_Music.set_volume(0.3)
jump_Music = pygame.mixer.Sound("RUN/audio/jump.mp3")


sky_surface = pygame.image.load('RUN/images/Sky.png').convert()
ground_surface = pygame.image.load('RUN/images/Ground.png').convert()

snail_surface = pygame.image.load("RUN/images/snail1.png").convert_alpha()

bird_surface = pygame.image.load("RUN/images/fly1.png").convert_alpha()

obstacle_rectangle_list = []

player_surface = pygame.image.load("RUN/images/player_walk_1.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom=(80, 300))

player_gravity = 0

player_stand = pygame.image.load("RUN/images/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand.get_rect(center=(400, 200))

press_Space = font.render("Press Space To Continue", False, (111, 196, 169))
press_Space_rectangle = press_Space.get_rect(center=(400,340))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1600)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -18
                    jump_Music.play()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rectangle_list.append(snail_surface.get_rect(bottomright=(randint(900,1100), 300)))
            else:
                obstacle_rectangle_list.append(bird_surface.get_rect(bottomright=(randint(900,1100), 200)))

    if game_active:
        fail_Music.stop()
        
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        scoreTime = display_score(start_time, font, screen)
 

        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom = 300
        screen.blit(player_surface, player_rectangle)

        obstacle_rectangle_list = obstacle_movement(obstacle_rectangle_list)
        
        game_active = collisions(player_rectangle,obstacle_rectangle_list)
        
    else:
        bg_Music.stop()
        fail_Music.play(loops=1)
        
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rectangle)
        obstacle_rectangle_list.clear()
        player_rectangle.midbottom =(80,300)
        player_gravity = 0
        
        finalScore_name = font.render(f"Your Score: {scoreTime}", False, (111, 196, 169))
        finalScore_name_rectangle = finalScore_name.get_rect(center=(400, 60))
        screen.blit(finalScore_name, finalScore_name_rectangle)

        screen.blit(press_Space, press_Space_rectangle)

    pygame.display.update()
    clock.tick(60)