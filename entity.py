import pygame

import force

ROLE_ME = "me"
ROLE_TARGET = "target"
ROLE_FRIEND = "friend"

_all_entities = {}

def GetEntity(guid):
	return _all_entities.get(guid)

def DelEntity(guid):
	if guid in _all_entities:
		del _all_entities[guid]

def GetAllEntities():
	return _all_entities.values()

COLOR4ROLE = {
	ROLE_ME : (0, 255, 255),
	ROLE_TARGET : (0, 0, 128),
	ROLE_FRIEND : (255, 0, 255),
}

class Entity:
	def __init__(self, guid, role, pos, radius):
		self.guid = guid
		self.role = role
		self.pos = pos
		self.radius = radius

		self.force_next_id = 0
		self.forces = {}
		self.path = None

		_all_entities[guid] = self

	def GetPos(self):
		return self.pos

	def AddForce(self, direction, magnitude, desc, relate_id):
		new_force = force.Force(self, direction, magnitude, desc, relate_id)
		self.force_next_id += 1
		self.forces[self.force_next_id] = new_force
		return self.force_next_id

	def DelForce(self, force_id):
		if force_id in self.forces:
			del self.forces[force_id]

	def SetPath(self, path):
		old_path = self.path

		self.path = path
		return old_path

	def GetRect(self):
		rect = pygame.Rect(
				self.pos[0] - self.radius,
				self.pos[1] - self.radius,
				self.radius * 2.0,
				self.radius * 2.0)

		for f in self.forces.values():
			rect.union_ip(f.GetRect())

		if self.path is not None:
			left = min(self.path, key=lambda pos: pos[0])[0]
			right = max(self.path, key=lambda pos: pos[0])[0]
			top = min(self.path, key=lambda pos: pos[1])[1]
			bottom = max(self.path, key=lambda pos: pos[1])[1]

			path_rect = pygame.Rect(
					left, top, right - left, bottom - top)
			rect.union_ip(path_rect)

		return rect
	
	def Draw(self, board):
		color = COLOR4ROLE[self.role]
		board.DrawCircle(color, self.pos, self.radius)

		for f in self.forces.values():
			f.Draw(board)
					
		if self.path is not None:
			board.DrawLines((0, 0, 0), self.path)