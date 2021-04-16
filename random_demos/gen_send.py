from collections.abc import Generator

def do_it(s: str) -> Generator[int, str, None]:

    print(s)
    result = yield 1
    print(result)

    result = yield 2
    print(result)

    yield 3


gen = do_it('r')
# print(next(gen))
# print(gen.send('a'))
# print(gen.send('b'))
