from primitives import *

interpreter = Interpreter()
interpreter.add_primitive("+", add)
interpreter.add_primitive("-", sub)
interpreter.add_primitive("print", print_expr)
interpreter.run(r"""
[:a] /drop
[:a a a] /dup
[:a :b a b] /swap
[:a :b b a b] /over
[/a a] /eval
["\n" + print] /println
""")
interpreter.repl()
