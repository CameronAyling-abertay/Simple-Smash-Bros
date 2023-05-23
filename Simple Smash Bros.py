###ITEMS WITH PERMANENCE

import pygame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Simple Smash Brothers!")

menus = [True, False, False, False]
variables = [180, 2]
stages = [True, False, False, False]

lylatPreview = pygame.image.load("Assets/Menus/previews/lylatPreview.png").convert_alpha()
stadiumPreview = pygame.image.load("Assets/Menus/previews/stadiumPreview.png").convert_alpha()
fdPreview = pygame.image.load("Assets/Menus/previews/fdPreview.png").convert_alpha()
battlefieldPreview = pygame.image.load("Assets/Menus/previews/battlefieldPreview.png").convert_alpha()
previews = [lylatPreview, stadiumPreview, fdPreview, battlefieldPreview]

menuBackdrop = pygame.image.load("Assets/backgrounds/menuBackground.png").convert_alpha()

decreaseArrow = pygame.image.load("Assets/Menus/arrowLeft.png").convert_alpha()
decreaseArrowPressed = pygame.image.load("Assets/Menus/arrowLeftPress.png").convert_alpha()
increaseArrow = pygame.image.load("Assets/Menus/arrowRight.png").convert_alpha()
increaseArrowPressed = pygame.image.load("Assets/Menus/arrowRightPress.png").convert_alpha()

font = pygame.font.Font('C:/WINDOWS/Fonts/consola.TTF', 23)
fontTwo = pygame.font.Font('C:/WINDOWS/Fonts/consola.TTF', 46)

###BUTTON CLASSES

class Button(object):
    def __init__(self, x, y, w, h, text, listPosition):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.listPosition = listPosition
        
    def getRect(self):
        return self.rect

    def getText(self):
        return self.text

class MenuButton(Button):
    def click(self, menus):
        menus = [False, False, False, False]
        menus[self.listPosition] = True
        return menus

class QuitButton(Button):
    def click(self):
        pygame.quit()
        quit()

class VarButton(Button):
    def increase(self):
        if variables[self.listPosition] <= 4:
            variables[self.listPosition] += 1
        if 120 <= variables[self.listPosition] <= 270:
            variables[self.listPosition] += 30

    def decrease(self):
        if 2 <= variables[self.listPosition] <= 5:
            variables[self.listPosition] -= 1
        if 150 <= variables[self.listPosition]:
            variables[self.listPosition] -= 30

    def getVarPos(self):
        return self.listPosition

class StageSelector(Button):
    def click(self, stages):
        stages = [False, False, False, False]
        stages[self.listPosition] = True
        return stages
         
###PLAYER CLASS

class Player (object):
    def __init__(self, x, y, p, lives):
        self.rect = pygame.Rect(x, y, 19, 38)
        self.num = p
        if self.num == 1:
            self.facing = "Right"
        elif self.num == 2:
            self.facing = "Left"
        self.respawnX = x
        self.respawnY = y
        self.air = True
        self.onGround = False
        self.left = False
        self.right = False
        self.yspeed = 0
        self.xspeed = 0
        self.pic = pygame.image.load("Assets/playerItems/player%s%s.png" % (self.num, self.facing)).convert_alpha()
        self.shieldPic = pygame.image.load("Assets/playerItems/player%sshield.png" % self.num).convert_alpha()
        self.jumps = 1
        self.contactFrame = False
        self.walljumps = 1
        self.wall = False
        self.attacking = False
        self.blocking = False
        self.shield = 5000
        self.stunned = False
        self.stunTime = 0
        self.grabbing = False
        self.grabbed = False
        self.grabCooldown = False
        self.throwing = False
        self.attackCooldown = False
        self.dead = False
        self.lives = lives
        self.health = 3
        self.invulnerable = False

    def respawn(self):
        if self.num == 1:
            self.facing = "Right"
        elif self.num == 2:
            self.facing = "Left"
        self.air = True
        self.onGround = False
        self.left = False
        self.right = False
        self.yspeed = 0
        self.xspeed = 0
        self.pic = pygame.image.load("Assets/playerItems/player%s%s.png" % (self.num, self.facing)).convert_alpha()
        self.jumps = 1
        self.contactFrame = False
        self.walljumps = 1
        self.wall = False
        self.attacking = False
        self.blocking = False
        self.shield = 5000
        self.stunned = False
        self.stunTime = 0
        self.grabbing = False
        self.grabbed = False
        self.grabCooldown = False
        self.throwing = False
        self.attackCooldown = False
        self.dead = False
        self.health = 3
        self.invulnerable = False

    def move(self, paused, plats, players):
        enemy = players[self.num%2]

###PAUSED

        if not paused:

