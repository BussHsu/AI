from hw2 import *

print resolve(["or","a","b"],["or",["not","a"],'b',"c"])
print resolve(["or","a","b"],["or",["not","a"],"c",["not","b"]])
print resolve("a","a")
print resolve(["not","a"],["not","a"])
print resolve(['or','a',['not','a'],'b'],['or',['not','b'],'c'])
