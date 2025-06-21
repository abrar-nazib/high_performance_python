# Your example has a small issue - it yields a tuple, not individual values
def gen():
    yield 1, 2, 3  # This yields ONE tuple: (1, 2, 3)


# What you probably meant:
def counting():
    yield 1
    yield 2
    yield 3


g = counting()
print(next(g))  # 1
print(next(g))  # 2
print(next(g))  # 3
# print(next(g))  # Would raise StopIteration
