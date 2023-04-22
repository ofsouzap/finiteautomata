from _mathutil import ipow


def slow_pow(b: int, p: int) -> int:

    if b == p == 0:
        raise ValueError()
    elif b == 0:
        return 0
    else:
        acc = 1
        for _ in range(p):
            acc *= b
        return acc


def test_general():

    for b in range(50):
        for p in range(10):

            if b == p == 0: continue

            res = ipow(b, p)
            exp = slow_pow(b, p)
            assert res == exp, f"{b}^{p} gave {res} but should be {exp}"
