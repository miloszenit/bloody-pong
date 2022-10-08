import pygame, sys, random

def ball_movement():
	global ball_speed_x, ball_speed_y, player_score, computer_player_score
	
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		ball_speed_y *= -1

	# Player score	
	if ball.left <= 0: 
		ball_reset()
		player_score += 1

	# Computer player score
	if ball.right >= screen_width:
		ball_reset()
		computer_player_score += 1

	if ball.colliderect(player) or ball.colliderect(computer_player):
		ball_speed_x *= -1

def player_movement():
	player.y += player_speed

	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height

def computer_player_movement():
	if computer_player.top < ball.y:
		computer_player.y += computer_player_speed
	if computer_player.bottom > ball.y:
		computer_player.y -= computer_player_speed

	if computer_player.top <= 0:
		computer_player.top = 0
	if computer_player.bottom >= screen_height:
		computer_player.bottom = screen_height

def ball_reset():
	global ball_speed_x, ball_speed_y

	ball.center = (screen_width/2, screen_height/2)
	ball_speed_y *= random.choice((1,-1))
	ball_speed_x *= random.choice((1,-1))	
		
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
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
computer_player = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

bg_color = '#1E1D1D'
my_color = '#C32E2E'

# Variables
ball_speed_x = 5 * random.choice((1,-1))
ball_speed_y = 5 * random.choice((1,-1))
player_speed = 0
computer_player_speed = 5

# Score
player_score = 0
computer_player_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player_speed -= 4
			if event.key == pygame.K_DOWN:
				player_speed += 4
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				player_speed += 4
			if event.key == pygame.K_DOWN:
				player_speed -= 4
				
	ball_movement()
	player_movement()
	computer_player_movement()

	screen.fill(bg_color)
	pygame.draw.rect(screen, my_color, computer_player)
	pygame.draw.rect(screen, my_color, player)
	pygame.draw.ellipse(screen, my_color, ball)
	pygame.draw.aaline(screen, my_color, (screen_width / 2, 0),(screen_width / 2, screen_height))
	
	player_text = basic_font.render(f'{player_score}', False, my_color)
	screen.blit(player_text,(430, 30))

	computer_player_text = basic_font.render(f'{computer_player_score}', False, my_color)
	screen.blit(computer_player_text,(355, 30))

	pygame.display.flip()
	clock.tick(140)