###DEAD
        
            if self.dead:
                self.rect.x = 1000
                self.rect.y = 1000
                self.deadTime = pygame.time.get_ticks()
                
                if self.deadTime - self.deadStart > 3000:
                    self.respawn()
                    self.rect = pygame.Rect(self.respawnX, self.respawnY, 19, 38)
                        
            elif not self.grabbed:

###SHIELD
                
                if self.blocking and self.shield > 0:
                    ticks = pygame.time.get_ticks()-self.blockMark
                    self.blockMark = pygame.time.get_ticks()
                    self.shield -= ticks
                    if self.shield < 0:
                        self.blocking = False
                        self.stun(4000)
                        self.shield = 2000
                        
                elif self.shield < 5000:
                    ticks = pygame.time.get_ticks()-self.blockMark
                    self.blockMark = pygame.time.get_ticks()
                    self.shield += ticks

                elif self.shield > 5000:
                    self.shield = 5000

###MOVEMENT
                        
                self.rect.x += self.xspeed
                
                contactPlats = self.checkContact(plats)
                self.wall = False
                if self.contactFrame:
                    if self.xspeed < 0:
                        self.rect.left = contactPlats[0].getRect().right
                    if self.xspeed > 0:
                        self.rect.right = contactPlats[0].getRect().left
                    self.wall = True
                    self.xspeed = 0
                    
                if not enemy.getGrabbed() and not self.blocking and not self.stunned:
                    if self.left:
                        if not self.right and self.xspeed > 0:
                            self.xspeed -= 1
                        if self.xspeed > -13:
                            self.xspeed -= 1

                    if self.right:
                        if not self.left and self.xspeed < 0:
                            self.xspeed += 1
                        if self.xspeed < 13:
                            self.xspeed += 1

                if ((self.right and not self.left) or (self.left and not self.right)) and not self.blocking and not self.stunned:
                    if self.right:
                        self.facing = "Right"
                        self.pic = pygame.image.load("Assets/playerItems/player%s%s.png" % (self.num, self.facing)).convert_alpha()
                    if self.left:
                        self.facing = "Left"
                        self.pic = pygame.image.load("Assets/playerItems/player%s%s.png" % (self.num, self.facing)).convert_alpha()

                if (not self.right and not self.left and self.xspeed != 0) or (self.left and self.right) or enemy.getGrabbed() or self.blocking:
                    if not self.air:
                        if self.xspeed > 0:
                            self.xspeed -= 1
                        if self.xspeed < 0:
                            self.xspeed += 1
                    else:
                        if self.xspeed > 0:
                            self.xspeed -= 0.25
                        if self.xspeed < 0:
                            self.xspeed += 0.25
                        
                if self.air:
                    self.rect.y -= self.yspeed
                    self.yspeed -= 0.5
                    if self.wall:
                        if contactPlats[0].getRect().top - 5 <= self.rect.top < contactPlats[0].getRect().top + 5:
                            self.rect.top = contactPlats[0].getRect().top
                            self.yspeed = 0
                            self.air = False
                            self.walljumps = 1
                            self.jumps = 1
                        elif self.yspeed < -4:
                            self.yspeed = -4
                    else:
                        if self.yspeed < -20:
                            self.yspeed = -20
                            
                contactPlats = self.checkContact(plats)
                if self.contactFrame or self.onGround:
                    if self.yspeed < 0.5: 
                        self.rect.bottom = contactPlats[len(contactPlats)-1].getRect().top
                        self.air = False
                        self.jumps = 2
                        self.walljumps = 1
                    if self.yspeed > 0 and not self.onGround:
                        self.rect.top = contactPlats[0].getRect().bottom
                    self.yspeed = 0
                else:
                    self.air = True

###ATTACKING

                if self.attacking or self.attackCooldown:
                    self.attackTime = pygame.time.get_ticks()
                    if self.attackTime - self.attackStart > 100:
                        self.attacking = False
                        self.attackCooldown = True
                    if self.attackTime - self.attackStart > 300:
                        self.attackCooldown = False
                if self.attacking:
                    if self.blocking or self.grabbing:
                        self.attacking = False
                    else:
                        if self.facing == "Left":
                            sword = pygame.Rect(self.rect.x-19, self.rect.y+19, 19, 9)
                        else:
                            sword = pygame.Rect(self.rect.x+19, self.rect.y+19, 19, 9)
                        if sword.colliderect(enemy.getRect()):
                            if not enemy.getInvul():
                                if enemy.getAttacking():
                                    if not enemy.simulate(players):
                                        enemy.damage(players)
                                    else:
                                        self.yspeed = 13
                                        self.air = True
                                        if self.facing == "Left":
                                            self.xspeed = 13
                                            enemy.changeMomentum(13, -13)
                                        else:
                                            self.xspeed = -13
                                            enemy.changeMomentum(13, 13)
                                elif not enemy.getBlock():
                                    enemy.damage(players)

