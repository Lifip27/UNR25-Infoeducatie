import socket, re, time, math
from hashlib import sha256
from Crypto.Cipher import AES

ip = "insert ip"
port = insertport

prompt_key = "Give me a vector B"
norm_key = "here it is:"
ct_key = "jumbled up prize:"

def get_norm_squared(line):
    line = line.strip()
    if line == "0":
        return 0
    if m := re.fullmatch(r'(\d+)\*sqrt\((\d+)\)', line):
        return int(m.group(1))**2 * int(m.group(2))
    if m := re.fullmatch(r'sqrt\((\d+)\)', line):
        return int(m.group(1))
    if line.isdigit():
        return int(line)
    raise ValueError(f"Bad format: {line}")

def wait_for_prompt(f):
    while True:
        line = f.readline()
        if not line:
            raise RuntimeError("Disconnected")
        if prompt_key in line.decode(errors="ignore"):
            return

def send_vector(f, x, y, z):
    f.write(f"{x} {y} {z}\n".encode())
    f.flush()
    norm, ct = None, None
    deadline = time.time() + 10
    while time.time() < deadline:
        line = f.readline()
        if not line:
            break
        s = line.decode(errors="ignore").strip()
        if norm_key in s:
            norm = s.split(":")[1].strip()
        elif ct_key in s:
            ct = s.split(":")[1].strip()
            break
    if not norm or not ct:
        raise RuntimeError("Missing data")
    return get_norm_squared(norm), ct

def connect(ip, port):
    s = socket.create_connection((ip, port), timeout=10)
    s.settimeout(10)
    f = s.makefile("rwb", buffering=0)
    return s, f

def main():
    print("Connecting...")
    s, f = connect(ip, port)

    try:
        wait_for_prompt(f)
        print("B = 1 0 0")
        n1, _ = send_vector(f, 1, 0, 0)

        wait_for_prompt(f)
        print("B = 0 1 0")
        n2, _ = send_vector(f, 0, 1, 0)

        wait_for_prompt(f)
        print("B = 0 0 1")
        n3, _ = send_vector(f, 0, 0, 1)

        x = (n2 + n3 - n1) // 2
        y = (n1 + n3 - n2) // 2
        z = (n1 + n2 - n3) // 2

        a1 = math.isqrt(x)
        a2 = math.isqrt(y)
        a3 = math.isqrt(z)

        wait_for_prompt(f)
        print(f"B = {a1} {a2} {a3}")
        _, ct_hex = send_vector(f, a1, a2, a3)

        key = sha256(b"(0, 0, 0)").digest()
        ct = bytes.fromhex(ct_hex)
        pt = AES.new(key, AES.MODE_ECB).decrypt(ct)

        pad = pt[-1]
        if 1 <= pad <= 16 and pt.endswith(bytes([pad]) * pad):
            flag = pt[:-pad]
        else:
            key2 = sha256(b"(0,0,0)").digest()
            pt2 = AES.new(key2, AES.MODE_ECB).decrypt(ct)
            pad2 = pt2[-1]
            if 1 <= pad2 <= 16 and pt2.endswith(bytes([pad2]) * pad2):
                flag = pt2[:-pad2]
            else:
                flag = pt

        try:
            print("Flag:", flag.decode())
        except:
            print("Flag bytes:", flag)

    finally:
        f.close()
        s.close()

if __name__ == "__main__":
    main()
