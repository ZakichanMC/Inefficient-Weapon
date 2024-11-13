import pygame
import random
from Scripts import SpriteManager as ss
from Scripts import CollideObjects as co
from Scripts import Images as img
pygame.init()

DISPLAY = pygame.display.set_mode((960, 540))
SCREEN = pygame.Surface((240, 135)) #blit things here, but use the dimensions of screen for pos

IFRAMEEVENT = pygame.USEREVENT + 1

pygame.display.set_caption("Inefficient Weapon")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

gameState = "tutorial"
isClicking = False
currentLevel = 0
resetPoints = [(4, 125)]

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            isClicking = True
        if event.type == pygame.MOUSEBUTTONUP:
            isClicking = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            co.crate.pushed(2, ss.player)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            ss.player.rect.x, ss.player.rect.y = resetPoints[currentLevel]
        
        if ss.player.iframes:
            pygame.time.set_timer(IFRAMEEVENT, 500)
        if event.type == IFRAMEEVENT:
            ss.player.iframes = False
            pygame.time.set_timer(IFRAMEEVENT, 0)

    SCREEN.fill(BLACK)
    ss.player.updateCam(SCREEN.get_width(), SCREEN.get_height())
    SCREEN.blit(img.level, (-ss.player.camX, -ss.player.camY))
    SCREEN.blit(ss.plate.image, (ss.plate.rect.x - ss.player.camX, ss.plate.rect.y - ss.player.camY)) #change to work with a list of multiple plates
    ss.plate.animate(ss.player.feetRect)



    for obj in co.staticObj:
        co.crate.collide(obj.rect)
        SCREEN.blit(obj.image, (obj.rect.x - ss.player.camX, obj.rect.y - ss.player.camY))
    for i in co.moveObj:
        SCREEN.blit(i.image, (i.rect.x - ss.player.camX, i.rect.y - ss.player.camY))
    for sprite in ss.spritesList: #draw second to last
        SCREEN.blit(sprite.image, (sprite.rect.x - ss.player.camX, sprite.rect.y - ss.player.camY))
    ss.player.drawHealth(SCREEN, img.halfHeart, img.fullHeart) #draw last

    if ss.player.health == 0: #move to ss later
        ss.player.rect.x, ss.player.rect.y = resetPoints[currentLevel]
        ss.player.health = 2

    keys = pygame.key.get_pressed()

    ss.player.takeDmg(3, co.spikes)
    ss.player.move(2, keys, isClicking)
    ss.player.animate()
    DISPLAY.blit(pygame.transform.scale(SCREEN, (960, 540)), (0, 0))

    pygame.display.update()
    clock.tick(30)