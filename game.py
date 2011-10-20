import pygame
import spyral
import random
import math

TICKS_PER_SECOND = 6
HEIGHT = 600
WIDTH = 800
BLOCK_SIZE = 32

operators = ["+","-","*","/"]
directions = {}
directions['up'] = 0
directions['down'] = 1
directions['right'] = 2
directions['left'] = 3

# locations are in terms of the discrete grid, with indexing beginning at 0. top-left is origin.
# pixel_x is grid_x*BLOCK_SIZE + BLOCK_SIZE/2, which corresponds to the centers of sprites

fonts = {}
geom = {}
images = {}
colors = {}
strings = {}

# snake is a list of SnakeNodes, head is the location of the head
def openSpace(foodItems,snake,head):
	taken = True
	while taken:
		taken = False
		loc = (random.randrange(0,25),random.randrange(0,18))
		for item in foodItems:
			if item.location == loc:
				taken = True
		for s in snake:
			if s.location == loc:
				taken = True
		if head == loc:
			taken = True
	return loc

class Score(spyral.sprite.Sprite):
	def __init__(self):
		spyral.sprite.Sprite.__init__(self)
		self.val = 0
		self.render()
		
	def render(self):
		self.image = fonts['score'].render("SCORE: %d" % self.val,True,colors['score'])
		self.rect.midtop = (geom['scorex'],geom['text_height'])

# self.express is a list of strings, each of which is a number or operator
class Expression(spyral.sprite.Sprite):
	def __init__(self):
		spyral.sprite.Sprite.__init__(self)
		self.express = []
		self.render()
		
	def render(self):
		self.image = fonts['Expression'].render( " ".join(self.express),True,colors['expression'])
		self.rect.midtop = (geom['expressionx'],geom['text_height'])
		
class Goal(spyral.sprite.Sprite):
	def __init__(self):
		spyral.sprite.Sprite.__init__(self)
		self.val = random.randrange(0,20,1)
		self.render()
	
	def render(self):
		self.image = fonts['goal'].render("Goal: %d" % self.val,True,colors['goal'])
		self.rect.midtop = (geom['goalx'],geom['text_height'])

class Length(spyral.sprite.Sprite):
	def __init__(self):
		spyral.sprite.Sprite.__init__(self)
		self.val = 0
		self.render()
		
	def render(self):
		self.image = fonts['length'].render("Length: %d" % self.val,True,colors['length'])
		self.rect.midtop = (geom['lengthx'],geom['text_height'])
		
class Operator(spyral.sprite.Sprite):
	def __init__(self,foodItems,snake,head):
		spyral.sprite.Sprite.__init__(self)
		self.location = openSpace(foodItems,snake,head)
		self.val = operators[random.randrange(0,4,1)]
		self.image = fonts['operator'].render(self.val,True,colors['operator'])
		self.rect.center = (self.location[0]*BLOCK_SIZE + BLOCK_SIZE/2,self.location[1]*BLOCK_SIZE + BLOCK_SIZE/2)

class Number(spyral.sprite.Sprite):
	def __init__(self,foodItems,snake,head):
		spyral.sprite.Sprite.__init__(self)
		self.location = openSpace(foodItems,snake,head)
		self.val = random.randrange(0,15,1)
		self.image = fonts['number'].render("%d" % self.val,True,colors['number'])
		self.rect.center = (self.location[0]*BLOCK_SIZE + BLOCK_SIZE/2,self.location[1]*BLOCK_SIZE + BLOCK_SIZE/2)

class SnakeNode(spyral.sprite.Sprite):
	def __init__(self,val,dir,loc):
		sypral.sprite.Sprite.__init__(self)
		self.value = val
		self.direction = dir
		self.location = loc
		self.render()
	
	def render(self):
		#for moving sprites in this game, the image changes every time the direction does
		self.image = fonts['node'].render(str(self.value),True,colors['node'])
		self.rect.center = (self.location[0]*BLOCK_SIZE + BLOCK_SIZE/2,self.location[1]*BLOCK_SIZE + BLOCK_SIZE/2)
		
