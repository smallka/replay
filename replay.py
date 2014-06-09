import sys
import pygame
from pygame.locals import *

from pgu import gui

import board
import entity
import command

FPS = 30
BOARD_LEFT = 60
BOARD_TOP = 200
BOARD_WIDTH = 800
BOARD_HEIGHT = 400
WIN_WIDTH = BOARD_LEFT + BOARD_WIDTH + 20
WIN_HEIGHT = BOARD_TOP + BOARD_HEIGHT + 20

COLOR_BG = (255, 255, 255)  # white

def main():
	pygame.init()
	pygame.display.set_caption('Replay')

	clock = pygame.time.Clock()

	screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), SWSURFACE)
	main_board = board.Board(screen, BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT)

	app = gui.App()
	container = gui.Container(align=-1,valign=-1)
	table = gui.Table()
	box = gui.ScrollArea(table, BOARD_WIDTH, BOARD_TOP - 20)
	container.add(box, BOARD_LEFT, 0)
	app.init(container)

	# test
	cmd_queue = []
	cmd_queue.append(command.CmdAddEntity(1, (100, 200), 120))
	cmd_queue.append(command.CmdAddEntity(2, (100, 400), 150))
	cmd_queue.append(command.CmdAddEntity(3, (500, 400), 200))
	cmd_queue.append(command.CmdAddForce(1, (1, 1.732), 200, "test", None))
	cmd_queue.append(command.CmdSetPath(1, ((100, 200), (200, 250), (500, 400))))
	cmd_queue.append(command.CmdSetTargetId(1, 3))
	cmd_queue.append(command.CmdAddForce(2, (1, -1.732), 200, "test", None))
	cmd_queue.append(command.CmdSetTargetId(2, 3))
	entity.SetMe(entity.GetEntity(1))

	while True:
		need_scroll_down = False

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == KEYUP:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				elif event.key == K_p:
					if len(cmd_queue) > 0:
						cmd_queue.pop()()
				elif event.key == K_j:
					# test
					import random
					table.tr()
					newline = gui.Label("%f" % random.random())
					table.td(newline)
					need_scroll_down = True

			elif event.type == MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				pos = main_board.TransformReverse(pos)
				ent = entity.GetEntityAtPos(pos)
				if ent is not None:
					entity.SetMe(ent)

				app.event(event)

			else:
				app.event(event)

		screen.fill(COLOR_BG)

		entities = entity.GetAllEntities()

		main_board.AdjustScaleAndOffset(entities)

		main_board.DrawCoordSystem()

		for ent in reversed(entities):
			ent.Draw(main_board)

		app.paint()
		pygame.display.flip()

		# bug: only work in next frame
		if need_scroll_down:
			box.set_vertical_scroll(65536)

		clock.tick(FPS)

if __name__ == '__main__':
	main()