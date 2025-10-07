# 1E1 x Stichting Accessibility
Een MVC-CRUD applicatie voor beheerders, ervaringsdeskundigen, en organisaties van stichting accessibility.

## Groepsleden
- [Jeffrey](https://github.com/JeffreyDoornbos)
- [Jeremy](https://github.com/Jeremy-1052559)
- [Julie](https://github.com/Julie-1010439)
- [Freek](https://github.com/freek925)
- [Yoshua](https://github.com/yoshua-1045100)

## Installatie

***Let op**: Zorg ervoor dat je de naam van het meegeleverde env bestand verandert naar .env en dat je deze in de project folder plaatst naast deze README.*

***Let op**: Om de applicatie via PyCharm te starten, moet de working directory worden aangepast naar de hoofdmap van het project (de project folder) in plaats van de src-map. Als dit geen oplossing biedt, raden wij aan de onderstaande stappen te volgen en de applicatie via de CLI te starten.*

### 1: Installeer python
Ga naar [python.org/downloads/](https://www.python.org/downloads/) en download en installeer de laatste versie van python.

De applicatie is getest op versies 3.11 - 3.14

### 2: Maak de virtual environment aan
Nu dat python is geinstalleerd, open een command prompt en navigeer naar de project folder. Type dan het volgende commando:
```
python -m venv venv
```

### 3: Activeer de virtual environment
Voer nu (afhankelijk van het gebruikte bestuurings systeem) een van volgende commando's in:

**Windows**:
```
cd ./venv/Scripts && Activate.bat && cd ../../
```

**MacOS / Linux**
```
source venv/bin/activate
```

Om te verifieren of de venv is geactiveerd, probeer het volgende commando uit te voeren, het verwachte resultaat is dat alleen pip in de lijst voorkomt:
```
python -m pip list
```

### 4: Installeer de vereiste python packages
Om de benodige packages voor de applicatie te installeren, voer het volgende commando in:
```
python -m pip install -r requirements.txt
```

Om te verifieren dat alles geinstalleerd is, voer nogmaals het volgende commando uit en kijk in de lijst of alle vereisten voorkomen:
```
python -m pip list
```

### 5: Start de applicatie
Nu dat alles is voorbereid kan de applicatie opgestart worden, voer hiervoor het volgende commando in:
```
python src/app.py
```

De app is nu beschikbaar op: 
[localhost:5000](http://127.0.0.1:5000)

De documentatie voor de API is te vinden op:
[localhost:5000/apidocs/](http://127.0.0.1:5000/apidocs/)

---
## Inlog gegevens

* Beheerder: naam = beheer@hotmail.nl, wachtwoord = test321
* Ervaringsdeskundigen: naam = testing@hotmail.nl, wachtwoord = test321

* Wil je registreren? Dat kan maar de beheerder moet jou wel accepteren (jijzelf)

---

### Beheerders

---

### Ervaringsdeskundige
[Ervaringsdeskundigen guide](markdown_files/guide_ervaringsdeskundigen.md)

---

### Organisaties (API keys)

---

### Sources & references
[Bronnenlijst & verwijzingen](markdown_files/bronnenlijst.md)

---

### Credits 
* Programming: Team: 1E1
* Freek, Jeffrey, Jeremy, Julie, Yoshua
* Hogeschool Rotterdam: leraren, lessen, powerpoints, workshops & opdrachten

---
