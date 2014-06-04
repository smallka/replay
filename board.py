
import pygame

COLOR_COORD_LINE = (200, 200, 200)  # gray

class Board:
	def __init__(self, surface, top, left, width, height):
		self.surface = surface

		# board on windows
		self.top = top
		self.left = left
		self.width = width
		self.height = height

		self.scale = 1.0
		self.offsetx = 0.0
		self.offsetz = 0.0

	# base on given rect
	def AdjustScaleAndOffset(self, top, bottom, left, right):
		vertical_scale =  self.width * 0.8 / (right - left)
		horizontal_scale = self.height * 0.8 / (bottom - top)
		self.scale = min(vertical_scale, horizontal_scale)
		self.offsetx = (left + right - self.width / self.scale) / 2.0
		self.offsetz = (top + bottom - self.height / self.scale) / 2.0

	def DrawCoordSystem(self):
		# vertical
		vertical_count = 40
		x = self.left
		for i in xrange(vertical_count + 1):
			pygame.draw.line(
					self.surface,
					COLOR_COORD_LINE,
					(x, self.top),
					(x, self.top + self.height))
			x += self.width / vertical_count

		# horizontal
		horizontal_count = self.height * vertical_count / self.width
		y = self.top
		for i in xrange(horizontal_count + 1):
			pygame.draw.line(
					self.surface,
					COLOR_COORD_LINE,
					(self.left, y),
					(self.left + self.width, y))
			y += self.height / horizontal_count

	def DrawCircle(self, color, pos, radius):
		real_pos = [
				int((pos[0] - self.offsetx) * self.scale),
				self.height - int((pos[1] - self.offsetz) * self.scale),
		]
		pygame.draw.circle(
				self.surface,
				color,
				real_pos,
				int(radius * self.scale),
				0)