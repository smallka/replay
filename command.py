import entity

# return closure which can undo command

def CmdAddEntity(guid, role, pos, radius):
	entity.Entity(guid, role, pos, radius)
	return lambda : entity.DelEntity(guid)