import pygame, sys, random


class MainBlock(pygame.sprite.Sprite):
	def __init__(self, path, x, y):
		super().__init__()                                            
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect(center = ( x, y))
		pygame.mixer.Sound.play(game_music)


class Player(MainBlock):
	def __init__(self, path, x, y, speed):
		super().__init__(path, x, y)
		self.speed = speed 
		self.movement = 0

	def screen_border(self):
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= screen_height:
			self.rect.bottom = screen_height

	def update(self, ball_group):
		self.rect.y += self.movement
		self.screen_border()


class ComputerPlayer(MainBlock):
	def __init__(self, path, x, y, speed):
		super().__init__(path, x, y)
		self.speed = speed

	def update(self, ball_group):
		if self.rect.top < ball_group.sprite.rect.y:
			self.rect.y += self.speed
		if self.rect.bottom > ball_group.sprite.rect.y:
			self.rect.y -= self.speed
		self.border()

	def border(self):
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= screen_height:
			self.rect.bottom = screen_height


class Ball(MainBlock):
	def __init__(self, path, x, y, speed_x, speed_y, racket):
		super().__init__(path, x, y)
		self.speed_x = speed_x * random.choice((-1,1))
		self.speed_y = speed_y * random.choice((-1,1))
		self.racket = racket
		self.movement = False
		self.score_time = 0

	def update(self):
		if self.movement:
			self.rect.x += self.speed_x
			self.rect.y += self.speed_y
			self.collision()
		else:
			self.counter_reset()

	def collision(self):
		if self.rect.top <= 0 or self.rect.bottom >= screen_height:
			pygame.mixer.Sound.play(hit_sound)
			self.speed_y *= -1

		if pygame.sprite.spritecollide(self, self.racket, False):
			pygame.mixer.Sound.play(hit_sound)
			racket_collision = pygame.sprite.spritecollide(self, self.racket, False)[0].rect
			if abs(self.rect.right - racket_collision.left) < 10 and self.speed_x > 0:
				self.speed_x *= -1
			if abs(self.rect.left - racket_collision.right) < 10 and self.speed_x < 0:
				self.speed_x *= -1
			if abs(self.rect.top - racket_collision.bottom) < 10 and self.speed_y < 0:
				self.rect.top = racket_collision.bottom
				self.speed_y *= -1
			if abs(self.rect.bottom - racket_collision.top) < 10 and self.speed_y > 0:
				self.rect.bottom = racket_collision.top
				self.speed_y *= -1

	def ball_reset(self):
		self.movement = False
		self.speed_x *= random.choice((-1,1))
		self.speed_y *= random.choice((-1,1))
		self.score_time = pygame.time.get_ticks()
		self.rect.center = (screen_width / 2,screen_height / 2)
		pygame.mixer.Sound.play(score_sound)

	def counter_reset(self):
		current_time = pygame.time.get_ticks()
		count_number = 3

		if current_time - self.score_time <= 600:
			count_number = 3
			
		if 600 < current_time - self.score_time <= 1200:
			count_number = 2
			
		if 1200 < current_time - self.score_time <= 1800:
			count_number = 1
			
		if current_time - self.score_time >= 1800:
			self.movement = True

		pygame.mixer.Sound.play(timer_sound)
		time_counter = counter_font.render(str(count_number), True, my_color)
		time_counter_rect = time_counter.get_rect(center = (screen_width / 2 - 10, screen_height / 2 + 20))
		screen.blit(time_counter, time_counter_rect)


class Game:
	def __init__(self,ball_group, racket_group):
		self.player_score = 0
		self.computer_player_score = 0
		self.ball_group = ball_group
		self.racket_group = racket_group

	def start_game(self):

		self.racket_group.draw(screen)
		self.ball_group.draw(screen)

		self.racket_group.update(self.ball_group)
		self.ball_group.update()
		self.ball_reset()
		self.draw_score()
	
	def ball_reset(self):
		if self.ball_group.sprite.rect.right >= screen_width:
			self.computer_player_score += 1
			self.ball_group.sprite.ball_reset()
		if self.ball_group.sprite.rect.left <= 0:
			self.player_score += 1
			self.ball_group.sprite.ball_reset()
		if self.computer_player_score == 5:
			screen.blit(end_lose, go_rect)
			pygame.display.flip()
			clock.tick(1)
		elif self.player_score == 5:
			screen.blit(end_win, go_rect)
			pygame.display.flip()
			clock.tick(1)

	def draw_score(self):
		player_score = basic_font.render(str(self.player_score), True, my_color)
		computer_player_score = basic_font.render(str(self.computer_player_score), True, my_color)

		player_score_rect = player_score.get_rect(midleft = (screen_width / 2 + 40, 60))
		computer_player_score_rect = computer_player_score.get_rect(midright = (screen_width / 2 - 40, 60))

		screen.blit(player_score, player_score_rect)
		screen.blit(computer_player_score, computer_player_score_rect)
		

class Screen():
	def __init__(self):
		self.stanje = 'intro'

	def intro_screen(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				self.stanje = 'main_game'

		screen.blit(intro_pic,(0,0))

		pygame.display.flip()

	def game_screen(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					player.movement -= player.speed
				if event.key == pygame.K_DOWN:
					player.movement += player.speed
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					player.movement += player.speed
				if event.key == pygame.K_DOWN:
					player.movement -= player.speed

		
		screen.blit(image,(0,0))
		pygame.draw.rect(screen, 'white', middle_line)

		game.start_game()
		pygame.display.flip()
		
	def manager_state(self):
		if self.stanje == 'intro':
			self.intro_screen()
		if self.stanje == 'main_game':
			self.game_screen()


# BloddyPong general setup
pygame.init()
clock = pygame.time.Clock()

game_state = Screen()

# Main window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Welcome to BloodyPong!')
image = pygame.image.load('images\\scary_image.jpg')
intro_pic = pygame.image.load('images\\intro_image.png')
middle_line = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)

# Fonts
basic_font = pygame.font.Font('fonts\\bloody.ttf', 80)
counter_font = pygame.font.Font('fonts\\bloody.ttf', 450)

# Sounds
hit_sound = pygame.mixer.Sound('sounds\\tennis.mp3')
timer_sound = pygame.mixer.Sound('sounds\\mac.wav')
score_sound = pygame.mixer.Sound('sounds\\zombie.wav')
game_music = pygame.mixer.Sound('sounds\\scary_music.mp3')

# Players
player = Player('images\\racket.png', screen_width - 20, screen_height / 2,5)
computer_player = ComputerPlayer('images\\racket.png', 20, screen_width / 2,5)

racket_group = pygame.sprite.Group()
racket_group.add(player)
racket_group.add(computer_player)

ball = Ball('images\\ball.png', screen_width / 2, screen_height / 2, 4, 4, racket_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game  = Game(ball_sprite, racket_group)

end_lose = pygame.image.load('images\\go_image.png').convert_alpha()
go_rect = end_lose.get_rect(center = (400,300))
end_win = pygame.image.load('images\\win_image.png').convert_alpha()
go_rect = end_win.get_rect(center = (400,300))

# Colors
bg_color = pygame.Color('#1E1D1D')
my_color = (150, 0, 0)

# Main loop
while True:
	game_state.manager_state()
	clock.tick(140)
