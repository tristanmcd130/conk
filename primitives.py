from interpreter import *

def head(interpreter):
	quote = interpreter.pop()
	interpreter.type_check(quote, AtomType.QUOTE)
	interpreter.push(quote.value[0])

def tail(interpreter):
	tos = interpreter.pop()
	interpreter.type_check(tos, AtomType.QUOTE)
	interpreter.push(Atom(AtomType.QUOTE, tos.value[1 : ]))
