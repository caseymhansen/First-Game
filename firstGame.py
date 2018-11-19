import pygame
pygame.font.init()
pygame.mixer.init()
# Sets the window size
win = pygame.display.set_mode((500, 480))
# Sets game caption
pygame.display.set_caption("First Game")

# Images for when Boi is walking right
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
# Images for when Boi is walking left
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
score = 0

# Game Clock
clock = pygame.time.Clock()

# Sounds
bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.15)

# Creates the Player Object
class player(object):
    # Initializes the Player variables
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 19, self.y + 11, 26, 52)

    # Draws the Character
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 19, self.y + 11, 26, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    # Subtracts 5 from the player's score when they get hit by the enemy
    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('Comic Sans MS', 100)
        text = font1.render("-5", 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101
                    pygame.quit()

# Creates the Enemy Object
class enemy(object):
    # Images for when enemy is walking right
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    # Images for when enemy is walking left
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    # Initializes the Enemy variables
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    # Draws the enemy
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 10, 50, 5))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 10, 50 - (5 * (10 - self.health)), 5))

    # Subtracts from the enemy's health when hit with a bullet
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        # print('hit')

    # Moves the enemy between 2 points
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0

# Creates the projectile objects or bullets
class projectile(object):
    # Initializes the projectile variables
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    # Draws the projectiles or bullets
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

# Draws the background and sprite animations for each frame
def redrawGameWindow():
    win.blit(bg, (0, 0))
    boi.draw(win)
    meanBoi.draw(win)
    text = font.render("Score: " + str(score), 1, (0, 0, 0))
    win.blit(text, (350, 10))
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


# Main Loop
font = pygame.font.SysFont('Comic Sans MS', 24, True)
boi = player(300, 410, 64, 64)  # Creates the player
meanBoi = enemy(100, 410, 64, 64, 450)  # Creates the enemy
shootLoop = 0  # Used to prevent bullets from shooting on top of each other
bullets = []  # Bullet array
run = True
while run:
    # Sets the framerate
    clock.tick(27)

    if meanBoi.visible:
        # Code for when the player and enemy collie
        if boi.hitbox[1] < meanBoi.hitbox[1] + meanBoi.hitbox[3] and boi.hitbox[1] + boi.hitbox[3] > meanBoi.hitbox[1]:
            if boi.hitbox[0] + boi.hitbox[2] > meanBoi.hitbox[0] and boi.hitbox[0] < meanBoi.hitbox[0] + meanBoi.hitbox[2]:
                boi.hit()
                score -= 5

    # Prevents multiple bullets from shooting on top of each other
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    # Closes the game window when the X in the top left is clicked
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        # Checks if bullet is within the Y range of the enemy's hitbox
        if bullet.y - bullet.radius < meanBoi.hitbox[1] + meanBoi.hitbox[3] and bullet.y + bullet.radius > meanBoi.hitbox[1]:
            # Checks if the bullet is within the X range of the enemy's hitbox
            if bullet.x + bullet.radius > meanBoi.hitbox[0] and bullet.x - bullet.radius < meanBoi.hitbox[0] + meanBoi.hitbox[2]:
                hitSound.play()  # Plays the hit sound
                meanBoi.hit()  # Subtracts enemy health
                score += 1  # Increments the player's score by 1
                bullets.pop(bullets.index(bullet))
        if bullet.x < 500 and bullet.x > 0:  # Moves the bullet across the screen
            bullet.x += bullet.vel
        else:  # Deletes bullet from screen when it hits the each of the window
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    # Code for shooting bullets
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if boi.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(boi.x + boi.width // 2), round(boi.y + boi.height // 2), 6, (0, 0, 0), facing))
        shootLoop = 1

    # Code for moving left
    if keys[pygame.K_a] and boi.x > boi.vel:
        boi.x -= boi.vel
        boi.left = True
        boi.right = False
        boi.standing = False
    # Code for moving right
    elif keys[pygame.K_d] and boi.x < (500 - boi.width - boi.vel):
        boi.x += boi.vel
        boi.right = True
        boi.left = False
        boi.standing = False
    # Code for not moving
    else:
        boi.standing = True
        boi.walkCount = 0

    # Code for the player jumping
    if not boi.isJump:
        if keys[pygame.K_w]:
            boi.isJump = True
            boi.right = False
            boi.left = False
            boi.walkCount = 0
    else:
        if boi.jumpCount >= -10:
            neg = 1
            if boi.jumpCount < 0:
                neg = -1
            boi.y -= (boi.jumpCount ** 2) * 0.5 * neg
            boi.jumpCount -= 1
        else:
            boi.isJump = False
            boi.jumpCount = 10
    # Redraws the game window each iteration
    redrawGameWindow()
# Closes the pygame window
pygame.quit()
