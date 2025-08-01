from Crypto.Cipher import AES
from hashlib import sha256
from sage.all import *
from secret import FLAG, A
import sys
import signal

A = vector(ZZ, A)

def encrypt_flag(key, flag):
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Pad the flag to a multiple of 16 bytes
    pad_len = 16 - (len(flag) % 16)
    padded_flag = flag + bytes([pad_len] * pad_len)
    
    return cipher.encrypt(padded_flag).hex()

def generate_challenge():
    print("The merchant of doom arrives!")
    print("From the depths of the underworld, he brings the following message:")
    print("Give me a vector B (3 integers, space-separated): ")
    
    inp = input().strip().split()
    if len(inp) != 3:
        print("The merchant of doom is not quite sure what you mean. Try again.")
        return
    
    if not all(map(lambda x: x.isdigit(), inp)):
        print("The merchant of doom is confused. Try again.")
        return
    
    if all(map(lambda x: int(x) == 0, inp)):
        print("The merchant of doom is displeased. Try again.")
        return
    
    # Get user input
    B = vector(ZZ, map(int, inp))

    cP = A.cross_product(B)
    cPN = cP.norm()
    print(f"[Merchant of DOOM] Alright, here it is: {cPN}")
    
    # Generate encryption key from SHA-256 hash of the cross product
    encryption_key = sha256(str(cP).encode()).digest()

    # Encrypt the flag
    encrypted_flag = encrypt_flag(encryption_key, FLAG)

    print(f"[Merchant Of DOOM] Here's your jumbled up prize: {encrypted_flag}")

def timeout_handler(_, __):
    print("\nTime is up! Closing the challenge.")
    sys.exit(0)  # Exit the program

if __name__ == "__main__":
  signal.signal(signal.SIGALRM, timeout_handler)
  signal.alarm(30)
  while True:
    generate_challenge()