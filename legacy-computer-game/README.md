# legacy-computer-game

## Descriere

În timp ce răsfoiam lucrurile vechi ale bunicului meu, am descoperit un joc pe calculator interesant. Din păcate, era criptat, dar am reușit să obțin codul sursă al procesului. Scopul este de a recupera flag-ul criptat.

## Fișiere

- `output.txt`
- `source.py`

## Soluție

Ni se oferă un script Python care implementează un sistem criptografic propriu. Se generează un număr prim mare `p` și un secret care este și el un prim de 1024 biți. Apoi:

- Se calculează `private = (g * secret) % p`, unde `g = 2`
- Se calculează `public = pow(private, 2, p)`
- Flag-ul este XOR-at cu `secret % p`
- Rezultatul este trecut de trei ori printr-un generator liniar congruent (LCG)

Valorile obținute la fiecare pas al LCG-ului sunt afișate ca:

- `flag_1`
- `flag_2`
- `flag_3`

Având aceste trei ieșiri consecutive ale LCG-ului, putem determina parametrii `a` și `c` folosind relațiile matematice dintre termeni consecutivi dintr-o secvență generată de LCG.

Odată obținuți `a` și `c`, putem inversa LCG-ul și determina valoarea inițială `f0`, adică flag-ul XOR-at cu `secret % p`.

Având și valoarea `public`, putem calcula `secret % p` astfel:

- Știm că `public = (g * secret)^2 % p`
- Rezultă că `(secret % p)^2 = public * inverse(4, p) % p`

Calculăm radicalul modular pentru a obține cele două posibile valori pentru `secret % p`. Aplicând XOR între fiecare variantă de `s` și `f0`, obținem două variante posibile pentru flag. Le convertim în bytes și verificăm care este validă.

## Flag

CTF{f5f987eb589797a98c0234cf4dbad05351e979ef41cf6beed2c46eb029e731e7}