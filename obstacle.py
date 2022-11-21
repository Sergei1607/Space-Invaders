# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 11:17:05 2022

@author: serge
"""

import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, size, color, x, y):
        super().__init__()
        
        self.image = pygame.Surface((size,size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x , y))
        
        
shape = [
'  xxxxxxx',
' xxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx']
   
    