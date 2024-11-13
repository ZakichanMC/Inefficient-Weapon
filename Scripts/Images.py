import pygame, os, sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir) 
pygame.init()

crateImg = pygame.image.load('Assets/Sprites/crate.png')
playerSheet = pygame.image.load('Assets/Sprites/PlayerIdleWalk.png')
level = pygame.image.load('Assets/Sprites/tutorial.png')
halfHeart = pygame.image.load('Assets/Sprites/halfheart.png')
fullHeart = pygame.image.load('Assets/Sprites/fullheart.png')

plateUp = pygame.image.load('Assets/Sprites/plateup.png')
plateDown = pygame.image.load('Assets/Sprites/platedown.png')

arrowSheet = pygame.image.load('Assets/Sprites/arrowSheet.png')