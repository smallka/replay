import entity

# return closure which can undo command

def CmdAddEntity(guid, role, pos, radius):
	entity.Entity(guid, role, pos, radius)
	return lambda : entity.DelEntity(guid)

def CmdAddForce(guid, direction, magnitude, desc, relate_id):
	ent = entity.GetEntity(guid)
	if ent is None:
		return lambda : None
	force_id = ent.AddForce(direction, magnitude, desc, relate_id)
	def Undo():
		ent = entity.GetEntity(guid)
		if ent:
			ent.DelForce(force_id)
	return Undo

def CmdSetPath(guid, path):
	ent = entity.GetEntity(guid)
	if ent is None:
		return lambda : None
	old_path = ent.SetPath(path)
	def Undo():
		ent = entity.GetEntity(guid)
		if ent:
			ent.SetPath(old_path)
	return Undo
