from fpylll import IntegerMatrix, LLL, GSO, CVP, FPLLL

def parse_instance(path="output.txt"):
    with open(path) as f:
        src = f.read()
    scope = {}
    exec(compile(src, path, 'exec'), {}, scope)
    return scope["p"], scope["cool"], scope["a"]

p, cool, a = parse_instance()

n = 64
m = n + 1

rows = [[0]*m for _ in range(m)]
rows[0][0] = int(p)
for i in range(1, m):
    rows[i][0] = int(a[i-1])
    rows[i][i] = 16

t = [int(cool)] + [0]*n

def combine_rows(rows, coeffs):
    v = [0]*len(rows[0])
    for i, c in enumerate(coeffs):
        if c == 0:
            continue
        ri = rows[i]
        for j in range(len(ri)):
            v[j] += int(c) * ri[j]
    return v

def attempt(prec_bits):
    A = IntegerMatrix.from_matrix(rows)
    LLL.reduction(A, delta=0.99)
    A_rows = [[int(A[i, j]) for j in range(m)] for i in range(m)]
    FPLLL.set_precision(prec_bits)
    M = GSO.Mat(A, float_type='mpfr')
    M.update_gso()

    try:
        res = CVP.closest_vector(M, t)
    except TypeError:
        res = CVP.closest_vector(A, t)

    res = [int(x) for x in res]
    candidates = [combine_rows(A_rows, res)]
    if len(res) == m:
        candidates.append(res)

    for v in candidates:
        delta = v[0] - t[0]
        if delta % p != 0:
            q = round(delta / p)
            v = v[:]
            v[0] -= q * p

        xs = []
        ok = True
        for i in range(1, m):
            vi = v[i]
            if vi % 16 != 0:
                ok = False
                break
            d = vi // 16
            if not (0 <= d <= 15):
                ok = False
                break
            xs.append(int(d))
        if not ok:
            continue

        lhs = sum(int(ai)*int(di) for ai, di in zip(a, xs))
        if (lhs - cool) % p != 0:
            continue

        HEX = "0123456789abcdef"
        h1 = ''.join(HEX[d] for d in xs)
        xs2 = [xs[j+1] if j % 2 == 0 else xs[j-1] for j in range(n)]
        h2 = ''.join(HEX[d] for d in xs2)

        b1 = bytes.fromhex(h1)
        b2 = bytes.fromhex(h2)

        def okflag(b):
            try:
                s = b.decode()
            except Exception:
                return None
            return s if s.startswith("CTF{") and s.endswith("}") and len(s) == 32 else None

        out = okflag(b1) or okflag(b2)
        if out:
            return out

    return None

def main():
    print("fpylll + CVS solver")
    for prec in (256, 384, 512, 768, 1024, 1536, 2048, 3072, 4096):
        print(f"bits: {prec}")
        out = attempt(prec)
        if out:
            print(out)
            return
    print("no")

if __name__ == "__main__":
    main()
