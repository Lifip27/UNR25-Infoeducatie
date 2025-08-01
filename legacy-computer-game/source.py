from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import random

flag = bytes_to_long(open('flag.txt', 'rb').read().strip())

p = getPrime(flag.bit_length()+1)
g = 2
secret = getPrime(1024)
private = (g * secret) % p
public = pow(private, 2, p)
flag = flag ^ (secret%p)

def lcg(seed, a, c, m):
    seed = (a * seed + c) % m
    return seed

a = random.randint(1, secret-1)
c = random.randint(1, secret-1)

print(f'p = {p}')
print(f'g = {g}')
print(f'public = {public}')
for i in range(3):
    flag = lcg(flag, a, c, p)
    print(f'flag_{i+1} = {flag}')

