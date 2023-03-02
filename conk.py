from primitives import *

interpreter = Interpreter()
interpreter.add_primitive("+", add)
interpreter.add_primitive("-", sub)
interpreter.run("""
[:a] /drop
[:a a a] /dup
[:a :b a b] /swap
[:a :b b a b] /over
[/a a] /eval
""")
interpreter.repl()
