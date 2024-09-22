import base64

def decrypt_aes_ecb(c: bytes, key: bytes) -> bytes:
    from Crypto.Cipher import AES
    aes = AES.new(key=key, mode=AES.MODE_ECB)
    return aes.decrypt(c)

if __name__ == '__main__':
    k: bytes = b'YELLOW SUBMARINE'
    with open('s1c7.txt', 'rb') as f:
        c: bytes = base64.b64decode(f.read())
        print(decrypt_aes_ecb(c, k).decode('ascii'))