from primitives import *

interpreter = Interpreter()
interpreter.add_primitive("head", head)
interpreter.add_primitive("tail", tail)
interpreter.add_primitive("quit", quit)
interpreter.add_primitive("concat", concat)
interpreter.add_primitive("print", print_atom)
interpreter.run(r"""
	[:a] \drop
	[:a a a] \dup
	[:a :b a b] \swap
	[:a :b b a b] \over
	[:a :b a] \nip
	[\a a] \eval
	[\a :b a b] \dip
	["\n" concat print] \println
""")
interpreter.repl()
