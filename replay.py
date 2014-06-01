import sys
import pygame
from pygame.locals import *

import entity

FPS = 30
MAP_WIDTH = 800
MAP_HEIGHT = 600
XBORDER = 10
YBORDER = 20
WIN_WIDTH = MAP_WIDTH + XBORDER + 200
WIN_HEIGHT = MAP_HEIGHT + YBORDER + 10

COLOR_BG = (255, 255, 255)  # white
COLOR_COORD_LINE = (200, 200, 200)  # gray
COLOR_RANGE = (0, 0, 0)  # black

def DrawCoordLines(surface):
	# vertical
	vertical_count = 40
	x = XBORDER
	for i in xrange(vertical_count + 1):
		pygame.draw.line(
				surface,
				COLOR_COORD_LINE,
				(x, YBORDER),
				(x, YBORDER + MAP_HEIGHT))
		x += MAP_WIDTH / vertical_count

	# horizontal
	horizontal_count = MAP_HEIGHT * vertical_count / MAP_WIDTH
	y = YBORDER
	for i in xrange(horizontal_count + 1):
		pygame.draw.line(
				surface,
				COLOR_COORD_LINE,
				(XBORDER, y),
				(XBORDER + MAP_WIDTH, y))
		y += MAP_HEIGHT / horizontal_count


def main():
	pygame.init()
	pygame.display.set_caption('AI Play')

	fpsClock = pygame.time.Clock()

	display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

	entity.Entity(1, entity.ROLE_ME, (200, 100), 10)
	entity.Entity(2, entity.ROLE_TARGET, (500, 345), 20)
	entity.Entity(3, entity.ROLE_FRIEND, (400, 245), 20)

	while True:
		display_surface.fill(COLOR_BG)

		DrawCoordLines(display_surface)

		entity.DrawAllEntities(display_surface)

		for event in pygame.event.get():
			if event.type == QUIT \
					or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()

		pygame.display.update()
		fpsClock.tick(FPS)

if __name__ == '__main__':
	main()