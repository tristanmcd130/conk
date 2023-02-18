from re import split, sub, findall
from unicodedata import category

# INTERPRETER FUNCTIONS

def lex(string):
	return [token for token in split(r'([\s\[\]]|"(?:[^"\\]*(?:\\.)*)*")|#.+', string) if token and not token.isspace()]

def is_number(string):
	try:
		float(string)
		return True
	except ValueError:
		return False

def parse(tokens):
	parse_stack = [[]]
	for token in tokens:
		if token == "[":
			parse_stack.append([])
		elif token == "]":
			top = parse_stack.pop()
			parse_stack[-1].append(top)
		elif is_number(token):
			parse_stack[-1].append(float(token))
		elif token[0] == token[-1] == '"':
			parse_stack[-1].append(token[1 : -1].encode()) # string literals are byte strings in order to avoid having to make a class
		else:
			parse_stack[-1].append(token) # symbols are normal python strings
	return parse_stack[-1]

def find(name):
	for env in env_stack[ : : -1]:
		if name in env:
			return env[name]
	return None

def evaluate(tree):
	for atom in tree:
		if callable(atom):
			if atom():
				break
		elif type(atom) == str:
			if find(atom):
				env_stack.append({})
				evaluate(find(atom))
				env_stack.pop()
			elif atom[0] == "\\":
				if len(stack) < 1:
					print("Nothing to assign to function")
					break
				if type(stack[-1]) == list:
					env_stack[-1][atom[1 : ]] = stack.pop()
				else:
					print("Cannot assign non-list to function")
					break
			else:
				print("Unknown word", atom)
				break
		else:
			stack.append(atom)

def unescape(byte_string):
	string = byte_string.decode()
	for replacement in [("\\n", "\n"), ("\\t", "\t"), ("\\b", "\b"), ("\\r", "\r"), ("\\f", "\f"), ('\\"', '"')]:
		string = string.replace(replacement[0], replacement[1])
	for replacement in [("\\" + match, int(match)) for match in findall(r"\\(\d+)", string)]:
		if replacement[1] < 0x110000 and category(chr(replacement[1])) != "Cn":
			string = string.replace(replacement[0], chr(replacement[1]))
	return string

def atom_to_str(atom):
	if type(atom) in [float, int]:
		return "%g" % atom
	elif type(atom) == str:
		return atom
	elif type(atom) == bytes:
		return unescape(atom)
	elif type(atom) == list:
		string = "["
		for element in atom:
			if type(element) == bytes:
				string += '"' + element.decode() + '" '
			else:
				string += atom_to_str(element) + " "
		if string[-1] == " ":
			string = string[ : -1]
		return string + "]"

# PRIMITIVES

def concat():
	if len(stack) < 2:
		print("Stack underflow")
		return 1
	tos = stack.pop()
	nos = stack.pop()
	if type(tos) == type(nos) == list or type(tos) == type(nos) == bytes:
		stack.append(nos + tos)
	else:
		print("Both arguments to concat must be quotations or strings")
		stack.append(nos)
		stack.append(tos)
		return 1

def dup():
	if len(stack) < 1:
		print("Stack underflow")
		return 1
	stack.append(stack[-1])

def eq():
	if len(stack) < 2:
		print("Stack underflow")
		return 1
	tos = stack.pop()
	nos = stack.pop()
	stack.append(int(tos == nos))

def sub():
	if len(stack) < 2:
		print("Stack underflow")
		return 1
	tos = stack.pop()
	nos = stack.pop()
	if type(tos) in [float, int] and type(nos) in [float, int]:
		stack.append(nos - tos)
	else:
		print("Both arguments to - must be numbers")
		stack.append(nos)
		stack.append(tos)
		return 1

def ifelse():
	if len(stack) < 3:
		print("Stack underflow")
		return 1
	else_body = stack.pop()
	if_body = stack.pop()
	if stack.pop():
		evaluate(if_body)
	else:
		evaluate(else_body)

def mul():
	if len(stack) < 2:
		print("Stack underflow")
		return 1
	tos = stack.pop()
	nos = stack.pop()
	if type(tos) in [float, int] and type(nos) in [float, int]:
		stack.append(nos * tos)
	else:
		print("Both arguments to * must be numbers")
		stack.append(nos)
		stack.append(tos)
		return 1
# REPL

stack = []
env_stack = [{
	"print": [lambda: print(end = atom_to_str(stack.pop()))],
	"println": parse(lex('"\\n" concat print')),
	"concat": [concat],
	"dup": [dup],
	"=": [eq],
	"drop": [stack.pop],
	"-": [sub],
	"ifelse": [ifelse],
	"*": [mul],
	
}]
while True:
	tokens = lex(input("> "))
	#print("Tokens:", tokens)
	tree = parse(tokens)
	evaluate(tree)
	#print("Tree:", tree)
	print(atom_to_str(stack))

"""
[			# n
	dup		# n n
	0 =		# n n=0
	[
		drop
		1
	]
	[
		dup	# n n
		1 -	# n n-1
		factorial *
	] ifelse
] \factorial
"""

# [dup 0 = [drop 1] [dup 1 - factorial *] ifelse] \factorial
