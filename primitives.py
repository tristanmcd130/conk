from interpreter import *

def add(interpreter):
	t = interpreter.pop()
	interpreter.push(interpreter.pop() + t)

def sub(interpreter):
	t = interpreter.pop()
	interpreter.push(interpreter.pop() - t)

def print_expr(interpreter):
	print(interpreter.expr_to_str(interpreter.pop()), end = "")

def evaluate(interpreter):
	interpreter.evaluate(interpreter.pop())

def head(interpreter):
	interpreter.push(interpreter.pop()[0])

def tail(interpreter):
	interpreter.push(interpreter.pop()[1 : ])

def ifelse(interpreter):
	else_body = interpreter.pop()
	if_body = interpreter.pop()
	if interpreter.pop():
		interpreter.evaluate(if_body)
	else:
		interpreter.evaluate(else_body)

def eq(interpreter):
	t = interpreter.pop()
	interpreter.push(int(interpreter.pop() == t))

def mul(interpreter):
	t = interpreter.pop()
	interpreter.push(interpreter.pop() * t)

def clear(interpreter):
	interpreter.stack = []

def quote(interpreter):
	interpreter.push([interpreter.pop()])

def while_loop(interpreter):
	body = interpreter.pop()
	condition = interpreter.pop()
	while True:
		interpreter.evaluate(condition)
		if not interpreter.pop():
			break
		interpreter.evaluate(body)
