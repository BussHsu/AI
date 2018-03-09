from hw2 import *
TELL(["or", "a", "b", "c"])
TELL(["or", "b", "e", ["not", "c"]])
print ASK(["or", "a", "b", "e"])

CLEAR()

TELL('a')
print ASK('b')
print ASK('a')

CLEAR()

TELL('a')
print ASK(['not', 'a'])

CLEAR()
print ASK(['or','a',['not','a']])