###GRABBING

                if self.grabbing:
                    if self.rect.colliderect(enemy.getRect()) and not enemy.getInvul():
                        enemy.changeGrabbed(True)
                        self.xspeed = 0
                    if pygame.time.get_ticks() - self.grabTime > 200:
                        self.grabbing = False
                        self.grabCooldown = True
                        self.grabCooldownStart = pygame.time.get_ticks()
                if self.grabCooldown:
                    if pygame.time.get_ticks() - self.grabCooldownStart > 800:
                        self.grabCooldown = False

###THROWING

                if self.throwing:
                    self.throwing = False
                    enemy.changeGrabbed(False)
                    enemy.stun(600)
                    if self.facing == "Left":
                        enemy.throw("Left")
                    else:
                        enemy.throw("Right")

###STATUSES

            elif self.grabbed:
                if pygame.time.get_ticks() - self.grabStart < 500:
                    if enemy.getFacing() == "Left":
                        self.facing = "Right"
                        self.rect.x = enemy.getRect().x-19
                        self.rect.y = enemy.getRect().y-10
                    else:
                        self.facing = "Left"
                        self.rect.x = enemy.getRect().x+19
                        self.rect.y = enemy.getRect().y-10
                    self.pic = pygame.image.load("Assets/playerItems/player%s%s.png" % (self.num, self.facing)).convert_alpha()
                else:
                    self.grabbed = False
                    self.invulnerable = True
                    self.invulTime = 300
                    self.invulMark = pygame.time.get_ticks()

            if self.stunned:
                ticks = pygame.time.get_ticks() - self.stunMark
                self.stunMark = pygame.time.get_ticks()
                self.stunTime -= ticks
                if self.stunTime <= 0:
                    self.stunned = False

            if self.invulnerable:
                ticks = pygame.time.get_ticks()-self.invulMark
                self.invulMark = pygame.time.get_ticks()
                self.invulTime -= ticks
                if self.invulTime <= 0:
                    self.invulnerable = False

###MOVEMENT ALTERATION FUNCTIONS

    def dirChange(self, left, state):
        if left:
            self.left = state
        else:
            self.right = state

    def jump(self, players):
        if not players[self.num%2].getGrabbed() and not self.blocking and not self.grabbed and not self.stunned:
            if self.walljumps != 0 and self.wall:
                self.yspeed = 13
                self.walljumps -= 1
                if self.jumps != 0:
                    self.jumps -= 1
                if self.xspeed > 0:
                    self.xspeed = -13
                else:
                    self.xspeed = 13
                    
            elif self.jumps != 0:
                self.yspeed = 13
                self.air = True
                self.jumps -= 1

    def checkContact(self, plats):
        self.contactFrame = False
        self.onGround = False
        contactPlats = []
        for p in plats:
            if self.rect.colliderect(p.getRect()) == True:
                self.contactFrame = True
                contactPlats.append(p)
        for p in plats:
            if p.rect.collidepoint(self.rect.left+1, self.rect.bottom+1) or \
               p.rect.collidepoint(self.rect.right-1, self.rect.bottom+1):
                self.onGround = True
                contactPlats.append(p)
        return contactPlats

    def changeMomentum(self, y, x):
        if y > 0:
            self.air = True
        self.yspeed = y
        self.xspeed = x

###ATTACKING FUNCTIONS

    def kill(self):
        self.dead = True
        self.lives -= 1
        self.deadStart = pygame.time.get_ticks()

    def attack(self, players):
        if not self.attackCooldown and not self.attacking and not self.grabbing and not players[self.num%2].getGrabbed() and not self.stunned:
            self.attacking = True
            self.attackStart = pygame.time.get_ticks()
        if players[self.num%2].getGrabbed():
            self.throwing = True

    def damage(self, players):
        self.stunned = False
        self.stunTime = 0
        self.invulnerable = True
        self.invulTime = 300
        self.invulMark = pygame.time.get_ticks()
        if players[self.num%2].getFacing() == "Left":
            self.xspeed = -8
        else:
            self.xspeed = 8
        self.yspeed = 8
        self.air = True
        self.health -= 1
        if self.health == 0:
            self.kill()

    def simulate(self, players):
        if self.facing == "Left":
            sword = pygame.Rect(self.rect.x-19, self.rect.y+19, 19, 9)
        else:
            sword = pygame.Rect(self.rect.x+19, self.rect.y+19, 19, 9)
        temp = False
        for p in players:
            if sword.colliderect(p.getRect()):
                temp = True
        return temp

