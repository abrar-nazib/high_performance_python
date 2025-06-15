async def z(x):
    return x

async def f(x):
    y = await z(x)
    return y

async def g(x):
    yield x # Async generator
    # yield from is not allowed.