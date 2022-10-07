import pygame, sys

pygame.init()
clock = pygame.time.Clock()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Welcome to BloodyPong!')

ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
computer = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
player = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

bg_color = '#1E1D1D'
my_color = '#C32E2E'

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill(bg_color)
	pygame.draw.rect(screen, my_color, computer)
	pygame.draw.rect(screen, my_color, player)
	pygame.draw.ellipse(screen, my_color, ball)
	pygame.draw.aaline(screen, my_color, (screen_width / 2, 0),(screen_width / 2, screen_height))
	
	pygame.display.flip()
	clock.tick(140)
