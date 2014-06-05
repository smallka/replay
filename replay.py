import sys
import pygame
from pygame.locals import *

import board
import entity
import command

FPS = 30
WIN_WIDTH = 900
WIN_HEIGHT = 660

COLOR_BG = (255, 255, 255)  # white

def main():
	pygame.init()
	pygame.display.set_caption('AI Play')

	fpsClock = pygame.time.Clock()

	main_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	main_board = board.Board(main_surface, 20, 60, 800, 600)

	# test
	cmd_queue = []
	cmd_queue.append(command.CmdAddEntity(1, entity.ROLE_ME, (100, 200), 120))
	cmd_queue.append(command.CmdAddEntity(2, entity.ROLE_TARGET, (600, 400), 200))

	while True:
		main_surface.fill(COLOR_BG)

		entities = entity.GetAllEntities()

		main_board.AdjustScaleAndOffset(entities)

		main_board.DrawCoordSystem()

		for ent in entities:
			ent.Draw(main_board)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYUP:
				if event.key == K_ESCAPE:
					for undo in reversed(cmd_queue):
						undo()
					cmd_queue = []

		pygame.display.update()
		fpsClock.tick(FPS)

if __name__ == '__main__':
	main()