# merchandise

## Descriere

Serverul (SageMath) criptează flag-ul cu **AES-ECB**, folosind drept cheie `SHA256(str(A × B))`, unde:
- **A** = vector 3D secret (de pe server),
- **B** = vector 3D introdus de client.

Obiectiv: alege **B** astfel încât cheia să devină **cunoscută** și să putem decripta flag-ul.

---

## Fișiere

- `chall.sage` — logică server
- `solve.py` — exploit client (rezolvarea automată)

---

## Observație

### Flux pe server (`chall.sage`)

Serverul primește `B`, calculează produsul vectorial și derivă cheia din acesta:

```python
# prompt + validare minimală
print("Give me a vector B (3 integers, space-separated): ")
inp = input().strip().split()
if len(inp) != 3:
    ...
if not all(map(lambda x: x.isdigit(), inp)):
    ...
if all(map(lambda x: int(x) == 0, inp)):
    ...

# A × B + normă
B  = vector(ZZ, map(int, inp))
cP = A.cross_product(B)
cPN = cP.norm()
print(f"[Merchant of DOOM] Alright, here it is: {cPN}")

# cheia = SHA256(str(A × B))
encryption_key = sha256(str(cP).encode()).digest()

# AES-ECB + PKCS#7
cipher = AES.new(encryption_key, AES.MODE_ECB)
pad_len = 16 - (len(FLAG) % 16)
padded_flag = FLAG + bytes([pad_len] * pad_len)
print(f"[Merchant Of DOOM] Here's your jumbled up prize: {cipher.encrypt(padded_flag).hex()}")
```

## Soluție

Scopul este să decriptăm flag-ul criptat cu AES-ECB, unde cheia este derivată astfel:

key = SHA256(str(A × B))


### Observație cheie:

Dacă alegem un vector **B** care este **paralel** cu vectorul **A**, atunci produsul vectorial **A × B = (0, 0, 0)**.

În acest caz, cheia devine:

key = SHA256("(0, 0, 0)")


Aceasta este o valoare cunoscută pe care o putem folosi pentru a decripta flag-ul.

---

### Pași concreți:

1. Trimitem către server următorii vectori:
   - `B₁ = (1, 0, 0)`
   - `B₂ = (0, 1, 0)`
   - `B₃ = (0, 0, 1)`

2. Serverul returnează normele produselor vectoriale:
   - `n1 = ||A × B₁||² = a₂² + a₃²`
   - `n2 = ||A × B₂||² = a₁² + a₃²`
   - `n3 = ||A × B₃||² = a₁² + a₂²`

3. Rezolvăm sistemul:
    ```python
   a1_squared = (n2 + n3 - n1) // 2
   a2_squared = (n1 + n3 - n2) // 2
   a3_squared = (n1 + n2 - n3) // 2
   ```

4. Obținem valorile absolute ale componentelor lui A:
    ```python
    a1 = math.isqrt(a1_squared)
    a2 = math.isqrt(a2_squared)
    a3 = math.isqrt(a3_squared)
    ```

5. Construim un vector paralel cu A:
    ```python
    B = (abs(a1), abs(a2), abs(a3))
    ```

6. Trimitem acest vector B la server. Deoarece A × B = (0, 0, 0), cheia de criptare devine:
    ```python
    key = SHA256(b"(0, 0, 0)").digest()
    ```

7. Decriptăm flag-ul cu AES-ECB:
    ```python
    pt = AES.new(key, AES.MODE_ECB).decrypt(ciphertext)
    ```

8. Eliminăm padding-ul PKCS#7:
    ```python
    pad = pt[-1]
    flag = pt[:-pad]
    ```

# Flag

CTF{76b6e66355e0ae005021842c8082b9f3595aa04c7d574567ca73a37db5d1f790}