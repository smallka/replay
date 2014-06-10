import sys

import entity

def to_pos(str):
	return [ float(v) for v in str[1:-1].split(":") ]

######################## commands ##########################
#
# return closure for undo operation
#
###########################################################

def add_entity(ent_id, pos, radius):
	entity.Entity(ent_id, pos, radius)
	return lambda : entity.DelEntity(ent_id)

def set_force(ent_id, direction, magnitude):
	ent = entity.GetEntity(ent_id)
	if ent is None:
		return lambda : None

	force_id = ent.AddForce(direction, magnitude, "", None)
	def Undo():
		same_ent = entity.GetEntity(ent_id)
		if same_ent:
			same_ent.DelForce(force_id)
	return Undo

def set_path(ent_id, *path):
	ent = entity.GetEntity(ent_id)
	if ent is None:
		return lambda : None

	old_path = ent.SetPath(path)
	def Undo():
		same_ent = entity.GetEntity(ent_id)
		if same_ent:
			same_ent.SetPath(old_path)
	return Undo

def set_target(ent_id, target_id):
	ent = entity.GetEntity(ent_id)
	if ent is None:
		return lambda : None
	old_target_id = ent.SetTargetId(target_id)
	def Undo():
		same_ent = entity.GetEntity(ent_id)
		if same_ent:
			same_ent.SetTargetId(old_target_id)
	return Undo

keywords = {
	"add_entity": (int, to_pos, float, ),
	"set_force": (int, to_pos, float, ),
	"set_path": (int, to_pos, ),
	"set_target": (int, int, ),
}

class Processor:
	def __init__(self, filename):
		self.lines = open(filename, "r").readlines()
		self.line_idx = -1
		self.cmd_queue = []

	# find and execute the next command
	# return the line number and text 
	def Next(self):
		self.line_idx += 1
		while self.line_idx < len(self.lines):
			line = self.lines[self.line_idx].strip()

			for keyword, converters in keywords.iteritems():
				idx = line.find(keyword)
				if idx == -1:
					continue
				fields = line[idx:].split(",")[1:]
				args = []
				for field_idx in xrange(len(fields)):
					field = fields[field_idx].strip()
					converter = converters[min(field_idx, len(converters)-1)]
					args.append(converter(field))
					
				print keyword, args
				undo = getattr(sys.modules[__name__], keyword)(*args)
				self.cmd_queue.append((self.line_idx, undo))
				return "%d: %s" % (self.line_idx, line)

			self.line_idx += 1
		return None

	def Prev(self):
		if len(self.cmd_queue) <= 0:
			return False

		last_cmd = self.cmd_queue.pop()

		last_cmd[1]()

		self.line_idx = last_cmd[0] - 1
		return True
