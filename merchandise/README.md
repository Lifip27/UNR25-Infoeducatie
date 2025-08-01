# merchandise

## DESCRIERE

The Merchant of DOOM era un traficant de arme notoriu care își codifica tranzacțiile într-un mod neobișnuit, folosind vectori 3D pentru a ascunde informații. Scopul este să descifrăm cum funcționează codificarea și să recuperăm flag-ul criptat.

## Fișiere

- `chall.sage` – codul care simulează serverul
- `solve.py` – script pentru rezolvare

---

## Soluție

Scriptul oferit criptează un flag folosind AES în modul ECB. Cheia de criptare se obține astfel:

1. Serverul are un vector secret **A**.
2. Utilizatorul trimite un vector **B**.
3. Se calculează produsul vectorial A × B.
4. Se ia norma acestui produs și se arată utilizatorului.
5. Se formează cheia de criptare aplicând SHA-256 la stringul produsului vectorial.
6. Flag-ul este criptat cu AES-ECB folosind acea cheie.

### Obiectiv

Trebuie să trimitem un vector **B** astfel încât cheia folosită la criptare să fie cunoscută de noi.

### Observație

Dacă **A × B = (0, 0, 0)**, atunci cheia devine:  
`SHA256(str((0, 0, 0)))`, adică o valoare fixă pe care o știm.

Asta se întâmplă când vectorii **A** și **B** sunt paraleli.

### Cum găsim un vector B paralel cu A?

Nu știm vectorul A, dar putem să-l reconstruim aproximativ:

1. Trimitem 3 vectori:  
   - (1, 0, 0)  
   - (0, 1, 0)  
   - (0, 0, 1)

2. Serverul ne răspunde cu norma (lungimea) lui A × B pentru fiecare.

3. Din aceste 3 valori obținem 3 ecuații cu pătratele componentelor lui A:
a2^2 + a3^2 = norm1
a1^2 + a3^2 = norm2
a1^2 + a2^2 = norm3

4. Rezolvăm sistemul și obținem valorile absolute ale lui a1, a2 și a3.

5. Construim vectorul **B = (|a1|, |a2|, |a3|)**, care va fi paralel cu A.

6. Trimitem acest vector B – rezultatul va fi A × B = 0.

### Final

Dacă avem cheia cunoscută, putem decripta flag-ul cu AES-ECB și scoatem padding-ul la final.

---

## Flag

CTF{76b6e66355e0ae005021842c8082b9f3595aa04c7d574567ca73a37db5d1f790}