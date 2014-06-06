import entity

# return closure which can undo command

def CmdAddEntity(ent_id, pos, radius):
	entity.Entity(ent_id, pos, radius)
	return lambda : entity.DelEntity(ent_id)

def CmdAddForce(ent_id, direction, magnitude, desc, relate_id):
	ent = entity.GetEntity(ent_id)
	if ent is None:
		return lambda : None
	force_id = ent.AddForce(direction, magnitude, desc, relate_id)
	def Undo():
		same_ent = entity.GetEntity(ent_id)
		if same_ent:
			same_ent.DelForce(force_id)
	return Undo

def CmdSetPath(ent_id, path):
	ent = entity.GetEntity(ent_id)
	if ent is None:
		return lambda : None
	old_path = ent.SetPath(path)
	def Undo():
		same_ent = entity.GetEntity(ent_id)
		if same_ent:
			same_ent.SetPath(old_path)
	return Undo

def CmdSetTargetId(ent_id, target_id):
	ent = entity.GetEntity(ent_id)
	if ent is None:
		return lambda : None
	old_target_id = ent.SetTargetId(target_id)
	def Undo():
		same_ent = entity.GetEntity(ent_id)
		if same_ent:
			same_ent.SetPath(old_target_id)
	return Undo
