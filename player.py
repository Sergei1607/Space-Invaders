# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 09:37:19 2022

@author: serge
"""

import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        
        self.image = pygame.image.load("graphics/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600 
        self.lasers = pygame.sprite.Group()
        
    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -8))
       
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True
        
    def get_imput(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT] and self.rect.x < 540:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            
    def update(self):
        self.get_imput()
        self.recharge()
        self.lasers.update()
        
            