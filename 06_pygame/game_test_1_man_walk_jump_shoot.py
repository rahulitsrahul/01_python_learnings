import pygame

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.man_dir = 1 # direction of player facing, -1 -> left, 1 -> right

    def draw(self, win):
        if self.walkCount + 1 >= 9:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount], (self.x,self.y))
                self.walkCount += 1
                self.man_dir = -1
                print(f"Left: walk count: {self.walkCount}")
            elif self.right:
                win.blit(walkRight[self.walkCount], (self.x,self.y))
                self.walkCount +=1
                self.man_dir = 1
                print(f"Right: walk count: {self.walkCount}")
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

class projectice(object):
    def __init__(self, x=200, y=400, radius=10, color=(0,0,0), facing=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facig = facing # [either -1 or 1] 1 if right -1 if leftf
        self.vel = 8
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        
        

def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update()


def operate_player(keys, man):
    global jmp_count_list, player_y
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    
    if keys[pygame.K_UP] & (man.isJump == False):
        man.isJump = True
        jmp_count_list = [((-2* i**2) + 200) for i in range(-man.jumpCount, man.jumpCount+1)]
    
    if man.isJump:
        if len(jmp_count_list)>0:
            man.y = player_y - jmp_count_list.pop(0)
            print(f"JUMP  val: {man.y}")
        else:
            man.isJump = False


def operate_bullets(keys, man):
    global bullets, trigger
        
    def is_touched_border(bullet):
        if ((bullet.x < 0) | (bullet.x > 500)):
            return True
        else:
            return False
    
    if keys[pygame.K_SPACE] & (trigger == False):
        if(len(bullets) < 1):
            bullets.append(projectice())
        print("Fired")
        trigger = True
        bullets[0].x = man.x
        bullets[0].y = man.y
        bullets[0].facing = man.man_dir
        
    if trigger:
        if (not is_touched_border(bullets[0])):
            bullets[0].x = bullets[0].x + (bullets[0].facing * bullets[0].vel)
            bullets[0].y = bullets[0].y
            # print(f"Bullet moving at {bullets[0].x}")
        else:
            # print("Trigger Disabled")
            trigger = False
            bullets.pop(0)


if __name__ == "__main__":
    # Initialize Game window
    pygame.init()
    win = pygame.display.set_mode((500,480))
    pygame.display.set_caption("First Game")
    clock = pygame.time.Clock()

    # Load the sprites and images
    walkRight = [pygame.image.load(f"R{i}.png") for i in range(1,10)]
    walkLeft = [pygame.image.load(f"L{i}.png") for i in range(1,10)]
    bg = pygame.image.load('bg.jpg')
    char = pygame.image.load('standing.png')
    
    jmp_count_list = []
    player_x = 200
    player_y = 410
    
    trigger = False
    
    
    # Initlaize Player
    man = player(player_x, player_y, 64,64)
    
    # Initialize Bullets
    bullets = []
    
    
    run = True
    while run:
        clock.tick(20) #

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Initialize Keys
        keys = pygame.key.get_pressed()
        # Operate Player
        operate_player(keys=keys, man=man)
        # Operate Bullets
        operate_bullets(keys=keys, man=man)
        
        redrawGameWindow()
    
    pygame.quit()