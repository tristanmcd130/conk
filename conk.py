from primitives import *
from sys import argv

interpreter = Interpreter()
interpreter.add_primitive("head", head)
interpreter.add_primitive("tail", tail)
interpreter.add_primitive("quit", quit)
interpreter.add_primitive("concat", concat)
interpreter.add_primitive("print", print_atom)
interpreter.add_primitive("=", eq)
interpreter.add_primitive("-", sub)
interpreter.add_primitive("*", mul)
interpreter.add_primitive("ifelse", ifelse)
interpreter.add_primitive("use", use)
interpreter.add_primitive("length", length)
interpreter.add_primitive("quote", quote)
interpreter.add_primitive("debug", debug)
interpreter.run(r"""
	[:a] \drop
	[:a a a] \dup
	[:a :b a b] \swap
	[:a :b b a b] \over
	[:a :b a] \nip
	[\a a] \eval
	[\a :b a b] \dip
	["\n" concat print] \println
	[:a :b b a -1 * -] \+
	[:n n 0 = [1] [n n 1 - factorial *] ifelse] \factorial
	[:list list head dup head eval [tail head eval] [drop list tail cond] ifelse] \cond
	[1] \else
	[:n :m [[[m 0 =] [n 1 +]] [[n 0 =] [m 1 - 1 ackermann]] [[else] [m 1 - m n 1 - ackermann ackermann]]] cond] \ackermann
""")
if len(argv) > 1:
	interpreter.run(f'"{argv[1]}" use')
else:
	interpreter.repl()