###OTHER COMBAT FUNCTIONS

    def throw(self, direction):
        self.yspeed = 13
        self.air = True
        if direction == "Left":
            self.xspeed = -13
        else:
            self.xspeed = 13
        self.stunned = True

    def grab(self):
        if not self.grabbing and not self.grabCooldown and not self.attacking and not self.stunned and not self.blocking:
            self.yspeed = 4
            self.grabbing = True
            self.air = True
            if self.facing == "Left":
                self.xspeed = -8
            else:
                self.xspeed = 8
            self.grabTime = pygame.time.get_ticks()

    def changeGrabbed(self, state):
        self.xspeed = 0
        self.yspeed = 0
        self.grabbed = state
        if state:
            self.blocking = False
            self.grabStart = pygame.time.get_ticks()

    def changeBlock(self, state):
        if not self.stunned:
            if state:
                self.xspeed = 0
                if self.yspeed > 0:
                    self.yspeed = 0
                self.blockMark = pygame.time.get_ticks()
            if not self.grabbed and self.shield > 0:
                self.blocking = state

    def stun(self, time):
        self.stunned = True
        self.stunMark = pygame.time.get_ticks()
        if self.stunTime < time:
            self.stunTime = time

###GETTER FUNCTIONS

    def getPic(self):
        return self.pic

    def getShield(self):
        return self.shieldPic

    def getFacing(self):
        return self.facing

    def getBlock(self):
        return self.blocking

    def getInvul(self):
        return self.invulnerable

    def getGrabbed(self):
        return self.grabbed

    def getAttacking(self):
        return self.attacking

    def getDead(self):
        return self.dead

    def getRect(self):
        return self.rect

    def getLives(self):
        return self.lives

    def getHealth(self):
        return self.health

###PLATFORM CLASS
    
class Platform(object):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def getRect(self):
        return self.rect

###STAGE FUNCTIONS

def stadium():
    background = pygame.image.load("Assets/backgrounds/stadiumBackground.png").convert_alpha()
    
    left = Platform(150, 450, 150, 25)
    right = Platform(900, 450, 150, 25)
    floor = Platform(100, 600, 1000, 400)

    plats = [left, right, floor]

    sRespawnX = 300
    sRespawnY = 562
    oRespawnX = 881
    oRespawnY = 562

    return sRespawnX, sRespawnY, oRespawnX, oRespawnY, plats, background

def lylat():
    background = pygame.image.load("Assets/backgrounds/spaceBackground.png").convert_alpha()
    
    left = Platform(350, 350, 100, 25)
    middle = Platform(550, 350, 100, 25)
    right = Platform(750, 350, 100, 25)
    floor = Platform(250, 500, 700, 60)

    plats = [left, middle, right, floor]

    sRespawnX = 300
    sRespawnY = 462
    oRespawnX = 881
    oRespawnY = 462

    return sRespawnX, sRespawnY, oRespawnX, oRespawnY, plats, background

def fd():
    background = pygame.image.load("Assets/backgrounds/voidBackground.png").convert_alpha()
    
    floor = Platform(200, 600, 800, 60)

    plats = [floor]

    sRespawnX = 300
    sRespawnY = 562
    oRespawnX = 881
    oRespawnY = 562

    return sRespawnX, sRespawnY, oRespawnX, oRespawnY, plats, background

def battlefield():
    background = pygame.image.load("Assets/backgrounds/skyBackground.png").convert_alpha()
    
    left = Platform(300, 450, 200, 25)
    middle = Platform(500, 300, 200, 25)
    right = Platform(700, 450, 200, 25)
    floor = Platform(200, 600, 800, 60)

    plats = [left, middle, right, floor]

    sRespawnX = 300
    sRespawnY = 562
    oRespawnX = 881
    oRespawnY = 562

    return sRespawnX, sRespawnY, oRespawnX, oRespawnY, plats, background

###GAME FUNCTION

def game(clock, screen, stages, variables, menus):

