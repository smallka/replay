
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

		_all_entities[guid] = self

	def Draw(self, board):
		color = COLOR4ROLE[self.role]
		board.DrawCircle(color, self.pos, self.radius)
		