# -*- coding: utf-8 -*-
import pygame
import sys
from player import Player
import obstacle 
from alien import Alien , Extra
from random import choice, randint
from laser import Laser

# =============================================================================
# Classes
# =============================================================================

class Game:
    def __init__(self):
        
        # player setup
        player_sprite = Player((screen_width/2, screen_hight-10), 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        
        # health and score setup
        
        self.lives = 3
        self.lives_surf = pygame.image.load("graphics/player.png").convert_alpha()
        self.live_x_start_pos = screen_width - (self.lives_surf.get_size()[0] * 2 + 20)
        
        self.score = 0
        self.font = pygame.font.Font("font/Pixeled.ttf", 20)
        
        
        # obstacle setup
        
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 15, y_start = 480)
        
        # alien setup
        
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()
        
        # extre alien
        
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800)
        
        # audio
        
        music = pygame.mixer.Sound("audio/music.wav")
        music.set_volume(0.2)
        music.play(loops = -1 )
        
        self.explosion = pygame.mixer.Sound("audio/explosion.wav")
        self.explosion.set_volume(0.4)
        
        self.laser_sound = pygame.mixer.Sound("audio/laser.wav")
        self.laser_sound.set_volume(0.2)
        
        
        
    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)
                    
    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)
        
    def alien_setup(self, rows, cols, x_distance= 60, y_distance= 48, x_offset = 70, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                 x = col_index * x_distance + x_offset
                 y = row_index * y_distance + y_offset
                 if row_index == 0:
                     alien_sprite = Alien("yellow", x, y)
                 elif row_index == 1 or row_index == 2: 
                     alien_sprite = Alien("green", x, y)
                 else:
                     alien_sprite = Alien("red", x, y)
                 self.aliens.add(alien_sprite)
                 
    def alien_position_checkout(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.x == 519:
                self.alien_direction = -1
                self.alien_move_down(0)
            elif alien.rect.x == 100:
                self.alien_direction = 1
                self.alien_move_down(0)
                
    def alien_move_down(self, distance):
        if self.aliens:
            all_aliens = self.aliens.sprites()
            for alien in all_aliens:
                alien.rect.y += distance
                
    def alien_shoot(self):
        if self.aliens:
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_hight)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()
            
    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time == 0:
            self.extra.add(Extra(choice(["left", "right"]),screen_width))
            self.extra_spawn_time = randint(400, 800)
        
    def collision_checks(self):
        
        #player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                
                # obstacle collision
                if pygame.sprite.spritecollide(laser,self.blocks, True):
                    laser.kill()
                    
                # aliens collision    
                
                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    self.explosion.play()
                    laser.kill()
               
                    
                # aliens collision    
                if pygame.sprite.spritecollide(laser,self.extra, True):
                    laser.kill()     
                    self.score += 500
     
        # alien lasers
        if self.alien_lasers:
            for alien_laser in self.alien_lasers:
                if pygame.sprite.spritecollide(alien_laser,self.blocks, True):
                    alien_laser.kill()
                    
       # alien lasers with player
        if self.alien_lasers:
              for alien_laser in self.alien_lasers:
                 if pygame.sprite.spritecollide(alien_laser,self.player, False):
                     self.explosion.play()
                     alien_laser.kill()
                     self.lives -=1
                     if self.lives <= 0:
                          pygame.quit()
                          sys.exit()
                         
                     
        # aliens with blocks
        
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks, True)
                
                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()
                    
    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.lives_surf.get_size()[0] + 10))
            screen.blit(self.lives_surf, (x,8))
            
    def display_score(self):
        text_surface = self.font.render(f'Score: {self.score}',False,("white"))
        text_rect = text_surface.get_rect(center = (110, 20))
        screen.blit(text_surface, text_rect)
        
    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render("You Won", False, ("white"))
            victory_rect = victory_surf.get_rect(center = (300, 300))
            screen.blit(victory_surf, victory_rect)
       
        
    def run(self):
        
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_position_checkout()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.alien_lasers.update()
        self.extra_alien_timer()
        self.extra.draw(screen)
        self.extra.update()
        self.display_lives()
        self.collision_checks()
        self.display_score()
        self.victory_message()
        
        
class CRT:
    def __init__(self):
        self.tv = pygame.image.load("graphics/tv.png").convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_hight, screen_hight))
        
        
    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_hight/line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, "black", (0,y_pos), (screen_width, y_pos), 1)
            
            
    def draw(self):
        self.tv.set_alpha(randint(1,90))
        self.create_crt_lines()
        screen.blit(self.tv, (0,0))
    
# =============================================================================
# Pygame Technical stuff
# =============================================================================
if __name__ == '__main__':
    
    pygame.init()
    
    screen_width = 600
    screen_hight = 600

    screen = pygame.display.set_mode((screen_width, screen_hight))
    
    # clock for the frame rate
    
    clock = pygame.time.Clock()
    
    # creating the instance of the game class
    
    game = Game()
    
    crt = CRT()
    
    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)
    
    
# =============================================================================
# ################################## Run Game ##############################
# =============================================================================
    
# =============================================================================
# While true and events
# =============================================================================
    
    while True:
        # to be able to quit de game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if event.type == ALIENLASER:
                game.alien_shoot()
            
    
# =============================================================================
# Game
# =============================================================================
    
        screen.fill((30, 30, 30))
        crt.draw()
        game.run()
    
# =============================================================================
# Final Stuff
# =============================================================================
    
        pygame.display.update()
        clock.tick(60)