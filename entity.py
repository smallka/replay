import pygame

ROLE_ME = "me"
ROLE_TARGET = "target"
ROLE_FRIEND = "friend"

_all_entity = {}

def GetEntity(guid):
	return _all_entity.get(guid)

def DrawAllEntities(surface):
	for ent in _all_entity.values():
		ent.Draw(surface)

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
		_all_entity[guid] = self

	def Draw(self, surface):
		color = COLOR4ROLE[self.role]
		pygame.draw.circle(surface, color, self.pos, self.radius, 0)
		