import pygame, math, os, sys
from Scripts import Images as img
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir) 
pygame.init()

GRAY = (50, 50, 50)

class MoveableObjects(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        
    def pushed(self, speed, player):
        relX, relY = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        distance = math.sqrt(relX**2 + relY**2)
        if distance < 25:
            self.angle = math.atan2(relY, relX)
            self.rect.x -= int(speed * 5 * math.cos(self.angle))
            self.rect.y -= int(speed * 5 * math.sin(self.angle))
    
    def collide(self, obj):
       if self.rect.colliderect(obj):
        overlapX = min(self.rect.right - obj.left, obj.right - self.rect.left)
        overlapY = min(self.rect.bottom - obj.top, obj.bottom - self.rect.top)
        
        if abs(overlapX) < abs(overlapY): #if you're overlapping more horiz than vert
            if self.rect.centerx < obj.centerx:
                self.rect.right = obj.left
            else:
                self.rect.left = obj.right
        else:
            if self.rect.centery < obj.centery:
                self.rect.bottom = obj.top 
            else:
                self.rect.top = obj.bottom

class StaticObjects(pygame.sprite.Sprite):
    def __init__(self, image, color, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.image = image
        self.image.fill((50, 50, 50))
        self.image.set_colorkey(GRAY)
        pygame.draw.rect(self.image, color, [0, 0, self.image.get_width(), self.image.get_height()])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

crate = MoveableObjects(img.crateImg, 43, 34)
wall1 = StaticObjects(pygame.Surface((1, 99)), GRAY, 20, 29)
wall2 = StaticObjects(pygame.Surface((159, 1)), GRAY, 21, 31)
wall3 = StaticObjects(pygame.Surface((1, 99)), GRAY, 179, 29)
wall4 = StaticObjects(pygame.Surface((20, 1)), GRAY, 180, 127)
wall5 = StaticObjects(pygame.Surface((32, 9)), GRAY, 168, 143)
wall6 = StaticObjects(pygame.Surface((136, 5)), GRAY, 32, 149)
wall7 = StaticObjects(pygame.Surface((32, 9)), GRAY, 0, 143)
wall8 = StaticObjects(pygame.Surface((1, 16)), GRAY, 0, 127)
wall9 = StaticObjects(pygame.Surface((20, 1)), GRAY, 0, 127)
staticObj = pygame.sprite.Group()
moveObj = pygame.sprite.Group()

staticObj.add(wall1)
staticObj.add(wall2)
staticObj.add(wall3)
staticObj.add(wall4)
staticObj.add(wall5)
staticObj.add(wall6)
staticObj.add(wall7)
staticObj.add(wall8)
staticObj.add(wall9)
moveObj.add(crate)

spikes = pygame.rect.Rect(116, 32, 16, 117)
