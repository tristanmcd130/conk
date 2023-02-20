from interpreter import *

def head(interpreter):
	quote = interpreter.pop()
	interpreter.type_check(quote, AtomType.QUOTE)
	interpreter.push(quote.value[0])

def tail(interpreter):
	tos = interpreter.pop()
	interpreter.type_check(tos, AtomType.QUOTE)
	interpreter.push(Atom(AtomType.QUOTE, tos.value[1 : ]))

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
