import pygame
from sys import exit
import random
import os

import sys

pygame.init()

f = open('game_stats.txt','r')
high_score=f.read()
f.close


poyo = pygame.mixer.Sound('gamefiles/sound/poyo.wav')
class Bulet(pygame.sprite.Sprite):
	def __init__(self,pos_x,pos_y,bullet_speed):
		super().__init__()
		self.bullet_speed=bullet_speed
		self.pos_x=pos_x
		self.pos_y=pos_y
		self.enemy_sprite = pygame.image.load('gamefiles/graphics/bullet/bullet.png').convert_alpha()
		self.image=self.enemy_sprite
		self.rect = self.image.get_rect(midbottom = (pos_x,pos_y))

	def update(self):
		self.image=self.enemy_sprite
		self.rect.x += self.bullet_speed
class Player(pygame.sprite.Sprite):
	def __init__(self,pos_y,pos_x,bullet_speed):
		super().__init__()
		player_walk_1 = pygame.image.load('gamefiles/graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('gamefiles/graphics/player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.bullet_speed=bullet_speed
		self.player_index = 0
		self.pos_y=pos_y
		self.pos_x=pos_x
		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (self.pos_x,self.pos_y))
		self.speed=3
		self.reload_speed=1 
		self.shoot_delay=0
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
		elif keys[pygame.K_q ] and self.shoot_delay==0:
			bullets.add(Bulet(self.pos_x,self.pos_y,self.bullet_speed))
		
			self.shoot_delay=100
			pygame.mixer.Sound.play(poyo)

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
		
		if self.shoot_delay>0:
			self.shoot_delay-=self.reload_speed
		
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.enemy_sprite = pygame.image.load('gamefiles/graphics/enemy/enemy.png').convert_alpha()
		self.image=self.enemy_sprite
		self.rect = self.image.get_rect(midbottom = (random.randint(500,800),random.randint(50,300)))

	def update(self):
		self.image=self.enemy_sprite
		self.rect.x -= 1




screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()
test_font = pygame.font.Font('gamefiles/font/Pixeltype.ttf', 50)
game_active = False
start_time = 0

#Groups
enemy=pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
bullets = pygame.sprite.Group()

player_obj=Player(200,200,2)
player.add(player_obj)
enemy.add(Enemy())

sky_surface = pygame.image.load('gamefiles/graphics/Sky.png').convert()

# Intro screen
player_stand = pygame.image.load('gamefiles/graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

score=0


font = pygame.font.Font('freesansbold.ttf',20)
text = font.render(f"Score: {str(score)}", True, (161, 3, 3))
textRect = text.get_rect()
textRect.center = (150,60)

font2 = pygame.font.Font('freesansbold.ttf', 20)
text2 = font2.render(f"High score: {str(high_score)}", True, (64, 168, 50))
textRect2 = text2.get_rect()
textRect2.center = (275,60)
# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			if score>int(float(high_score)):
					f = open('game_stats.txt','w')
					f.write(str(score))
					print("new high score")
					f.close
			pygame.quit()
			exit()
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)

	if game_active:
		screen.blit(sky_surface,(0,0))
		screen.blit(text, textRect)
		screen.blit(text2, textRect2)
		#print(player_obj.pos_x)
		spawn_chance_inverted=200
		x=random.randint(1,spawn_chance_inverted)
		for e in enemy:
			enemy_rect = e.rect
			player_rect=player_obj.rect
			colide=pygame.Rect.colliderect(player_rect,enemy_rect)
			if colide:
				enemy=[]
				if score>int(float(high_score)):
					f = open('game_stats.txt','w')
					f.write(str(score))
					print("new high score")
					f.close
				sys.exit()
				game_active=False
		for b in bullets:
			bullet_rect=b.rect
			for e in enemy:
				enemy_rect=e.rect
				colide=pygame.Rect.colliderect(bullet_rect,enemy_rect)
				if colide:
					score+=1
					e.kill()
					b.kill()
		if x==1:
			enemy.add(Enemy())

		text = font.render(f"Score: {str(score)}", True, (161, 3, 3))
		
		player.draw(screen)
		player.update()
		enemy.draw(screen)
		enemy.update()
		bullets.draw(screen)
		bullets.update()
		if player_obj.shoot_delay<20:color=(64, 168, 50)
		elif player_obj.shoot_delay<40:color=(214, 240, 113)
		elif player_obj.shoot_delay<60:color=(229, 240, 113)
		elif player_obj.shoot_delay<80:color=(161, 85, 3)
		else:color=(161, 3, 3)
		pygame.draw.rect(screen, color, pygame.Rect(30, 30, 60, 60))

		
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)

	pygame.display.update()
	clock.tick(60)