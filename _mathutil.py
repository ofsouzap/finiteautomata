def ipow(b: int, p: int, acc: int = 1) -> int:

    if b == p == 0:
        raise ValueError("Can't compute 0^0")
    elif b == 0:
        return 0
    elif p == 0:
        return acc
    elif p == 1:
        return b * acc
    elif p % 2 == 0:
        return ipow(b*b, p//2, acc)
    else:
        # ASSERT: p % 2 == 1 and p > 1
        return ipow(b*b, p//2, b*acc)
