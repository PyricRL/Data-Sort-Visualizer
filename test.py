import sys

def gen():
    yield 1
    yield 2
    yield 3
    yield 4

x = gen()

print(next(x))
print(next(x))
print(next(x))
print(next(x))