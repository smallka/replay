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
	pygame.display.set_caption('Replay')

	fpsClock = pygame.time.Clock()

	main_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	main_board = board.Board(main_surface, 60, 20, 800, 600)

	# test
	cmd_queue = []
	cmd_queue.append(command.CmdAddEntity(1, (100, 200), 120))
	cmd_queue.append(command.CmdAddEntity(2, (100, 400), 150))
	cmd_queue.append(command.CmdAddEntity(3, (500, 400), 200))
	cmd_queue.append(command.CmdAddForce(1, (1, 1.732), 200, "test", None))
	cmd_queue.append(command.CmdSetPath(1, ((100, 200), (200, 250), (600, 400))))
	cmd_queue.append(command.CmdSetTargetId(1, 3))
	cmd_queue.append(command.CmdAddForce(2, (1, -1.732), 200, "test", None))
	cmd_queue.append(command.CmdSetTargetId(2, 3))
	entity.SetMe(entity.GetEntity(1))

	while True:
		main_surface.fill(COLOR_BG)

		entities = entity.GetAllEntities()

		main_board.AdjustScaleAndOffset(entities)

		main_board.DrawCoordSystem()

		for ent in reversed(entities):
			ent.Draw(main_board)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				pos = main_board.TransformReverse(pos)
				ent = entity.GetEntityAtPos(pos)
				if ent is not None:
					entity.SetMe(ent)

			elif event.type == KEYUP:
				if event.key == K_p:
					if len(cmd_queue) > 0:
						cmd_queue.pop()()

		pygame.display.update()
		fpsClock.tick(FPS)

if __name__ == '__main__':
	main()