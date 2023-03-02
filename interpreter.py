from re import split

class Symbol(str):
	pass

class Interpreter:
	def __init__(self):
		self.stack = []
		self.env_stack = [{}]
	def push(self, value):
		self.stack.append(value)
	def pop(self):
		if not len(self.stack):
			self.throw("Stack underflow") 
		return self.stack.pop()
	def throw(self, message):
		raise Exception(message)
	def tokenize(self, string):
		return [token for token in split(r"([\[\]\s]|\"[^\"]+\")|#.*", string) if token and not token.isspace()]
	def is_number(self, string):
		try:
			float(string)
			return True
		except ValueError:
			return False
	def parse(self, tokens):
		parse_stack = [[]]
		for token in tokens:
			if token == "[":
				parse_stack.append([])
			elif token == "]":
				quote = parse_stack.pop()
				parse_stack[-1].append(quote)
			elif self.is_number(token):
				parse_stack[-1].append(float(token))
			elif token[0] == token[-1] == '"':
				parse_stack[-1].append(token[1 : -1])
			else:
				parse_stack[-1].append(Symbol(token))
		return parse_stack[-1]
	def find(self, name):
		for env in self.env_stack[ : : -1]:
			if name in env:
				return env[name]
	def evaluate(self, tree):
		for expr in tree:
			if callable(expr):
				expr(self)
			elif type(expr) == Symbol:
				definition = self.find(expr)
				if definition != None:
					self.env_stack.append({})
					self.evaluate(definition)
					self.env_stack.pop()
				elif expr[0] == "/":
					self.env_stack[-1][expr[1 : ]] = self.pop()
				elif expr[0] == ":":
					self.env_stack[-1][expr[1 : ]] = [self.pop()]
				else:
					self.throw(f"Unknown word {expr}")
			else:
				self.push(expr)
	def expr_to_str(self, expr):
		if type(expr) in [float, int]:
			return "%g" % expr
		elif type(expr) == str:
			return expr.replace("\\n", "\n")
		elif type(expr) == Symbol:
			return expr
		elif type(expr) == list:
			string = "["
			for element in expr:
				if type(element) == str:
					string += f'"{element}" '
				else:
					string += f"{self.expr_to_str(element)} "
			if string[-1] == " ":
				string = string[ : -1]
			return string + "]"
	def run(self, code):
		try:
			self.evaluate(self.parse(self.tokenize(code)))
		except Exception as e:
			print(f"Error: {str(e).capitalize()}")
	def repl(self):
		while True:
			self.run(input("> "))
			print(self.expr_to_str(self.stack))
	def add_primitive(self, name, function):
		self.env_stack[0][name] = [function]
