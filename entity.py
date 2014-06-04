
ROLE_ME = "me"
ROLE_TARGET = "target"
ROLE_FRIEND = "friend"

_all_entities = {}

def GetEntity(guid):
	return _all_entities.get(guid)

def DelEntity(guid):
	if guid in _all_entities:
		del _all_entities[guid]
		
def DrawAllEntities(board):
	top, bottom, left, right = None, None, None, None

	for ent in _all_entities.values():
		if left is None or ent.pos[0] - ent.radius < left:
			left = ent.pos[0] - ent.radius
		if right is None or ent.pos[0] + ent.radius > right:
			right = ent.pos[0] + ent.radius
		if top is None or ent.pos[1] - ent.radius < top:
			top = ent.pos[1] - ent.radius
		if bottom is None or ent.pos[1] + ent.radius > bottom:
			bottom = ent.pos[1] + ent.radius

	if top is not None:
		board.AdjustScaleAndOffset(top, bottom, left, right)

	for ent in _all_entities.values():
		ent.Draw(board)

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
		