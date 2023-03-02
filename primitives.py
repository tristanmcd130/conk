from interpreter import *

def add(interpreter):
	t = interpreter.pop()
	n = interpreter.pop()
	interpreter.push(n + t)

def sub(interpreter):
	t = interpreter.pop()
	n = interpreter.pop()
	interpreter.push(n - t)
