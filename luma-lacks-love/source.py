import random
from Crypto.Util.number import getPrime

flag = open('flag.txt','rb').read().strip()
flag = flag.hex()

cool = 0
p = getPrime(512)
a = [random.randint(1,p-1) for _ in range(len(flag))]

for i in range(len(flag)):
    cool += int(flag[i],16) * a[i]
    cool %= p

print(f'p = {p}')
print(f'a = {a}')
print(f'cool = {cool}')
