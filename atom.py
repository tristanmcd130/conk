from enum import Flag, auto

class AtomType(Flag):
	NUMBER = auto()
	STRING = auto()
	SYMBOL = auto()
	QUOTE = auto()
	PRIMITIVE = auto()
	def __str__(self):
		return self.name.lower()

class Atom:
	def __init__(self, data_type, value):
		self.type = data_type
		self.value = value
		if data_type == AtomType.NUMBER and type(value) not in [float, int]:
			print(f"Error: Invalid value for number: expected float or int, got {type(value)}")
		elif data_type in [AtomType.STRING, AtomType.SYMBOL] and type(value) != str:
			print(f"Error: Invalid value for string or symbol: expected str, got {type(value)}")
		elif data_type == AtomType.QUOTE:
			if type(value) != list:
				print(f"Error: Invalid value for quote: expected list, got {type(value)}")
			elif not all([isinstance(item, Atom) for item in value]):
				print(f"Error: Invalid values in quote: expected all Atoms, got {[type(item) for item in value]}")
		elif data_type == AtomType.PRIMITIVE and not callable(value):
			print(f"Error: Invalid value for primitive: expected callable, got {type(value)}")
	def __repr__(self):
		match self.type:
			case AtomType.NUMBER:
				return "%g" % self.value
			case AtomType.STRING:
				return self.value
			case AtomType.SYMBOL:
				return self.value
			case AtomType.QUOTE:
				string = "["
				for item in self.value:
					string += str(item) + " "
				if string[-1] == " ":
					string = string[ : -1]
				return string + "]"
			case AtomType.PRIMITIVE:
				return "<primitive>"
