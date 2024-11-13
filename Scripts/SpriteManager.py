import pygame, math
from Scripts import CollideObjects as co
from Scripts import Images as img

pygame.init()

class SpriteSheetManager():
    def __init__(self, image):
        super().__init__()
        self.sheet = image
        
    def getCurrentImg(self, width, height, frame, action):
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0,0), (frame * width, action * height, width, height))
        image.set_colorkey((0,0,0))
        return image


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.spriteSheet = img.playerSheet
        self.currentSprite = 0
        self.image = SpriteSheetManager(self.spriteSheet).getCurrentImg(16, 16, self.currentSprite, 7)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.feetRect = pygame.rect.Rect(self.rect.x, self.rect.y + self.rect.height - 2, self.rect.width, 2)
        self.animationSpeed = 0
        self.direction = 0
        self.speed = 0
        self.isRolling = False
        self.iframes = False
        self.rframes = False
        self.health = 2

        self.camX, self.camY = 0, 0
    
    def move(self, speed, keys, isRolling):
        self.speed = speed
        if isRolling and not self.isRolling:
            self.isRolling = True
            self.rframes = True
            self.currentSprite = 0  # Reset sprite for rolling animation
        
        if not any(keys[k] for k in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d)) and not self.isRolling:
            self.speed = 0

        else:
            if not self.isRolling:
                self.rframes = False
                if keys[pygame.K_w]:
                    self.direction = 3
                    self.rect.y -= speed
                if keys[pygame.K_s]:
                    self.direction = 2
                    self.rect.y += speed
                if keys[pygame.K_a]:
                    self.direction = 1
                    self.rect.x -= speed
                if keys[pygame.K_d]:
                    self.direction = 0
                    self.rect.x += speed
            else:
                if self.direction == 0:
                    self.rect.x += speed + 0.5
                elif self.direction == 1:
                    self.rect.x -= speed + 1.5
                elif self.direction == 2:
                    self.rect.y += speed + 0.5
                elif self.direction == 3:
                    self.rect.y -= speed + 1.5
        self.feetRect.x = self.rect.x
        for obj in co.staticObj:
            self.collide(obj.rect)
        for obj in co.moveObj:
            self.collide(obj.rect)
        self.feetRect.y = self.rect.y + self.rect.height - self.feetRect.height
        for obj in co.staticObj:
            self.collide(obj.rect)
        for obj in co.moveObj:
            self.collide(obj.rect)

    def animate(self):
        if self.isRolling:
            self.animationSpeed = 0.25
            action = self.direction + 8  # Rolling animation
        elif self.speed == 0:
            self.animationSpeed = 0.1
            action = self.direction  # Idle animation
        else:
            self.animationSpeed = 0.17
            action = self.direction + 4  # Walking animation
        
        self.currentSprite += self.animationSpeed 
        if self.currentSprite >= 4:  # 4 frames per action
            self.currentSprite = 0
            if self.isRolling:
                self.isRolling = False  # End rolling after one cycle
        
        self.image = SpriteSheetManager(self.spriteSheet).getCurrentImg(16, 16, int(self.currentSprite), action)

    def collide(self, obj):
       if self.feetRect.colliderect(obj):
        overlapX = min(self.feetRect.right - obj.left, obj.right - self.rect.left)
        overlapY = min(self.feetRect.bottom - obj.top, obj.bottom - self.rect.top)
        
        if abs(overlapX) < abs(overlapY): #if you're overlapping more horiz than vert
            if self.feetRect.centerx < obj.centerx:
                self.rect.right = obj.left
            else:
                self.rect.left = obj.right
        else:
            if self.feetRect.centery < obj.centery:
                self.rect.bottom = obj.top 
            else:
                self.rect.top = obj.bottom - self.rect.height + self.feetRect.height
        self.feetRect.x = self.rect.x
        self.feetRect.y = self.rect.y + self.rect.height - self.feetRect.height

    def updateCam(self, screenW, screenH):
        self.camX = self.rect.x - screenW // 2
        self.camY = self.rect.y - screenH // 2
    
    def takeDmg(self, speed, enemy):
        if not self.iframes and not self.rframes:
            if self.rect.colliderect(enemy):
                if not self.health == 0:
                    self.health -= 1
                relX, relY = self.rect.centerx - enemy.centerx, self.rect.centery - enemy.centery
                self.angle = math.atan2(relY, relX)
                self.rect.x += int(speed * 5 * math.cos(self.angle))
                self.rect.y += int(speed * 5 * math.sin(self.angle))
                self.feetRect.x = self.rect.x
                self.feetRect.y = self.rect.y + self.rect.height - self.feetRect.height
                self.iframes = True
    
    def drawHealth(self, surface, half, full):
        if self.health == 2:
            surface.blit(full, (0, 0))
        elif self.health == 1:
            surface.blit(half, (0, 0))   


player = Player(4, 125)
spritesList = pygame.sprite.Group()
spritesList.add(player)

class PressurePlate(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, 16, 16)
        self.rect.x, self.rect.y = x, y
        self.image = img.plateDown
    
    def animate(self, thing):
        if thing.colliderect(self.rect):
            self.image = img.plateDown
        else:
            self.image = img.plateUp
plate = PressurePlate(148, 80)
plateList = pygame.sprite.Group()
plateList.add(plate)

