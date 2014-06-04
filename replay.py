import sys
import pygame
from pygame.locals import *

import board
import entity

FPS = 30
WIN_WIDTH = 1000
WIN_HEIGHT = 700

COLOR_BG = (255, 255, 255)  # white

def main():
	pygame.init()
	pygame.display.set_caption('AI Play')

	fpsClock = pygame.time.Clock()

	main_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	main_board = board.Board(main_surface, 10, 20, 800, 600)

	# test
	me = entity.Entity(1, entity.ROLE_ME)
	me.pos = (100, 200)
	me.radius = 100
	target = entity.Entity(2, entity.ROLE_TARGET)
	target.pos = (600, 400)
	target.radius = 200
	entity.Entity(3, entity.ROLE_FRIEND)

	while True:
		main_surface.fill(COLOR_BG)

		main_board.DrawCoordSystem()

		entity.DrawAllEntities(main_board)

		for event in pygame.event.get():
			if event.type == QUIT \
					or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()

		pygame.display.update()
		fpsClock.tick(FPS)

if __name__ == '__main__':
	main()