class Snake(spyral.sprite.Sprite):
	def __init__(self):
		spyral.sprite.Sprite.__init__(self)
		self.image = images['head']
		self.location = (11,8)
		self.nodes = []
		self.clearing = False
		self.collapsing = False
		self.length = 0
		self.direction = directions['up']
		self.render()
	
	def render(self):
		#render the nodes
	
		#render the head
		self.rect.center = (self.location[0]*BLOCK_SIZE + BLOCK_SIZE/2,self.location[1]*BLOCK_SIZE + BLOCK_SIZE/2)
		
class Game(spyral.scene.Scene):
	def __init__(self):
		spyral.scene.Scene.__init__(self)
		self.camera = spyral.director.get_camera()
		self.group = spyral.sprite.Group(self.camera)
		background = spyral.util.new_surface((WIDTH,HEIGHT))
		background.fill(colors['background'])
		self.camera.set_background(background)
		self.goal = 15
		self.snake = Snake()
		self.foodItems = [Operator([],[],self.snake.location)]
		for n in range(0,3):
			self.foodItems.append(Number(self.foodItems,[],self.snake.location))
		for i in self.foodItems:
			self.group.add(i,)
		self.group.add(self.snake)
		self.moving = False
	
	def render(self):
		self.group.draw()
		self.camera.draw()
	
	def update(self,tick):

		for event in pygame.event.get([pygame.KEYUP, pygame.KEYDOWN]):
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					spyral.director.pop()
				if event.key == pygame.K_UP:
					self.moving = True
					self.snake.direction = directions['up']
				elif event.key == pygame.K_DOWN:
					self.moving = True
					self.snake.direction = directions['down']
				elif event.key == pygame.K_RIGHT:
					self.moving = True
					self.snake.direction = directions['right']
				elif event.key == pygame.K_LEFT:
					self.moving = True
					self.snake.direction = directions['left']
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_UP and self.snake.direction == directions['up']:
					self.moving = False
				elif event.key == pygame.K_DOWN and self.snake.direction == directions['down']:
					self.moving = False
				elif event.key == pygame.K_RIGHT and self.snake.direction == directions['right']:
					self.moving = False
				elif event.key == pygame.K_LEFT and self.snake.direction == directions['left']:
					self.moving = False
		pygame.event.clear()
		
		
		if self.moving == True:
		
			#test if we've hit a wall or self
		
			#starting at the end of the snake, move the nodes. So, the direction and location of
			#the second-to-last node become those of the last node and so on up the chain, until
			#the first node goes to where the head is
			
			
			#move the head
			if self.snake.direction == directions['up']:
				self.snake.location = (self.snake.location[0],self.snake.location[1]-1)
			elif self.snake.direction == directions['down']:
				self.snake.location = (self.snake.location[0],self.snake.location[1]+1)
			elif self.snake.direction == directions['right']:
				self.snake.location = (self.snake.location[0]+1,self.snake.location[1])
			elif self.snake.direction == directions['left']:
				self.snake.location = (self.snake.location[0]-1,self.snake.location[1])
			
			#test for target
			
		self.snake.render()
		self.group.update()

		
if __name__ == "__main__":
	spyral.init()
	
	colors['background'] = (0, 0, 0)
	colors['head'] = (255,255,255)
	colors['node'] = (255,255,255)
	colors['number'] = (255,255,255)
	colors['operator'] = (255,255,255)
	
	
	images['head'] = spyral.util.new_surface(BLOCK_SIZE,BLOCK_SIZE)
	images['head'].fill(colors['head'])
	
	fonts['node'] = pygame.font.SysFont(None,BLOCK_SIZE)
	fonts['number'] = pygame.font.SysFont(None,BLOCK_SIZE)
	fonts['operator'] = pygame.font.SysFont(None,BLOCK_SIZE)
	
	spyral.director.init((WIDTH,HEIGHT), ticks_per_second=TICKS_PER_SECOND)
	spyral.director.push(Game())
	spyral.director.clock.use_wait = False
	pygame.event.set_allowed(None)
	pygame.event.set_allowed(pygame.KEYDOWN)
	pygame.event.set_allowed(pygame.KEYUP)
	spyral.director.run()