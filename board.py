
import math
import pygame

import pgu
import pgu.text

COLOR_COORD_LINE = (200, 200, 200)  # gray
COLOR_COORD_LINE_DARK = (150, 150, 150)  # dark gray

COLOR_COORD_NUM = (0, 0, 0)

COLOR_INFO_FG = (0, 0, 0)
COLOR_INFO_BG = (0, 255, 0)

ARROW_LENGTH = 10
ARROW_ANGLE = math.pi / 6

class Board:
	def __init__(self, surface, left, top, width, height):
		self.surface = surface

		# board on windows
		self.left = left
		self.top = top
		self.width = width
		self.height = height

		self.scale = 1.0
		self.offsetx = 0.0
		self.offsetz = 0.0

		self.font = pygame.font.Font("freesansbold.ttf", 10)

	def AdjustScaleAndOffset(self, entities):
		rect = None
		for ent in entities:
			if rect is None:
				rect = ent.GetRect()
			else:
				rect.union_ip(ent.GetRect())

		if rect is None:
			return

		vertical_scale =  self.width * 0.8 / rect.width
		horizontal_scale = self.height * 0.8 / rect.height
		self.scale = min(vertical_scale, horizontal_scale)
		self.offsetx = int(rect.centerx - self.width / self.scale / 2.0)
		self.offsetz = int(rect.centery - self.height / self.scale / 2.0)

	def DrawCoordSystem(self):
		# vertical lines
		vertical_count = 40
		vertical_step = self.width / vertical_count
		x = self.left

		for i in xrange(vertical_count + 1):
			if i % 5 == 0:
				color = COLOR_COORD_LINE_DARK

				coord = self.offsetx + \
						i * vertical_step / self.scale 
				coord_surface = self.font.render(
						"%.1f" % coord, True, COLOR_COORD_NUM)
				coord_rect = coord_surface.get_rect()
				coord_rect.midtop = (
						self.left + i * vertical_step,
						self.top + self.height + 5)
				self.surface.blit(coord_surface, coord_rect)
			else:
				color = COLOR_COORD_LINE
			pygame.draw.line(
					self.surface,
					color,
					(x, self.top),
					(x, self.top + self.height))
			x += vertical_step

		# horizontal lines
		horizontal_count = self.height * vertical_count / self.width
		horizontal_step = self.height / horizontal_count
		y = self.top
		for i in xrange(horizontal_count + 1):
			if i % 5 == 0:
				color = COLOR_COORD_LINE_DARK

				coord = self.offsetz + \
						(horizontal_count - i) * horizontal_step / self.scale 
				coord_surface = self.font.render(
						"%.1f" % coord, True, COLOR_COORD_NUM)
				coord_rect = coord_surface.get_rect()
				coord_rect.midright = (
						self.left,
						self.top + i * horizontal_step)
				self.surface.blit(coord_surface, coord_rect)
			else:
				color = COLOR_COORD_LINE
			pygame.draw.line(
					self.surface,
					color,
					(self.left, y),
					(self.left + self.width, y))
			y += horizontal_step

	def _Transform(self, pos):
		return (
				self.left + int((pos[0] - self.offsetx) * self.scale),
				self.top + int(self.height - (pos[1] - self.offsetz) * self.scale),
		)

	def TransformReverse(self, pos):
		return (
				(pos[0] - self.left) / self.scale + self.offsetx,
				(self.height - (pos[1] - self.top)) / self.scale + self.offsetz,
		)

	def DrawCircle(self, color, pos, radius):
		pygame.draw.circle(
				self.surface,
				color,
				self._Transform(pos),
				int(radius * self.scale),
				0)

	def DrawArrow(self, color, start_pos, end_pos):	
		start = self._Transform(start_pos)
		end = self._Transform(end_pos)
		pygame.draw.aaline(self.surface, color, start, end)

		angle = math.atan2(start[1] - end[1], start[0] - end[0])
		left = (
				end[0] + ARROW_LENGTH * math.cos(angle - ARROW_ANGLE),
				end[1] + ARROW_LENGTH * math.sin(angle - ARROW_ANGLE))
		pygame.draw.aaline(self.surface, color, end, left)
		right = (
				end[0] + ARROW_LENGTH * math.cos(angle + ARROW_ANGLE),
				end[1] + ARROW_LENGTH * math.sin(angle + ARROW_ANGLE))
		pygame.draw.aaline(self.surface, color, end, right)

	def DrawPath(self, color, pointlist):	
		pygame.draw.lines(
				self.surface,
				color,
				False,
				[ self._Transform(pos) for pos in pointlist ],
				10)

	def DrawInfoText(self, info):
		surface = self.font.render(info, True, COLOR_INFO_FG, COLOR_INFO_BG)
		rect = surface.get_rect()
		rect.midtop = (self.left + self.width / 2, self.top + self.height + 20)
		self.surface.blit(surface, rect)
