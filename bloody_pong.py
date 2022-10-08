import pygame, sys

def ball_movement():
	global ball_speed_x, ball_speed_y
	
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		ball_speed_y *= -1
	if ball.left <= 0 or ball.right >= screen_width:
		ball_speed_x *= -1

	if ball.colliderect(player) or ball.colliderect(computer):
		ball_speed_x *= -1

def player_movement():
	player.y += player_speed

	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height
		
# BloddyPong general setup
pygame.init()
clock = pygame.time.Clock()

# Main window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Welcome to BloodyPong!')

# Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
computer = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
player = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

bg_color = '#1E1D1D'
my_color = '#C32E2E'

# Variables
ball_speed_x = 10
ball_speed_y = 10
player_speed = 0

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player_speed -= 10
			if event.key == pygame.K_DOWN:
				player_speed += 10
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				player_speed += 10
			if event.key == pygame.K_DOWN:
				player_speed -= 10
				
	ball_movement()
	player_movement()

	screen.fill(bg_color)
	pygame.draw.rect(screen, my_color, computer)
	pygame.draw.rect(screen, my_color, player)
	pygame.draw.ellipse(screen, my_color, ball)
	pygame.draw.aaline(screen, my_color, (screen_width / 2, 0),(screen_width / 2, screen_height))
	
	pygame.display.flip()
	clock.tick(140)
