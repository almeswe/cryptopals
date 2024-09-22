from s1c3 import *
from s1c4 import *

def repkey_xor(p: bytes, k: bytes) -> bytes:
    assert len(p) >= len(k)
    if len(p) == len(k):
        return xor(p, k)
    rep: bytearray = bytearray(len(p))
    for i in range(len(p)):
        rep[i] = k[i % len(k)]
    return xor(p, rep)

if __name__ == '__main__':
    k: str = 'ICE'
    t: str = '''Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal'''
    th: bytes = tobytes(t)
    kh: bytes = tobytes(k)
    rb: bytes = repkey_xor(th, kh)
    print(tohex(rb))