###GAME SETUP

    swordLeft = pygame.image.load("Assets/playerItems/swordLeft.png").convert_alpha()
    swordRight = pygame.image.load("Assets/playerItems/swordRight.png").convert_alpha()

    zero = pygame.image.load("Assets/numbers/zero.png").convert_alpha()
    one = pygame.image.load("Assets/numbers/one.png").convert_alpha()
    two = pygame.image.load("Assets/numbers/two.png").convert_alpha()
    three = pygame.image.load("Assets/numbers/three.png").convert_alpha()
    four = pygame.image.load("Assets/numbers/four.png").convert_alpha()
    five = pygame.image.load("Assets/numbers/five.png").convert_alpha()
    six = pygame.image.load("Assets/numbers/six.png").convert_alpha()
    seven = pygame.image.load("Assets/numbers/seven.png").convert_alpha()
    eight = pygame.image.load("Assets/numbers/eight.png").convert_alpha()
    nine = pygame.image.load("Assets/numbers/nine.png").convert_alpha()
    colon = pygame.image.load("Assets/numbers/colon.png").convert_alpha()

    stefanHead = pygame.image.load("Assets/HUD/player1Head.png").convert_alpha()
    olgaHead = pygame.image.load("Assets/HUD/player2Head.png").convert_alpha()

    fullHealth = pygame.image.load("Assets/HUD/fullHealth.png").convert_alpha()
    oTwoHealth = pygame.image.load("Assets/HUD/right23Health.png").convert_alpha()
    oOneHealth = pygame.image.load("Assets/HUD/right13Health.png").convert_alpha()
    sTwoHealth = pygame.image.load("Assets/HUD/left23Health.png").convert_alpha()
    sOneHealth = pygame.image.load("Assets/HUD/left13Health.png").convert_alpha()
    aliveLife = pygame.image.load("Assets/HUD/crystal.png").convert_alpha()
    goneLife = pygame.image.load("Assets/HUD/emptyCrystal.png").convert_alpha()

    stefanWin = pygame.image.load("Assets/Menus/stefanWin.png").convert_alpha()
    olgaWin = pygame.image.load("Assets/Menus/olgaWin.png").convert_alpha()
    draw = pygame.image.load("Assets/Menus/draw.png").convert_alpha()

    background = pygame.Rect(-300, -300, 1800, 1400)

    if stages[0]:
        sRespawnX, sRespawnY, oRespawnX, oRespawnY, plats, backdrop = lylat()
    elif stages[1]:
        sRespawnX, sRespawnY, oRespawnX, oRespawnY, plats, backdrop = stadium()
    elif stages[2]:
        sRespawnX, sRespawnY, oRespawnX, oRespawnY, plats, backdrop = fd()
    elif stages[3]:
        sRespawnX, sRespawnY, oRespawnX, oRespawnY, plats, backdrop = battlefield()

    stefan = Player(sRespawnX, sRespawnY, 1, variables[1])
    olga = Player(oRespawnX, oRespawnY, 2, variables[1])

    players = [stefan, olga]

    SECONDPASSED = pygame.USEREVENT + 1
    pygame.time.set_timer(SECONDPASSED, 1000)

    paused = False

    resumeButton = Button(500, 340, 200, 50, "Resume", None)
    quitButton = MenuButton(500, 410, 200, 50, "Main Menu", 0)
    buttons = [resumeButton, quitButton]
    returnToMain = False

###GAME START

    timeLeft = 2

    while timeLeft >= 0:
        screen.blit(backdrop, (0,0))
        screen.blit(stefan.getPic(), (stefan.getRect().left-6, stefan.getRect().top-6))
        screen.blit(olga.getPic(), (olga.getRect().left, olga.getRect().top-6))
        screen.blit(stefanHead, (10, 10))
        screen.blit(olgaHead, (1070, 10))
        for i in range(0, variables[1]):
            screen.blit(goneLife, (140+i*50, 10))
            screen.blit(goneLife, (1015-i*50, 10))

        for i in range(0, stefan.getLives()):
            screen.blit(aliveLife, (140+i*50, 10))

        for i in range(0, olga.getLives()):
            screen.blit(aliveLife, (1015-i*50, 10))

        if stefan.getHealth() == 3:
            screen.blit(fullHealth, (140, 80))
        if stefan.getHealth() == 2:
            screen.blit(sTwoHealth, (140, 80))
        if stefan.getHealth() == 1:
            screen.blit(sOneHealth, (140, 80))
            
        if olga.getHealth() == 3:
            screen.blit(fullHealth, (880, 80))
        if olga.getHealth() == 2:
            screen.blit(oTwoHealth, (880, 80))
        if olga.getHealth() == 1:
            screen.blit(oOneHealth, (880, 80))

        for p in plats:
            pygame.draw.rect(screen, (200, 200, 200), p.getRect())
                 
        temp = []
        if timeLeft+1 == 1:
            temp.append(one)
        if timeLeft+1 == 2:
            temp.append(two)
        if timeLeft+1 == 3:
            temp.append(three)
        screen.blit(temp[0], (570, 355))

        for event in pygame.event.get():
            if event.type == SECONDPASSED:
                timeLeft -=1

        pygame.display.update()
        clock.tick(60)

    timeLeft = variables[0]

