def xor(a: bytes, b: bytes) -> bytes:
    assert len(a) == len(b)
    return int.to_bytes(int.from_bytes(a, 'little') ^ int.from_bytes(b, 'little'), len(a), 'little')

def tohex(b: bytes) -> str:
    s: str = ''
    for bb in b:
        c = hex(bb)[2:]
        if len(c) == 1:
            c = '0' + c
        s += c
    return s

def tobytes(s: str) -> bytes:
    return bytes(s, 'ascii')

def frombytes(b: bytes) -> str:
    return b.decode('ascii')

def onebkey_xor(p: bytes, k: int) -> bytes:
    return xor(p, bytes(bytearray([k] * len(p))))

def crack_onebkey_xor(c: bytes) -> tuple[bytes, int]:
    dist: float = None
    best: tuple = (None, None)
    for k in range(0x000, 0x100):
        p: bytes = onebkey_xor(c, k)
        f: dict = ascii_freqmap(p)
        d: float = ascii_freqmap_dist(f)
        if not dist or dist > d:
            dist = d
            best = (p, k)
    assert best[0]
    return best

def freqmap_norm(freqmap: dict, over: int) -> dict:
    for key in freqmap:
        freqmap[key] = float(freqmap[key]) / over
    return freqmap

def ascii_freqmap(p: bytes) -> dict:
    d: dict = {
        'e' : 0.0, 't' : 0.0, 'a' : 0.0, 'o' : 0.0,
        'i' : 0.0, 'n' : 0.0, 's' : 0.0, 'r' : 0.0,
        'h' : 0.0, 'd' : 0.0, 'l' : 0.0, 'u' : 0.0,
        'c' : 0.0, 'm' : 0.0, 'f' : 0.0, 'y' : 0.0,
        'w' : 0.0, 'g' : 0.0, 'p' : 0.0, 'b' : 0.0, 
        'v' : 0.0, 'k' : 0.0, 'x' : 0.0, 'q' : 0.0,
        'j' : 0.0, 'z' : 0.0
    }
    for c in p:
        if ischar(c):
            d[chr(c).lower()] += 1
    freqmap_norm(d, len(p))
    return d

def ascii_freqmap_dist(freqmap: dict) -> float:
    golden_freqmap: dict = {
        'e' : 0.0120, 't' : 0.0910, 'a' : 0.0812,
        'o' : 0.0768, 'i' : 0.0731, 'n' : 0.0695,
        's' : 0.0628, 'r' : 0.0602, 'h' : 0.0592,
        'd' : 0.0432, 'l' : 0.0398, 'u' : 0.0288,
        'c' : 0.0271, 'm' : 0.0261, 'f' : 0.0230,
        'y' : 0.0211, 'w' : 0.0209, 'g' : 0.0203,
        'p' : 0.0182, 'b' : 0.0149, 'v' : 0.0111,
        'k' : 0.0069, 'x' : 0.0017, 'q' : 0.0011,
        'j' : 0.0010, 'z' : 0.0007
    }
    dist: float = 0.0
    for key in freqmap:
        dist += (golden_freqmap[key] - freqmap[key]) ** 2
    return dist

def ascii_trigram_freqmap(p: bytes) -> dict:
    d: dict = {
        'the': 0.0,
        'and': 0.0,
        'ing': 0.0,
        'her': 0.0,
        'hat': 0.0,
        'his': 0.0,
        'tha': 0.0,
        'ere': 0.0,
        'for': 0.0,
        'ent': 0.0,
        'ion': 0.0,
        'ter': 0.0,
        'was': 0.0,
        'you': 0.0,
        'ith': 0.0,
        'ver': 0.0,
        'all': 0.0,
        'wit': 0.0,
        'thi': 0.0,
        'tio': 0.0
    }
    for i in range(0, len(p), 1):
        if i + 1 < len(p) and i + 2 < len(p):
            if ischar(p[i]) and ischar(p[i+1]) and ischar(p[i+2]):
                trigram: str = f'{chr(p[i])}{chr(p[i+1])}{chr(p[i+2])}'.lower()
                if trigram in d:
                    d[trigram] += 1
    freqmap_norm(d, len(p))
    return d

def ascii_trigram_freqmap_dist(fmap: dict) -> float:
    golden_freqmap: dict = {
        'the': 0.03508232,
        'and': 0.01593878,
        'ing': 0.01147042,
        'her': 0.00822444,
        'hat': 0.00650715,
        'his': 0.00596748,
        'tha': 0.00593593,
        'ere': 0.00560594,
        'for': 0.00555372,
        'ent': 0.00530771,
        'ion': 0.00506454,
        'ter': 0.00461099,
        'was': 0.00460487,
        'you': 0.00437213,
        'ith': 0.00431250,
        'ver': 0.00430732,
        'all': 0.00422758,
        'wit': 0.00397290,
        'thi': 0.00394796,
        'tio': 0.00378058
    }
    distance: float = 0.0
    for key in fmap:
        distance += (golden_freqmap[key] - fmap[key]) ** 2
    return distance

def ascii_quadrigram_freqmap(p: bytes) -> dict:
    d: dict = {
        'that': 0.00761242,
        'ther': 0.00604501,
        'with': 0.00573866,
        'tion': 0.00551919,
        'here': 0.00374549,
        'ould': 0.00369920,
        'ight': 0.00309440,
        'have': 0.00290544,
        'hich': 0.00284292,
        'whic': 0.00283826,
        'this': 0.00276333,
        'thin': 0.00270413,
        'they': 0.00262421,
        'atio': 0.00262386,
        'ever': 0.00260695,
        'from': 0.00258580,
        'ough': 0.00253447,
        'were': 0.00231089,
        'hing': 0.00229944,
        'ment': 0.00223347
    }
    for i in range(0, len(p), 1):
        if i + 3 < len(p):
            if ischar(p[i]) and ischar(p[i+1]) and ischar(p[i+2]) and ischar(p[i+3]):
                quadrigram: str = f'{chr(p[i])}{chr(p[i+1])}{chr(p[i+2])}{chr(p[i+3])}'.lower()
                if quadrigram in d:
                    d[quadrigram] += 1
    freqmap_norm(d, len(p))
    return d

def ascii_quadrigram_freqmap_dist(fmap: dict) -> float:
    golden_freqmap: dict = {
        'that': 0.0,
        'ther': 0.0,
        'with': 0.0,
        'tion': 0.0,
        'here': 0.0,
        'ould': 0.0,
        'ight': 0.0,
        'have': 0.0,
        'hich': 0.0,
        'whic': 0.0,
        'this': 0.0,
        'thin': 0.0,
        'they': 0.0,
        'atio': 0.0,
        'ever': 0.0,
        'from': 0.0,
        'ough': 0.0,
        'were': 0.0,
        'hing': 0.0,
        'ment': 0.0
    }
    distance: float = 0.0
    for key in fmap:
        distance += (golden_freqmap[key] - fmap[key]) ** 2
    return distance

def ischar(ival: int) -> bool:
    return (ival in range(ord('A'), ord('Z'))) or\
           (ival in range(ord('a'), ord('z')))

if __name__ == '__main__':
    c1: str = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    c2: str = 'ETAOIN SHRDLU'
    c1b: bytes = bytes.fromhex(c1)
    c2b: bytes = tobytes(c2)
    p1, k = crack_onebkey_xor(c1b)
    print(p1.decode('ascii'))
    p2 = onebkey_xor(c2b, k)
    print(p2.decode('ascii'))
