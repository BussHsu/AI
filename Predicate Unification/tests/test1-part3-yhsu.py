from hw2 import *
TELL(["and", ["or", "a", "b"],["or", ["not", "a"], ["not", "c"]]])
print ASK(["implies", "c", "b"])
CLEAR()
TELL(['and',['or',['implies','a','b'],['biconditional','a','c']],['not',['and',['implies','a','b'],['biconditional','a','c']]]])
TELL(['and','a','c'])
print ASK('b')
print ASK(['implies','a','c'])
print ASK(['implies','c','a'])
print ASK(['biconditional','a','c'])
