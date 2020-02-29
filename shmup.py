# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'data/img')


WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # to load image
        # self.image = player_img
        # to scale image
        # self.image = pygame.transform.scale(player_img, (image_width, image_height))
        self.image = pygame.transform.scale(player_img, (50, 38))
        # to make image background transparent
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # set radius for sicular collision
        self.radius = 20
        # draw radius to see is it feets
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
            
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # set radius for sicular collision
        self.radius = int(self.rect.width * 0.85 / 2)
        # draw radius to see is it feets
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -30)
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-2, 2)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.x + 30 < 0 or self.rect.x > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -30)
            self.speedy = random.randrange(2, 5)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
            
# Load all game graphics
background = pygame.image.load(path.join(img_dir, 'background.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
meteor_img = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()

all_sprites = pygame.sprite.Group()
player = Player()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
all_sprites.add(player)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()
    
    # check to see if a bullet hit mob
    # True means that every mob that is hitted 
    # will be deleted and next True means that 
    # bullet will be deleted
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    
    # add killed mobs
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        
    # check to see if a mob hit the player
    # False indicate is thing you hit should 
    # be deleted or not
    # rectangular collision
    # hits = pygame.sprite.spritecollide(player, mobs, False)
    # circlular collision
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    # empty list evaluates to False
    if hits:
        running = False
        

    # Draw / render
    # filling screen with black
    screen.fill(BLACK)
    # setting background
    screen.blit(background, background_rect)
    
    all_sprites.draw(screen)
    
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()