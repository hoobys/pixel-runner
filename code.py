import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha() # gracz
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.K_RIGHT]:
            self.rect.x += 3
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha() # slimak
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))


    def animation_state(self):
        if type == 'fly': self.animation_index += 0.2
        else: self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= score / 10 + 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def colllision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True
   
def move_bg(speed, rectangle1, rectangle2, surface):
    rectangle1.x -= speed
    rectangle2.x -= speed
    if rectangle1.x <= surface.get_width() * -1:
        rectangle1.x = surface.get_width() - 25
    if rectangle2.x <= surface.get_width() * -1:
        rectangle2.x = surface.get_width() - 25
    screen.blit(surface, rectangle1)
    screen.blit(surface, rectangle2)

pygame.init() # uruchamia pygame
screen = pygame.display.set_mode((800,400)) # tworzenie ekranu gry
pygame.display.set_caption('Pixel Runner') # nazwa okna gry
clock = pygame.time.Clock() # obiekt clock
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) # tworzenie czcionki
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1).set_volume(0.1)

# Grupy
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


sky_surface = pygame.image.load('graphics/Sky.png').convert() # tworzymy dodatkowy surface z niebem
sky_rect = sky_surface.get_rect(midtop = (0,0))
sky_rect2 = sky_surface.get_rect(midtop = (800, 0))


ground_surface = pygame.image.load('graphics/ground.png').convert() # ziemia
ground_rect = ground_surface.get_rect(midtop = (400, 300))
ground_rect2 = ground_surface.get_rect(midtop = (1187, 300))

# Ekran startowy
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand.get_rect(center = (400,200))

title_surface = test_font.render('Pixel Runner', False, (111,196,169))
title_rectangle = title_surface.get_rect(center = (400, 70))

start_surface = test_font.render('Press R to run!', False, (111,196,169))
start_rectangle = start_surface.get_rect(center = (400, 330))

# Czas
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(600, 1400))

while True:
    for event in pygame.event.get(): # sprawdzanie inputow uzytkownika
        if event.type == pygame.QUIT: # klikniecie X
            pygame.quit() # wyjscie z gry
            exit()
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                ground_rect.midtop = (400, 300)
                ground_rect2.midtop = (1187, 300)




    if game_active:
        move_bg(5, ground_rect, ground_rect2, ground_surface)
        move_bg(1, sky_rect, sky_rect2, sky_surface)

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = colllision_sprite()

    
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rectangle)


        lastscore_surface = test_font.render(f'Your score: {score}', False, (111,196,169))
        lastscore_rectangle = lastscore_surface.get_rect(center = (400, 330))
        screen.blit(title_surface, title_rectangle)

        if score == 0: screen.blit(start_surface, start_rectangle)
        else: screen.blit(lastscore_surface, lastscore_rectangle)

    pygame.display.update() # aktualizuje display (screen)
    clock.tick(60) # pętla nie powinna działać szybciej niz 60 fps