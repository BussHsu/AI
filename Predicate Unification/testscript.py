import InferenceEngine as eng
import myLogics as logic

resolver = eng.Resolver()
a = resolver.resolve_lists(["or","a","b"],["or", ["not","a"], ["not", "a"], "c"])
print a
b = resolver.resolve_lists(["or", "a", "b"], ["or", ["not","a"], ["not","a"], "c", ["not", "b"]])
print b
c = resolver.resolve_lists("a", ["or", ["not", "a"], ["not", "a"]])
print c

infer = eng.InferenceEngine()
infer.tell(["or",["and",["or","a","b"],["not",["implies","c","d"]],["not",["biconditional","k","c"]],["or","a","b","c"],["or","a","b","c"]],"p"])
infer.tell(["implies",["implies","a","b"],["biconditional","b","d"]])
infer.tell("z")

s = logic.Statement(["or" ,"a" ,["or","c",["not","p"]],"p"])
cnf = s.to_CNF()
print cnf
print infer.ask(["or","a","p"])
print infer.knowledge_base
infer.clear()

infer.tell(logic.Statement(['or',['not',['not',['not',['not','b']]]],['not',['not','c']]]).to_CNF())
infer.tell(logic.Statement(['not','b']).to_CNF())
print infer.ask(logic.Statement('b').to_CNF())
print infer.ask(logic.Statement('c').to_CNF())

