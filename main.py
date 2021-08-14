from math import trunc
import pygame
import sys
import random
#289 511
pygame.init()
screen = pygame.display.set_mode((1000,600))
clock = pygame.time.Clock()

#game variables
state_grav =[1 , 2]
gravity = 0.75
rocket_movement = 0
game_active = True

bg_surface = pygame.image.load('sprites/background.jpg').convert()
#(1000, 600)
bg_surface = pygame.transform.scale(bg_surface, (1000, 600)) 
base_surface =  pygame.image.load('sprites/baase.png').convert_alpha()
base_surface = pygame.transform.scale(base_surface, (5,650))
floor_y = -100

rocket_surface = pygame.image.load('sprites/finalrocket_1.png').convert_alpha()
rocket_surface = pygame.transform.scale(rocket_surface, (150,150))
rocket_rect = rocket_surface.get_rect(center = (500,520))

#pipes keyaspect to control pipe and gravity
pipe_surface = pygame.image.load('sprites/pipe.png').convert_alpha()
pipe_surface = pygame.transform.scale(pipe_surface, (700,52))
pipe_list = []

SPAWNPIPES = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPES , 1200)
pipe_height = [500,600,700,800]


def draw_floor():
    screen.blit(base_surface,(0,floor_y))
    screen.blit(base_surface,(0,floor_y - 650))
    screen.blit(base_surface,(995,floor_y))
    screen.blit(base_surface,(995,floor_y - 650))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    right_pipe = pipe_surface.get_rect(midleft = (random_pipe_pos,-700))
    left_pipe = pipe_surface.get_rect(midright = (random_pipe_pos-300,-700))
    return right_pipe,left_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centery +=8
    return pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx +400 >= 900:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,True,False)
            screen.blit(flip_pipe,pipe)
def check_coll(pipes):
    for pipe in pipes:
        if rocket_rect.colliderect(pipe):
            return False
    if rocket_rect.centerx<= -100 or rocket_rect.centerx >= 1000:
        return False
    return True


    


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                rocket_movement = 0
                rocket_movement -= 17
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
            
        if event.type == SPAWNPIPES:
            pipe_list.extend(create_pipe())#appends tuples or any thing given by the function
    
    screen.blit(bg_surface,(0,0))

    if game_active:
    #rocket
        rocket_movement += gravity
        rocket_rect.centerx += rocket_movement
        screen.blit(rocket_surface,rocket_rect)
        game_active = check_coll(pipe_list)

        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    #floor
    draw_floor()
    floor_y += 1
    if floor_y >= 512:
        floor_y = 0

    pygame.display.update()
    clock.tick(60) 