###MAIN LOOP 

    while stefan.getLives() != 0 and olga.getLives() != 0 and timeLeft > 0 and returnToMain == False:

###USER INPUTS
###PLAYER 1
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    stefan.jump(players)
                if event.key == pygame.K_a:
                    stefan.dirChange(True, True)
                if event.key == pygame.K_d:
                    stefan.dirChange(False, True)

                if event.key == pygame.K_g:
                    stefan.attack(players)
                if event.key == pygame.K_h:
                    stefan.grab()
                if event.key == pygame.K_j:
                    stefan.changeBlock(True)
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    stefan.dirChange(True, False)
                if event.key == pygame.K_d:
                    stefan.dirChange(False, False)
                if event.key == pygame.K_j:
                    stefan.changeBlock(False)

###PLAYER 2

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    olga.jump(players)
                if event.key == pygame.K_LEFT:
                    olga.dirChange(True, True)
                if event.key == pygame.K_RIGHT:
                    olga.dirChange(False, True)

                if event.key == pygame.K_KP1:
                    olga.attack(players)
                if event.key == pygame.K_KP2:
                    olga.grab()
                if event.key == pygame.K_KP3:
                    olga.changeBlock(True)
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    olga.dirChange(True, False)
                if event.key == pygame.K_RIGHT:
                    olga.dirChange(False, False)
                if event.key == pygame.K_KP3:
                    olga.changeBlock(False)

###MULTIUSE

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                if event.key == pygame.K_p:
                    paused = True
                    inMenu = True
                    stefan.dirChange(True, False)
                    stefan.dirChange(False, False)
                    olga.dirChange(True, False)
                    olga.dirChange(False, False)
                    
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

###TIMING

            if event.type == SECONDPASSED and not paused:
                timeLeft -= 1

###PLAYER ORDER

        standInList = players
        if stefan.getGrabbed():
            standInList = reversed(players)

###VISUAL REPRESENTATION

        screen.blit(backdrop, (0, 0))

        for player in standInList:
            player.move(paused, plats, players)
            
            if not player.getDead():
                if not player.getRect().colliderect(background):
                    player.kill()

            if not player.getDead():
                if player.getFacing() == "Left":
                    screen.blit(player.getPic(), (player.getRect().x, player.getRect().y-6))
                    if player.getAttacking():
                        screen.blit(swordLeft, (player.getRect().x-19, player.getRect().y+19))
                else:
                    screen.blit(player.getPic(), (player.getRect().x-6, player.getRect().y-6))
                    if player.getAttacking() and not player.getGrabbed():
                        screen.blit(swordRight, (player.getRect().x+19, player.getRect().y+19))
                if player.getBlock():
                    screen.blit(player.getShield(), (player.getRect().x-15, player.getRect().y-6))

        print(clock.get_fps())

        for p in plats:
            pygame.draw.rect(screen, (200, 200, 200), p.getRect())

        timeList = [int(timeLeft / 60), ":", int((timeLeft%60) / 10), timeLeft%60%10]
        temp = []
        for i in timeList:
            if i == 0:
                temp.append(zero)
            if i == 1:
                temp.append(one)
            if i == 2:
                temp.append(two)
            if i == 3:
                temp.append(three)
            if i == 4:
                temp.append(four)
            if i == 5:
                temp.append(five)
            if i == 6:
                temp.append(six)
            if i == 7:
                temp.append(seven)
            if i == 8:
                temp.append(eight)
            if i == 9:
                temp.append(nine)
            if i == ":":
                temp.append(colon)
        timeList = temp

        for i, j in zip(timeList, range(0, 4)):
            screen.blit(i, (495+j*60, 20))

        screen.blit(stefanHead, (10, 10))
        screen.blit(olgaHead, (1070, 10))
        
        for i in range(0, variables[1]):
            screen.blit(goneLife, (140+i*50, 10))
            screen.blit(goneLife, (1015-i*50, 10))

        for i in range(0, stefan.getLives()):
            screen.blit(aliveLife, (140+i*50, 10))

        for i in range(0, olga.getLives()):
            screen.blit(aliveLife, (1015-i*50, 10))

        if stefan.getHealth() == 3:
            screen.blit(fullHealth, (140, 80))
        if stefan.getHealth() == 2:
            screen.blit(sTwoHealth, (140, 80))
        if stefan.getHealth() == 1:
            screen.blit(sOneHealth, (140, 80))
            
        if olga.getHealth() == 3:
            screen.blit(fullHealth, (880, 80))
        if olga.getHealth() == 2:
            screen.blit(oTwoHealth, (880, 80))
        if olga.getHealth() == 1:
            screen.blit(oOneHealth, (880, 80))

