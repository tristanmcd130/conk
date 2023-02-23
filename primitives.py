from interpreter import *

def head(interpreter):
	quote = interpreter.pop()
	interpreter.type_check(quote, AtomType.QUOTE)
	if len(quote.value) == 0:
		interpreter.throw("Cannot get head of empty quote")
	interpreter.push(quote.value[0])

def tail(interpreter):
	quote = interpreter.pop()
	interpreter.type_check(quote, AtomType.QUOTE)
	interpreter.push(Atom(AtomType.QUOTE, quote.value[1 : ]))

def quit(interpreter):
	exit()

def concat(interpreter):
	tos = interpreter.pop()
	nos = interpreter.pop()
	interpreter.type_check(tos, AtomType.QUOTE | AtomType.STRING)
	interpreter.type_check(nos, tos.type)
	interpreter.push(Atom(tos.type, nos.value + tos.value))

def print_atom(interpreter):
	tos = interpreter.pop()
	print(tos, end = "")

def eq(interpreter):
	tos = interpreter.pop()
	nos = interpreter.pop()
	interpreter.type_check(nos, tos.type)
	interpreter.push(Atom(AtomType.NUMBER, int(tos.value == nos.value)))

def sub(interpreter):
	tos = interpreter.pop()
	nos = interpreter.pop()
	interpreter.type_check(tos, AtomType.NUMBER)
	interpreter.type_check(nos, AtomType.NUMBER)
	interpreter.push(Atom(AtomType.NUMBER, nos.value - tos.value))

def mul(interpreter):
	tos = interpreter.pop()
	nos = interpreter.pop()
	interpreter.type_check(tos, AtomType.NUMBER)
	interpreter.type_check(nos, AtomType.NUMBER)
	interpreter.push(Atom(AtomType.NUMBER, nos.value * tos.value))

def ifelse(interpreter):
	else_body = interpreter.pop()
	if_body = interpreter.pop()
	condition = interpreter.pop()
	interpreter.type_check(else_body, AtomType.QUOTE)
	interpreter.type_check(if_body, AtomType.QUOTE)
	if condition.value:
		interpreter.evaluate(if_body)
	else:
		interpreter.evaluate(else_body)

def use(interpreter):
	filename = interpreter.pop()
	interpreter.type_check(filename, AtomType.STRING)
	try:
		with open(filename.value, "r") as f:
			interpreter.run(f.read())
	except FileNotFoundError:
		interpreter.throw(f'File "{filename}" not found')

def length(interpreter):
	quote = interpreter.pop()
	interpreter.type_check(quote, AtomType.QUOTE)
	interpreter.push(Atom(AtomType.NUMBER, len(quote.value)))

def quote(interpreter):
	interpreter.push(Atom(AtomType.QUOTE, [interpreter.pop()]))

def debug(interpreter):
	interpreter.debug = not interpreter.debug
