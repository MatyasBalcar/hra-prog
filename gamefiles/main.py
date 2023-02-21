import pygame
from sys import exit
import random
import sys
import math

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
		self.bullet_gfx_1 = pygame.image.load('gamefiles\graphics\Bullet\Bullet1.png').convert_alpha()#!zmen to na dobrou path
		self.bullet_gfx_2 = pygame.image.load('gamefiles\graphics\Bullet\Bullet2.png').convert_alpha()#!zmen to na dobrou path
		self.bullet_gfx_3 = pygame.image.load('gamefiles\graphics\Bullet\Bullet3.png').convert_alpha()#!zmen to na dobrou path
		self.image=self.bullet_gfx_1
		self.animation_count=0
		self.rect = self.image.get_rect(midbottom = (pos_x,pos_y))
	def animation(self):
		sprites=[self.bullet_gfx_1,self.bullet_gfx_2,self.bullet_gfx_3]
		if math.floor(self.animation_count)==3:
			self.animation_count=0
		else:self.animation_count+=0.1

		if self.animation_count>=0 and self.animation_count<=1:
			self.image=sprites[0]
		elif self.animation_count>1 and self.animation_count<=2:
			self.image=sprites[1]
		elif self.animation_count>2 and self.animation_count<=3:
			self.image=sprites[2]
	def update(self):
		self.animation()
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
		self.player_health=3
		self.healthpot_timer=0
		self.hasnuke=False
		self.health_delay=500
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
			#pygame.mixer.Sound.play(poyo)
		elif keys[pygame.K_e] and self.hasnuke:
			enemy.empty()
			self.hasnuke=False
			nuke.empty()
		elif keys[pygame.K_f] and self.healthpot_timer==0 and self.player_health<3:
			self.player_health+=1
			if self.player_health==1:
				lifes.add(Lifepoint(420,75))
			elif self.player_health==2:
				lifes.add(Lifepoint(450,75))
			elif self.player_health==3:
				lifes.add(Lifepoint(480,75))
			self.healthpot_timer+=self.health_delay
			for h in health_pot:
				h.kill()
			

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
		if self.healthpot_timer>0:
			self.healthpot_timer-=1
		if self.healthpot_timer==0 and len(health_pot)==0:
			health_pot.add(healt_pot_hud(600,75))
		
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.enemy_sprite = pygame.image.load('gamefiles/graphics/enemy/enemy.png').convert_alpha()
		self.image=self.enemy_sprite
		self.rect = self.image.get_rect(midbottom = (random.randint(500,800),random.randint(50,300)))

	def update(self):
		self.image=self.enemy_sprite
		self.rect.x -= 1

