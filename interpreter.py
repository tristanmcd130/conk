from atom import *

def is_number(string):
	try:
		float(string)
		return True
	except ValueError:
		return False

class Interpreter:
	def __init__(self):
		self.stack = Atom(AtomType.QUOTE, [])
		self.env_stack = [{}]
	def run(self, code):
		try:
			self.evaluate(self.parse(self.lex(code)))
		except TypeError:
			return
	def repl(self):
		while True:
			self.run(input("> "))
			print(self.stack)
	def push(self, atom):
		if not isinstance(atom, Atom):
			self.throw("Pushed value is not atom")
		self.stack.value.append(atom)
	def pop(self):
		if not len(self.stack.value):
			self.throw("Stack underflow")
		return self.stack.value.pop()
	def lex(self, string):
		tokens = []
		index = 0
		try:
			while index < len(string):
				while index < len(string) and string[index].isspace():
					index += 1
				if index >= len(string):
					break
				token = string[index]
				index += 1
				match token:
					case "[" | "]":
						tokens.append(token)
					case '"':
						while index < len(string) and string[index] != '"':
							token += string[index]
							index += 1
						token += string[index]
						index += 1
						tokens.append(token)
					case _:
						while index < len(string) and not (string[index].isspace() or string[index] in '[]"'):
							token += string[index]
							index += 1
						tokens.append(token)
			return tokens
		except IndexError:
			self.throw(f"Syntax error in {string}")
	def parse(self, tokens):
		parse_stack = [Atom(AtomType.QUOTE, [])]
		for token in tokens:
			if token == "[":
				parse_stack.append(Atom(AtomType.QUOTE, []))
			elif token == "]":
				top = parse_stack.pop()
				parse_stack[-1].value.append(top)
			elif is_number(token):
				parse_stack[-1].value.append(Atom(AtomType.NUMBER, float(token)))
			elif token[0] == token[-1] == '"':
				parse_stack[-1].value.append(Atom(AtomType.STRING, token[1 : -1]))
			else:
				parse_stack[-1].value.append(Atom(AtomType.SYMBOL, token))
		return parse_stack[-1]
	def find(self, name):
		for env in self.env_stack[ : : -1]:
			if name in env:
				return env[name]
		return None
	def evaluate(self, tree):
		try:
			for atom in tree.value:
				match atom.type:
					case AtomType.PRIMITIVE:
						atom.value(self)
					case AtomType.SYMBOL:
						definition = self.find(atom.value)
						if definition:
							self.env_stack.append({})
							self.evaluate(definition)
							self.env_stack.pop()
						elif atom.value[0] == ":":
							self.env_stack[-1][atom.value[1 : ]] = Atom(AtomType.QUOTE, [self.pop()])
						elif atom.value[0] == "\\":
							quote = self.pop()
							self.type_check(quote, AtomType.QUOTE)
							self.env_stack[-1][atom.value[1 : ]] = quote
						else:
							self.throw(f"Unknown word {atom}")
					case _:
						self.push(atom)
		except TypeError:
			raise TypeError
	def throw(self, message):
		print(f"Error: {message}")
		self.error = True
		raise TypeError
	def type_check(self, atom, expected_type):
		types = ["number", "string", "symbol", "quote", "primitive"]
		if atom.type != expected_type:
			self.throw(f"Expected a {expected_type}, received a {atom.type}")
	def add_primitive(self, name, code):
		self.env_stack[0][name] = Atom(AtomType.QUOTE, [Atom(AtomType.PRIMITIVE, code)])
