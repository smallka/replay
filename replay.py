import sys
import pygame
from pygame.locals import *

from pgu import gui

import board
import entity
import processor

FPS = 30
BOARD_LEFT = 60
BOARD_TOP = 200
BOARD_WIDTH = 800
BOARD_HEIGHT = 400
WIN_WIDTH = BOARD_LEFT + BOARD_WIDTH + 20
WIN_HEIGHT = BOARD_TOP + BOARD_HEIGHT + 40

COLOR_BG = (255, 255, 255)  # white

def main():
	pygame.init()
	pygame.display.set_caption("Replay")

	clock = pygame.time.Clock()

	screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), SWSURFACE)
	main_board = board.Board(screen, BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT)

	app = gui.App()
	container = gui.Container(align=-1, valign=-1)
	table = gui.Table()
	box = gui.ScrollArea(table, BOARD_WIDTH, BOARD_TOP)
	container.add(box, BOARD_LEFT, 0)
	app.init(container)

	proc = processor.Processor("input.log")

	while True:
		need_scroll_down = False
		entities_count = len(entity.GetAllEntities())

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == KEYUP:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()

				elif event.key == K_j:
					# next cmd
					line = proc.Next()
					if line is not None:
						table.tr()
						table.td(gui.Label(line), align=-1)
						need_scroll_down = True

				elif event.key == K_k:
					# undo prev cmd
					if proc.Prev():
						table.remove_row(table.getRows() - 1)

				elif event.key == K_m:
					# next cmds until me move
					me = entity.GetMe()
					if me is not None:
						old_pos = me.pos
						while True:
							line = proc.Next()
							if line is None:
								break

							table.tr()
							table.td(gui.Label(line), align=-1)
							need_scroll_down = True

							if me.pos != old_pos:
								break

				elif event.key == K_a:
					main_board.AdjustScaleAndOffset(entity.GetAllEntities())

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

		if len(entities) != entities_count:
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

if __name__ == "__main__":
	main()