from interpreter import *

def add(interpreter):
	t = interpreter.pop()
	n = interpreter.pop()
	interpreter.push(n + t)

def sub(interpreter):
	t = interpreter.pop()
	n = interpreter.pop()
	interpreter.push(n - t)

def print_expr(interpreter):
	print(interpreter.expr_to_str(interpreter.pop()), end = "")
