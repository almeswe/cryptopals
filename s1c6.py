import base64

from s1c5 import *

def hamm_dist(a: bytes, b: bytes) -> int:
    assert len(a) == len(b)
    dist: int = 0
    for i in range(len(a)):
        c: int = a[i] ^ b[i]
        for _ in range(8):
            dist += c & 1
            c >>= 1
    return dist

def transpose(c: bytes, keysz: int) -> list:
    blocks: list[bytearray] = []
    for _ in range(keysz):
        blocks.append(bytearray())
    for i in range(0, len(c)):
        blocks[i % keysz].append(c[i])
    return [bytes(ba) for ba in blocks]

def try_crack_repkey_xor(c: bytes, try_keys: int) -> list[bytes]:
    size: int = None
    dist: float = None
    best: tuple = ([], None)
    for _ in range(try_keys):
        dist = None
        for keysz in range(2, 41):
            if 4 * keysz < len(c):
                k1: bytes = c[0 * keysz:1 * keysz]
                k2: bytes = c[1 * keysz:2 * keysz]
                k3: bytes = c[2 * keysz:3 * keysz]
                k4: bytes = c[3 * keysz:4 * keysz]
                distf: float = (
                    hamm_dist(k1, k2) + hamm_dist(k1, k3) +
                    hamm_dist(k1, k4) + hamm_dist(k2, k3) +
                    hamm_dist(k2, k4) + hamm_dist(k3, k4)
                ) / 6
                distf /= float(keysz)
                if not dist or dist > distf:
                    if keysz not in best[0]:
                        dist = distf
                        size = keysz
        best[0].append(size)
    keys: list[bytes] = []
    for keysz in best[0]:
        key: bytearray = bytearray()
        t: list[bytearray] = transpose(c, keysz)
        for block in t:
            key.append(crack_onebkey_xor(block)[1])
        keys.append(bytes(key))
    return keys

def crack_repkey_xor(c: bytes, try_keys: int = 1) -> tuple[bytes, bytes]:
    dist: float = None
    best: tuple = (None, None)
    for k in try_crack_repkey_xor(c, try_keys):
        p: bytes = repkey_xor(c, k)
        f: dict = ascii_trigram_freqmap(p)
        d: float = ascii_trigram_freqmap_dist(f)
        if not dist or dist > d:
            dist = d
            best = (p, k)
    return best

if __name__ == '__main__':
    assert hamm_dist(tobytes('this is a test'), tobytes('wokka wokka!!!')) == 37
    with open('s1c6.txt', 'rb') as f:
        c: bytes = base64.b64decode(f.read())
        p, k = crack_repkey_xor(c, 3)
        print(p)
        print(k)