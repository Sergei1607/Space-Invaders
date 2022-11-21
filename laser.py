# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 10:34:46 2022

@author: serge
"""

import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height = 500):
        super().__init__()
        
        self.image = pygame.Surface((4,20))
        self.image.fill("White")
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        
    def destroy(self):
        if self.rect.y <= -50:
            self.kill()
            
    def update(self):
        self.rect.y += self.speed
        self.destroy()
        
    def alien_lasers_update(self):
        
        print("test")
        
             
           
            