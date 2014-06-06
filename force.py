import math
import pygame

class Force:
	def __init__(self, owner, direction, magnitude, desc, target_id):
		self.direction = direction
		self.magnitude = magnitude
		self.desc = desc
		self.target_id = target_id

		self.start_pos = owner.GetPos()
		rate = magnitude / math.hypot(direction[0], direction[1])
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
		board.DrawLine(
				(255, 0, 255),
				self.start_pos,
				self.end_pos)

