from s1c7 import *

def find_ecb_block(c: bytes) -> list:
    blocks: dict = {}
    same: list = []
    for i in range(len(c) // 16):
        block: bytes = c[i*16: (i+1)*16]
        if int.from_bytes(block, 'little') in blocks:
            same.append(block)
        else:
            blocks[int.from_bytes(block, 'little')] = True
    print(same)
    return same

if __name__ == '__main__':
    with open('s1c8.txt', 'r') as f: 
        find_ecb_block(f.read().encode('ascii'))