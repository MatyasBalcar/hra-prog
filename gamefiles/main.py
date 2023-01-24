import pygame
from sys import exit
import random
class Player(pygame.sprite.Sprite):
	def __init__(self,pos_y,pos_x):
		super().__init__()
		player_walk_1 = pygame.image.load('gamefiles/graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('gamefiles/graphics/player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.pos_y=pos_y
		self.pos_x=pos_x
		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.speed=3

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w] :
			self.pos_y-=self.speed

		elif keys[pygame.K_s] :
			self.pos_y+=self.speed

		elif keys[pygame.K_a] :
			self.pos_x-=self.speed

		elif keys[pygame.K_d] :
			self.pos_x+=self.speed

	def position_update(self):
		self.rect.center=[self.pos_x,self.pos_y]
	def animation_state(self):
		self.player_index += 0.1
		if self.player_index >= len(self.player_walk):self.player_index = 0
		self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.position_update()
		self.animation_state()

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.enemy_sprite = pygame.image.load('gamefiles/graphics/enemy/enemy.png').convert_alpha()
		self.image=self.enemy_sprite
		self.rect = self.image.get_rect(midbottom = (random.randint(500,800),random.randint(0,350)))



	def update(self):
		self.image=self.enemy_sprite
		self.rect.x -= 1

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()
test_font = pygame.font.Font('gamefiles/font/Pixeltype.ttf', 50)
game_active = False
start_time = 0

#Groups
enemy=pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
player_obj=Player(200,200)
player.add(player_obj)
enemy.add(Enemy())

sky_surface = pygame.image.load('gamefiles/graphics/Sky.png').convert()

# Intro screen
player_stand = pygame.image.load('gamefiles/graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))



# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)

	if game_active:
		screen.blit(sky_surface,(0,0))

		x=random.randint(1,300)

		if x==1:
			enemy.add(Enemy())


		player.draw(screen)
		player.update()
		enemy.draw(screen)
		enemy.update()



		
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)

	pygame.display.update()
	clock.tick(60)