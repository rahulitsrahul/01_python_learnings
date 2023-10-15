import pygame

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

 

# Main loop
if __name__ == "__main__":
    run = True
    while run:
        clock.tick(27) #

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()