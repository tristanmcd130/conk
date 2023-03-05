from primitives import *

interpreter = Interpreter()
interpreter.add_primitive("+", add)
interpreter.add_primitive("-", sub)
interpreter.add_primitive("print", print_expr)
interpreter.add_primitive("eval", evaluate)
interpreter.add_primitive("head", head)
interpreter.add_primitive("tail", tail)
interpreter.add_primitive("ifelse", ifelse)
interpreter.add_primitive("=", eq)
interpreter.add_primitive("*", mul)
interpreter.add_primitive("clear", clear)
interpreter.add_primitive("quote", quote)
interpreter.add_primitive("while", while_loop)
interpreter.run(r"""
[:a] \drop
[:a a a] \dup
[:a :b a b] \swap
[:a :b b a b] \over
[:a :b a] \nip
[print "\n" print] \println
[quote swap quote swap +] \cons
[:quote2 :quote1 :a a quote1 eval a quote2 eval] \bi
[[tail] [head] bi] \uncons
[uncons dup head eval [tail head nip eval] [drop cond] ifelse] \cond
[:n :m [[[m 0 =] [n 1 +]] [[n 0 =] [m 1 - 1 ackermann]] [[1] [m 1 - m n 1 - ackermann ackermann]]] cond] \ackermann
[:n n 0 = [1] [n n 1 - factorial *] ifelse] \factorial
""")
interpreter.repl()
