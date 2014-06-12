import math
import pygame

import force

COLOR_ENTITY_ME = (100, 255, 255)
COLOR_ENTITY_TARGET = (255, 0, 0)
COLOR_ENTITY_OTHER = (255, 255, 128)

COLOR_PATH = (128, 255, 128)

# in order: me, target, others
_entities = []
_me_id = None
_target_id = None

def _AddEntity(ent):
	if ent.id == _me_id:
		_entities.insert(0, ent)

	elif ent.id == _target_id:
		if len(_entities) > 0 and _entities[0].id == _me_id:
			_entities.insert(1, ent)
		else:
			_entities.insert(0, ent)
	else:
		_entities.append(ent)

def GetEntity(ent_id):
	for ent in _entities:
		if ent.id == ent_id:
			return ent
	return None

def DelEntity(ent_id):
	ent = GetEntity(ent_id)
	if ent is not None:
		_entities.remove(ent)

def GetAllEntities():
	return _entities

def GetEntityAtPos(pos):
	cands = []
	for ent in _entities:
		dist = math.hypot(ent.pos[0] - pos[0], ent.pos[1] - pos[1])
		if dist <= ent.radius:
			cands.append((ent, dist))

	ret = None
	min_dist = None
	for cand in cands:
		if min_dist is None or cand[1] < min_dist:
			ret = cand[0]
			min_dist = cand[1]

	return ret

def SetMe(ent):
	global _me_id, _target_id

	_me_id = ent.id
	_target_id = ent.target_id

	olds = _entities[:]
	del _entities[:]
	for ent in olds:
		_AddEntity(ent)

def GetMe():
	if _me_id is None:
		return None
	return GetEntity(_me_id)

class Entity:
	def __init__(self, id, pos, radius):
		self.id = id
		self.pos = pos
		self.radius = radius

		self.target_id = None

		self.force_next_id = 0
		self.forces = {}
		self.path = None

		_AddEntity(self)

	def GetPos(self):
		return self.pos

	def SetTargetId(self, target_id):
		old_target_id = self.target_id
		self.target_id = target_id

		if self.id == _me_id:
			global _target_id
			_target_id = target_id

		return old_target_id

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

	def SetPos(self, pos):
		old_pos = self.pos
		self.pos = pos
		return old_pos

	def GetRect(self):
		rect = pygame.Rect(
				self.pos[0] - self.radius,
				self.pos[1] - self.radius,
				self.radius * 2.0,
				self.radius * 2.0)

		for f in self.forces.values():
			rect.union_ip(f.GetRect())

		if self.path is not None:
			left, right, top, bottom = None, None, None, None
			for pos in self.path:
				if left is None or pos[0] < left:
					left = pos[0]
				if right is None or pos[0] > right:
					right = pos[0]
				if top is None or pos[1] < top:
					top = pos[1]
				if bottom is None or pos[1] > bottom:
					bottom = pos[1]

			path_rect = pygame.Rect(
					left, top, right - left, bottom - top)
			rect.union_ip(path_rect)

		return rect
	
	def Draw(self, board):
		if self.id == _me_id:
			board.DrawCircle(COLOR_ENTITY_ME, self.pos, self.radius)
						
			if self.path is not None:
				board.DrawPath(COLOR_PATH, self.path)

			for f in self.forces.values():
				f.Draw(board)

			board.DrawInfoText("guid = %d, pos = (%.2f, %.2f)"
					% (self.id, self.pos[0], self.pos[1]))

		elif self.id == _target_id:
			board.DrawCircle(COLOR_ENTITY_TARGET, self.pos, self.radius)

		else:
			board.DrawCircle(COLOR_ENTITY_OTHER, self.pos, self.radius)
