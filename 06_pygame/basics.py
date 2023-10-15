import pygame
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")

x = 50
y = 50
width = 40
height = 60
vel = 5

is_jump = False
jump_count = 10

run = True

while run:
    pygame.time.delay(100) # This will delay the game the given amount of milliseconds. In our casee 0.1 seconds will be the delay

    for event in pygame.event.get():  # This will loop through a list of any keyboard or mouse events.
        if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
            run = False  # Ends the game loop
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] & (x > 0) :
        x = x-vel
    if keys[pygame.K_RIGHT] & (x < (500 -vel -width)):
        x = x+vel
        
    if not is_jump:
        if keys[pygame.K_UP] & (y > 0):
            y = y-vel
        if keys[pygame.K_DOWN] & (y < (500 -vel - height)   ):
            y = y+vel
            
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            y -= (jump_count**2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 10
    
    win.fill((0,0,0))
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

pygame.quit()  # If we exit the loop this will execute and close our game