###PAUSE MENU

        while paused:
            print(clock.get_fps())
            while inMenu:
                screen.blit(menuBackdrop, (0,0))
                for i in buttons:
                    pygame.draw.rect(screen, (150, 150, 150), i.getRect())
                    if i.getRect().collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(screen, (180, 180, 180), i.getRect())
                        
                    text = font.render(i.getText(), 100, (0,0,0))
                    position = (i.getRect().left+(i.getRect().width-font.size(i.getText())[0])/2, i.getRect().top+(i.getRect().height-font.size(i.getText())[1])/2)
                    screen.blit(text, position)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i in buttons:
                            if i.getRect().collidepoint(pygame.mouse.get_pos()):
                                if type(i) == MenuButton:
                                    menus = i.click(menus)
                                    returnToMain = True
                                    paused = False
                                        
                                inMenu = False
                                pauseTime = 3
                                pygame.time.set_timer(SECONDPASSED, 1000)

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    
                pygame.display.update()
                clock.tick(60)

            if pauseTime >= 0 and not returnToMain:
                screen.blit(backdrop, (0,0))
                for p in players:
                    if p.getFacing() == "Right":
                        screen.blit(p.getPic(), (p.getRect().left-6, p.getRect().top-6))
                    else:
                        screen.blit(p.getPic(), (p.getRect().left, p.getRect().top-6))
                screen.blit(stefanHead, (10, 10))
                screen.blit(olgaHead, (1070, 10))
                for i in range(0, variables[1]):
                    screen.blit(goneLife, (140+i*50, 10))
                    screen.blit(goneLife, (1015-i*50, 10))

                for i in range(0, stefan.getLives()):
                    screen.blit(aliveLife, (140+i*50, 10))

                for i in range(0, olga.getLives()):
                    screen.blit(aliveLife, (1015-i*50, 10))

                if stefan.getHealth() == 3:
                    screen.blit(fullHealth, (140, 80))
                if stefan.getHealth() == 2:
                    screen.blit(sTwoHealth, (140, 80))
                if stefan.getHealth() == 1:
                    screen.blit(sOneHealth, (140, 80))
                    
                if olga.getHealth() == 3:
                    screen.blit(fullHealth, (880, 80))
                if olga.getHealth() == 2:
                    screen.blit(oTwoHealth, (880, 80))
                if olga.getHealth() == 1:
                    screen.blit(oOneHealth, (880, 80))

                for p in plats:
                    pygame.draw.rect(screen, (200, 200, 200), p.getRect())
                         
                temp = []
                if pauseTime == 1:
                    temp.append(one)
                if pauseTime == 2:
                    temp.append(two)
                if pauseTime == 3:
                    temp.append(three)
                screen.blit(temp[0], (570, 355))

                for event in pygame.event.get():
                    if event.type == SECONDPASSED:
                        pauseTime -=1

                if pauseTime == 0:
                    paused = False
                    
            pygame.display.update()
            clock.tick(60)
            
        pygame.display.update()
        clock.tick(60)

###WIN DECLARATION

    if not returnToMain:
        if olga.getLives() > stefan.getLives():
            screen.blit(olgaWin, (395, 295))
        elif stefan.getLives() > olga.getLives():
            screen.blit(stefanWin, (395, 295))
        else:
            screen.blit(draw, (395, 295))

        pygame.display.update()
        clock.tick(60)

        timeLeft = 3
        pygame.time.set_timer(SECONDPASSED, 1000)
        while timeLeft > 0:
            for event in pygame.event.get():
                if event.type == SECONDPASSED:
                    timeLeft -=1

###GAMELOOP

x = 0

while True:

###MAIN MENU
    
    if menus[0]:
        inMenu = True
        startGame = MenuButton(500, 500, 200, 50, "Start Game", 1)
        controlsButton = MenuButton(500, 570, 200, 50, "Controls", 3)
        exitGame = QuitButton(500, 640, 200, 50, "Quit", None)
        buttons = [startGame, controlsButton,exitGame]
        logo = pygame.image.load("Assets/Menus/logo.png").convert_alpha()

###PREGAME MENU

    if menus[1]:
        inMenu = True
        lylatButton = StageSelector(50, 98, 260, 180, "", 0)
        stadiumButton = StageSelector(330, 98, 260, 180, "", 1)
        fdButton = StageSelector(610, 98, 260, 180, "", 2)
        battlefieldButton = StageSelector(890, 98, 260, 180, "", 3)
        
        time = VarButton(500, 371, 200, 50, "Time", 0)
        lives = VarButton(500, 489, 200, 50, "Lives", 1)
        startGame = MenuButton(500, 602, 200, 50, "Start Game", 2)
        backButton = MenuButton(1050, 700, 100, 50, "Back", 0)
        buttons = [lylatButton, stadiumButton, fdButton, battlefieldButton, time, lives, startGame, backButton]

