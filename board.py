
import pygame

COLOR_COORD_LINE = (200, 200, 200)  # gray
COLOR_COORD_LINE_DARK = (150, 150, 150)  # dark gray

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

		self.font = pygame.font.Font('freesansbold.ttf', 10)

	def AdjustScaleAndOffset(self, entities):
		if len(entities) > 0:
			top, bottom, left, right = None, None, None, None
			for ent in entities:
				if left is None or ent.pos[0] - ent.radius < left:
					left = ent.pos[0] - ent.radius
				if right is None or ent.pos[0] + ent.radius > right:
					right = ent.pos[0] + ent.radius
				if top is None or ent.pos[1] - ent.radius < top:
					top = ent.pos[1] - ent.radius
				if bottom is None or ent.pos[1] + ent.radius > bottom:
					bottom = ent.pos[1] + ent.radius

			vertical_scale =  self.width * 0.8 / (right - left)
			horizontal_scale = self.height * 0.8 / (bottom - top)
			self.scale = min(vertical_scale, horizontal_scale)
			self.offsetx = int((left + right - self.width / self.scale) / 2.0)
			self.offsetz = int((top + bottom - self.height / self.scale) / 2.0)

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
						"%.1f" % coord, True, (0, 0, 0))
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
						"%.1f" % coord, True, (0, 0, 0))
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

	def DrawCircle(self, color, pos, radius):
		display_pos = [
				self.left + int((pos[0] - self.offsetx) * self.scale),
				self.top + int(self.height - (pos[1] - self.offsetz) * self.scale),
		]
		pygame.draw.circle(
				self.surface,
				color,
				display_pos,
				int(radius * self.scale),
				0)