class Nuke(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.nuke_png = pygame.image.load('gamefiles/graphics/nuke.png').convert_alpha()
		self.image=self.nuke_png
		self.rect = self.image.get_rect(midbottom = (random.randint(500,800),random.randint(50,300)))
		self.type="nuke"
	def update(self):
		self.image=self.nuke_png
		self.rect.x -= 1
class Lifepoint(pygame.sprite.Sprite):
	def __init__(self,pos_x,pos_y):
		super().__init__()
		self.health_point_sprite = pygame.image.load('gamefiles/graphics/zivot.png').convert_alpha()
		self.image=self.health_point_sprite
		self.pos_y=pos_y
		self.pos_x=pos_x
		self.rect = self.image.get_rect(midbottom = (self.pos_x,self.pos_y))

	def update(self):
		pass
class nuke_hud(pygame.sprite.Sprite):
	def __init__(self,pos_x,pos_y):
		super().__init__()
		self.health_point_sprite = pygame.image.load('gamefiles/graphics/nuke.png').convert_alpha()
		self.image=self.health_point_sprite
		self.pos_y=pos_y
		self.pos_x=pos_x
		self.rect = self.image.get_rect(midbottom = (self.pos_x,self.pos_y))

	def update(self):
		pass		
class health_pot_back(pygame.sprite.Sprite):
	def __init__(self,pos_x,pos_y):
		super().__init__()
		self.health_point_sprite = pygame.image.load('gamefiles\graphics\potion\okraj.png').convert_alpha()
		self.image=self.health_point_sprite
		self.pos_y=pos_y
		self.pos_x=pos_x
		self.rect = self.image.get_rect(midbottom = (self.pos_x,self.pos_y))

	def update(self):
		pass	
class health_bar_back(pygame.sprite.Sprite):
	def __init__(self,pos_x,pos_y):
		super().__init__()
		self.health_point_sprite = pygame.image.load('gamefiles\graphics\health_bar.png').convert_alpha()
		self.image=self.health_point_sprite
		self.pos_y=pos_y
		self.pos_x=pos_x
		self.rect = self.image.get_rect(midbottom = (self.pos_x,self.pos_y))

	def update(self):
		pass	
class healt_pot_hud(pygame.sprite.Sprite):
	def __init__(self,pos_x,pos_y):
		super().__init__()
		self.potion_gfx_1 = pygame.image.load('gamefiles\graphics\potion\potion1.png').convert_alpha()#!zmen to na dobrou path
		self.potion_gfx_2 = pygame.image.load('gamefiles\graphics\potion\potion2.png').convert_alpha()#!zmen to na dobrou path
		self.potion_gfx_3 = pygame.image.load('gamefiles\graphics\potion\potion3.png').convert_alpha()#!zmen to na dobrou path
		self.image=self.potion_gfx_1
		self.pos_y=pos_y
		self.animation_count=0
		self.pos_x=pos_x
		self.rect = self.image.get_rect(midbottom = (self.pos_x,self.pos_y))
	def animation(self):
		sprites=[self.potion_gfx_1,self.potion_gfx_2,self.potion_gfx_3]
		if math.floor(self.animation_count)==3:
			self.animation_count=0
		else:self.animation_count+=0.1

		if self.animation_count>=0 and self.animation_count<=1:
			self.image=sprites[0]
		elif self.animation_count>1 and self.animation_count<=2:
			self.image=sprites[1]
		elif self.animation_count>2 and self.animation_count<=3:
			self.image=sprites[2]
	def update(self):
		self.animation()

#stock code
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()
test_font = pygame.font.Font('gamefiles/font/Pixeltype.ttf', 50)
game_active = False
start_time = 0

#Groups
enemy=pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
health_pot=pygame.sprite.GroupSingle()
bullets = pygame.sprite.Group()
lifes = pygame.sprite.Group()
powerups=pygame.sprite.Group()
nuke=pygame.sprite.GroupSingle()
health_pot_back_group=pygame.sprite.GroupSingle()
health_bar=pygame.sprite.GroupSingle()
#adding to sprite groups for renders
powerups.add(Nuke())#!TEMP

health_pot_back_group.add(health_pot_back(600,75))
health_bar.add(health_bar_back(450,75))
health_pot_obj=healt_pot_hud(600,75)
health_pot.add(health_pot_obj)
lifes.add(Lifepoint(420,75))
lifes.add(Lifepoint(450,75))
lifes.add(Lifepoint(480,75))
player_obj=Player(200,200,2)
player.add(player_obj)
enemy.add(Enemy())
lifes_list=[]
for l in lifes:
	lifes_list.append(l)

#textura nebe
sky_surface = pygame.image.load('gamefiles/graphics/Sky.png').convert()

#! Intro screen (TODO) zmen na lepsi i s instrukcemi
player_stand = pygame.image.load('gamefiles/graphics/player/player_stand.png').convert_alpha()

player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

#skore
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

					f.close
			pygame.quit()
			exit()
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:
		screen.blit(sky_surface,(0,0))

		spawn_chance_inverted=5000
		x=random.randint(1,spawn_chance_inverted)
		for p in powerups:
			nuke_rect = p.rect
			player_rect=player_obj.rect
			colide=pygame.Rect.colliderect(player_rect,nuke_rect)
			if colide and player_obj.hasnuke==False:
				if p.type=="nuke":
					player_obj.hasnuke=True
					nuke.add(nuke_hud(550,75))
				p.kill()
			


		for e in enemy:
			
			enemy_rect = e.rect
			player_rect=player_obj.rect
			colide=pygame.Rect.colliderect(player_rect,enemy_rect)
			if enemy_rect.x<0:
				e.kill()
				player_obj.player_health-=1
				for l in lifes:
					l.kill()
				if player_obj.player_health==3:
					lifes.add(Lifepoint(420,75))
					lifes.add(Lifepoint(450,75))
					lifes.add(Lifepoint(480,75))
				elif player_obj.player_health==2:
					lifes.add(Lifepoint(420,75))
					lifes.add(Lifepoint(450,75))
				elif player_obj.player_health==1:
					lifes.add(Lifepoint(420,75))
			if colide:
				e.kill()
				player_obj.player_health-=1
				for l in lifes:
					l.kill()
				if player_obj.player_health==3:
					lifes.add(Lifepoint(420,75))
					lifes.add(Lifepoint(450,75))
					lifes.add(Lifepoint(480,75))
				elif player_obj.player_health==2:
					lifes.add(Lifepoint(420,75))
					lifes.add(Lifepoint(450,75))
				elif player_obj.player_health==1:
					lifes.add(Lifepoint(420,75))
				
				if score>int(float(high_score)):
					f = open('game_stats.txt','w')
					f.write(str(score))

					f.close
				if player_obj.player_health==0:

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
		if x>1 and x<50 and len(enemy)<=6:
			enemy.add(Enemy())
		elif x==spawn_chance_inverted:

			powerups.add(Nuke())
		text = font.render(f"Score: {str(score)}", True, (161, 3, 3))
		
		
		#GAME
		bullets.draw(screen)
		bullets.update()
		powerups.draw(screen)
		powerups.update()
		enemy.draw(screen)
		enemy.update()
		nuke.draw(screen)
		if player_obj.shoot_delay<20:color=(64, 168, 50)
		elif player_obj.shoot_delay<40:color=(214, 240, 113)
		elif player_obj.shoot_delay<60:color=(229, 240, 113)
		elif player_obj.shoot_delay<80:color=(161, 85, 3)
		else:color=(161, 3, 3)
		pygame.draw.circle(screen,color,(60,60),20)
		screen.blit(text, textRect)
		screen.blit(text2, textRect2)
		
		#HUD
		health_bar.draw(screen)
		health_pot_back_group.draw(screen)
		health_pot.draw(screen)
		health_pot.update()
		player.draw(screen)
		player.update()
		lifes.draw(screen)
		
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)

	pygame.display.update()
	clock.tick(60)