from primitives import *

interpreter = Interpreter()
interpreter.add_primitive("head", head)
interpreter.add_primitive("tail", tail)
interpreter.run(r"""
	[:a] \drop
	[:a a a] \dup
	[:a :b a b] \swap
	[:a :b b a b] \over
	[:a :b a] \nip
	[\a a] \eval
	[\a :b a b] \dip
""")
interpreter.repl()
