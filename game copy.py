from math import trunc
import pygame
import sys
import random
#289 511
pygame.init()
screen = pygame.display.set_mode((1000,600))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 50)
#game variables
state_grav =[1 , 2]
gravity = 0.75
rocket_movement = 0
game_active = True
score  = 0
highscore = 0
can_score = True 
bg_surface = pygame.image.load('sprites/background.jpg').convert()
#(1000, 600)
bg_surface = pygame.transform.scale(bg_surface, (1000, 600)) 
base_surface =  pygame.image.load('sprites/baase.png').convert()
base_surface = pygame.transform.scale(base_surface, (5,650))
floor_y = -100

rocket_surface1 = pygame.image.load('sprites/finalrocket_3.png').convert_alpha()
rocket_surface1 = pygame.transform.scale(rocket_surface1, (150,150))
rocket_surface2 = pygame.image.load('sprites/finalrocket_2.png').convert_alpha()
rocket_surface2 = pygame.transform.scale(rocket_surface2, (150,150))
rocket_surface3 = pygame.image.load('sprites/finalrocket_1.png').convert_alpha()
rocket_surface3 = pygame.transform.scale(rocket_surface3, (150,150))
rocket_frames = [rocket_surface1,rocket_surface2,rocket_surface3]
rocket_index = 0
rocket_surface = rocket_frames[rocket_index]
rocket_rect = rocket_surface.get_rect(center = (500,520))
BirdFLAP = pygame.USEREVENT+1
pygame.time.set_timer(BirdFLAP,200)


start_surface = pygame.image.load('sprites/finalrocket_1.png').convert_alpha()
start_surface = pygame.transform.scale(start_surface, (600,600))
start_rect = start_surface.get_rect(center = (500,300))

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
    visible_pipes = [pipe for pipe in pipes if pipe.centery < 650]
    return visible_pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx +400 >= 900:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,True,False)
            screen.blit(flip_pipe,pipe)
def check_coll(pipes):
    for pipe in pipes:
        global can_score
        if rocket_rect.colliderect(pipe):
            can_score = True
            return False
    if rocket_rect.centerx<= -100 or rocket_rect.centerx >= 1000:
        can_score = True
        return False

    return True

def rotate_roc(roc):
    new_roc = pygame.transform.rotozoom(roc ,-rocket_movement * 0.5, 1)#1 is scaling factor
    return new_roc

def roc_anim():
    new_roc = rocket_frames[rocket_index]
    new_roc_rect = new_roc.get_rect(center = (rocket_rect.centerx,520))
    return new_roc, new_roc_rect  

def score_display(game_state):
    if game_state=="main game":
        score_surface = game_font.render(str(score),True,(255,255,255))  
        score_rect = score_surface.get_rect(center = (500,50))
        screen.blit(score_surface,score_rect)
    if game_state == "game over":
        score_surface = game_font.render(f'Score: {score}',True,(255,255,255))  
        score_rect = score_surface.get_rect(center = (500,50))
        screen.blit(score_surface,score_rect)

        Game_over_surface = game_font.render('START',True,(170,80,255))  
        Gameover_rect = Game_over_surface.get_rect(center = (480,400))
        screen.blit(Game_over_surface,Gameover_rect)

        highscore_surface = game_font.render(f'High Score:{highscore} ',True,(255,255,255))  
        highscore_rect = highscore_surface.get_rect(center = (500,580))
        screen.blit(highscore_surface,highscore_rect)

def score_update(score,highscore):
    if score>= highscore:
        highscore = score
    return highscore

def score_check(pipes):
    global score,can_score

    if pipes:
        for pipe in pipes:
            if 515 <pipe.centery< 525 and can_score:
                score += 1
                can_score = False
            if pipe.centery>600:
                can_score = True


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
                pipe_list.clear()
                rocket_rect.center = (500,520)
                rocket_movement = 0
                game_active = True
                score = 0
            
        if event.type == SPAWNPIPES:
            pipe_list.extend(create_pipe())#appends tuples or any thing given by the function
        if event.type == BirdFLAP:
            if rocket_index < 2:
                rocket_index += 1
            else:
                rocket_index = 0
            rocket_surface,rocket_rect = roc_anim()
    
    screen.blit(bg_surface,(0,0))

    if game_active:
    #rocket
        rocket_movement += gravity
        rotated_roc = rotate_roc(rocket_surface)
        rocket_rect.centerx += rocket_movement
        screen.blit(rotated_roc,rocket_rect)
        game_active = check_coll(pipe_list)

        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        #score
        score_display("main game")
        score_check(pipe_list)
    else:
        screen.blit(start_surface,start_rect)
        highscore = score_update(score, highscore)
        score_display("game over")
    #floor
    draw_floor()
    floor_y += 1
    if floor_y >= 512:
        floor_y = 0

    pygame.display.update()
    clock.tick(60) 

 '''def draw(self , win):
        self.img_count += 1
        if self.img_count < self.anim_time:
            self.img = self.IMGS[0]
        elif self.img_count < self.anim_time*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.anim_time*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.anim_time*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.anim_time*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0'''
