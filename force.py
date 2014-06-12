import math
import pygame

force_color = {
	"attractive" : (255, 0, 0),
	"repulsive" : (0, 255, 128),
	"total repulsive" : (0, 128, 0),
	"final" : (0, 0, 255),
}

class Force:
	def __init__(self, owner, direction, magnitude, catalog, target_id):
		self.direction = direction
		self.magnitude = magnitude
		self.catalog = catalog
		self.target_id = target_id

		self.start_pos = owner.GetPos()
		rate = 10 * magnitude / math.hypot(direction[0], direction[1])
		self.end_pos = (
				self.start_pos[0] + direction[0] * rate,
				self.start_pos[1] + direction[1] * rate,
		)

	def GetRect(self):
		return pygame.Rect(
				min(self.start_pos[0], self.end_pos[0]),
				min(self.start_pos[1], self.end_pos[1]),
				abs(self.start_pos[0] - self.end_pos[0]),
				abs(self.start_pos[1] - self.end_pos[1]))

	def Draw(self, board):
		board.DrawArrow(
				force_color[self.catalog],
				self.start_pos,
				self.end_pos)

