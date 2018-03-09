#!/usr/bin/python

from hw2 import resolve

print resolve(["or", "a", "b", "c"], ["not", "b"])
print resolve(["or", "a", "b", "c"], ["or", "b", ["not", "c"]])
print resolve(["or", ["not", "raining"], "wet ground"], "raining")
print resolve(["or", "a", "b"], "c")
print resolve(["or", ["not", "a"], ["not", "b"], ["not", "c"]],
              ["or", "a", "b", ["not", "d"]])
print resolve("a", ["not", "a"])

