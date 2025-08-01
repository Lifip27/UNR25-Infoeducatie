# gaming-habbits

## Descriere

Betaflash trebuie să își întâlnească prietenul la o casă verde din imagine. Este necesar să identificăm numele orașului, coordonatele pătratului de pe hartă și regiunea cardinală, pentru a-l putea ghida până acolo.

Formatul cerut pentru flag este:  
`CTF{sha256(city_name(x.xx:x.xx)SE)}`

## Fișier

- `gaming-habbits.png`

## Soluție

Deschizând imaginea, se observă că provine din jocul **DayZ**. Se poate folosi harta interactivă disponibilă la adresa:

- [https://dayz.xam.nu](https://dayz.xam.nu)

Cu ajutorul analizei și confirmării, s-a stabilit că locația casei verzi se află în satul `Dobroye`.

Pe hartă, casa este localizată în pătratul cu coordonatele `(1.29:0.03)` și se află în zona `NE`.

Formatul complet devine:

Dobroye(1.29:0.03)NE


Această valoare este hash-uită cu algoritmul SHA-256. S-a folosit site-ul:

- [https://emn178.github.io/online-tools/sha256.html](https://emn178.github.io/online-tools/sha256.html)

pentru a genera hash-ul.

## Flag

CTF{6acfb96047869efed819b66c2bab15565698d8295ca78d7d4859a94873dcc5ce}