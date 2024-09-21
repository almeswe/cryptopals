from s1c3 import *

def read() -> list[str]:
    with open('./s1c4.txt', 'r') as f:
        return [line.replace('\n', '') for line in f.readlines()]

def find() -> tuple[bytes, int]:
    dist: float = None
    best: tuple = (None, None)
    lines: list[str] = read()
    for line in lines:
        cb: bytes = bytes.fromhex(line)
        p: bytes = crack_onepad_xor(cb)[0]
        f: dict = ascii_trigram_freqmap(p)
        d: float = ascii_trigram_freqmap_dist(f)
        if not dist or dist > d:
            dist = d
            best = (p, lines.index(line))
    assert best[0]
    return best

if __name__ == '__main__':
    p, index = find()
    print(f'{index}) {p.decode("ascii")}')