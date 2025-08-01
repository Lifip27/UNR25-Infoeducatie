# Ce este Ingineria Inversă?

![chall](poza.png)

## DESCRIPTION

"Reverse Engineering" (sau **Ingineria Inversă**) este ca o detectivistică tehnologică: în loc să ai instrucțiunile de construcție ale unui dispozitiv, primești produsul finit și încerci să înțelegi cum funcționează. În acest challenge, vom desfășura două fișiere executabile pentru a descoperi parole ascunse.

---

## Fișiere

- `1.exe`
- `2.exe`

## Unelte recomandate

În ingineria inversă, uneltele potrivite sunt esențiale. Cele mai comune includ:
- `strings`
- `Ghidra`
- `IDA Pro`
- `x64dbg`
- `CyberChef`
- `pwndbg` / `gdb`

---

![challs](poza2.png)

## Q1. Care este parola cu care ati primit mesajul "Access granted" ruland fisierul 1.exe?

Mai intai sa incercam sa vedem daca fisierul are ceva strings "hardcoded".

![ex1](poza3.png)

Am gasit parola folosing un tool super user de folosit:
```bash
strings 1.exe | grep password
```
Ce fac aceste comenzi?

```bash
strings 1.exe
```

Va enumera toate "strings" din acel fisier.

```bash
grep password
```
Va filtra doar cele care contin "password"

O alta methoda prin care putem gasi parola este sa o deschidem intr-un decompiler.

![rev](poza4.png)

Si gasim parola dinnou.

##### Flag: secret-password-124

## Q2. Trecem la nivelul urmator. Care este parola cu care ati primit mesajul "Access granted" ruland fisierul 2.exe?

De data aceasta daca incercam sa folosim methoda "strings" nu vom gasi parola asadar continuam cu decompilerul.

![rev2](poza5.png)

Putem vedea stringul " ;'gax#4x3<xdffb" dar daca incercam vom primi Access Denied.

![denied](poza7.png)

Bun, atunci ar trebui sa recitim codul main ca sa intelegem.

1. Ne salveaza input-ul in variabila v6.
```bash
scanf("%s", v6);
```

2. Copiaza acel string din dreapta in variabila Str2.
```bash
strcpy(Str2, " ;'gax#4x3<xdffb");
```

3. Variabila v3 este egala cu rezultatul din functia hash cu inputul variabilei v6. 
```bash
v3 = hash(v6);
```

Functia hash:

![hash](poza6.png)

Aceasta functie este o functie de XOR cu byte-ul 0x55.
Adica ia cate un character din variabila Str2 si ii face un calcul matematic prin al descifra.
Pentru a da reverse la aceasta functie putem sa intram pe site-ul:[https://gchq.github.io/CyberChef/](https://gchq.github.io/CyberChef/)

![cyberchef](poza8.png)

Reiese parola unr24-va-fi-1337.
Putem sa verificam asta:

![access](poza9.png)

##### Flag: unr24-va-fi-1337