###CONTROLS
        
    if menus[3]:
        inMenu = True
        backButton = MenuButton(1050, 700, 100, 50, "Back", 0)
        buttons = [backButton]
        actions = ["CONTROLS", "Left", "Right", "Jump", "Attack/Throw", "Grab", "Block", "Pause"]
        pOneControls = ["PLAYER ONE", "A", "D", "W", "G", "H", "J", "P"]
        pTwoControls = ["PLAYER TWO", "Left Arrow", "Right Arrow", "Up Arrow", "Keypad 1", "Keypad 2", "Keypad 3", "P"]
        controls = [actions, pOneControls, pTwoControls]
        tempOne = []
        
        for i in controls:
            tempTwo = []
            for j in i:
                tempTwo.append(fontTwo.render(j, 100, (0,0,0)))
            tempOne.append(tempTwo)
        controls = tempOne

###DRAWING THE MENUS
        
    while inMenu:
        print(clock.get_fps())
        
        screen.blit(menuBackdrop, (x,0))
        screen.blit(menuBackdrop, (x-1200, 0))
        
        for i in buttons:
            if menus[1] and buttons.index(i) < 4:
                if not stages[buttons.index(i)]:
                    pygame.draw.rect(screen, (150, 150, 150), i.getRect())
                    if i.getRect().collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(screen, (180, 180, 180), i.getRect())
                else:
                    pygame.draw.rect(screen, (255, 215, 115), i.getRect())
                    
            else:
                pygame.draw.rect(screen, (150, 150, 150), i.getRect())
                if type(i) == VarButton:
                    screen.blit(decreaseArrow, (i.getRect().left, i.getRect().top))
                    screen.blit(increaseArrow, (i.getRect().right-50, i.getRect().top))
                        
                    if i.getRect().collidepoint(pygame.mouse.get_pos()):
                        if pygame.mouse.get_pos()[0] <= i.getRect().left + 50 and pygame.mouse.get_pressed()[0]:
                            screen.blit(decreaseArrowPressed, (i.getRect().left, i.getRect().top))
                        if pygame.mouse.get_pos()[0] >= i.getRect().right - 50 and pygame.mouse.get_pressed()[0]:
                            screen.blit(increaseArrowPressed, (i.getRect().right-50, i.getRect().top))
                        
                if i.getRect().collidepoint(pygame.mouse.get_pos()):
                    if type(i) != VarButton:
                        pygame.draw.rect(screen, (180, 180, 180), i.getRect())

            if type(i) != VarButton:            
                text = font.render(i.getText(), 100, (0,0,0))
                position = (i.getRect().left+(i.getRect().width-font.size(i.getText())[0])/2, i.getRect().top+(i.getRect().height-font.size(i.getText())[1])/2)
                screen.blit(text, position)
            else:
                text = font.render(i.getText(), 100, (0,0,0))
                position = (i.getRect().left+(i.getRect().width-font.size(i.getText())[0])/2, i.getRect().top-((i.getRect().height-font.size(i.getText())[1])/2+font.size(i.getText())[1]))
                screen.blit(text, position)
                
                text = font.render(str(variables[i.getVarPos()]), 100, (0,0,0))
                position = (i.getRect().left+(i.getRect().width-font.size(str(variables[i.getVarPos()]))[0])/2, i.getRect().top+(i.getRect().height-font.size(str(variables[i.getVarPos()]))[1])/2)
                screen.blit(text, position)

        if menus[0]:
            screen.blit(logo, (378, 70))
                    
        if menus[1]:
            for p in previews:
                screen.blit(p, (60+previews.index(p)*280, 108))

        if menus[3]:
            for i in controls:
                for j in i:
                    screen.blit(j, (50+controls.index(i)*400, 100+80*i.index(j)))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons:
                    if i.getRect().collidepoint(pygame.mouse.get_pos()):
                        if type(i) == MenuButton:
                            menus = i.click(menus)
                            
                        if type(i) == StageSelector:
                            stages = i.click(stages)
                                
                        if type(i) == VarButton:
                            if pygame.mouse.get_pos()[0] <= i.getRect().left + 50:
                                i.decrease()
                            if i.getRect().right - 50 <= pygame.mouse.get_pos()[0]:
                                i.increase()

                        if type(i) == QuitButton:
                            i.click()
                                
                        inMenu = False

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        pygame.display.update()
        clock.tick(60)

        x = (x+2)%1200

###RUN GAME
    
    if menus[2]:
        game(clock, screen, stages, variables, menus)
        menus = [True, False, False, False]
        x = 0











    
