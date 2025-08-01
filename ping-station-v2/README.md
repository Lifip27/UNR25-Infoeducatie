# ping-station-v2

## Descriere

Scopul este să identificăm și să exploatăm o vulnerabilitate în aplicația web furnizată pentru a extrage conținutul fișierului `flag.txt`.

## Serviciu

- Aplicație web care oferă un câmp de text pentru a da `ping` către o adresă IP
- Fișier furnizat: capturi de ecran (`poza1.png`, `poza2.png`, etc.)

## Analiză

Deschizând interfața aplicației (`poza1.png`), observăm că putem introduce o adresă IP și trimite o comandă `ping`.

Acest tip de funcționalitate este adesea vulnerabil la **command injection**, dacă inputul nu este validat corespunzător.

### Testare

Am început prin a introduce caractere speciale pentru a evalua comportamentul aplicației:

- `;`, `+`, `\` — testate fără succes
- Caracterele `|` s-au dovedit funcționale (`poza2.png`)

Exemplu de comandă care a funcționat:

192.168.1.1|ls

Aceasta ne permite să listăm fișierele din directorul curent și confirmă prezența unui vector de command injection (`poza3.png`).

## Exploatare

Pentru a citi fișierul `flag.txt`, folosim comanda:

192.168.1.1|cat${IFS}flag.txt

Explicație:

- `${IFS}` este o variabilă shell care reprezintă caracterul "space" (spațiu), utilă pentru evitarea filtrelor rudimentare.

Rezultatul afișat conține flag-ul (`poza4.png`).

## Flag

this-will-be-dynamic