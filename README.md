# RC Client

Ce dépôt contient un client UDP servant a controller le PiCar de SunFounder avec une manette DualShock 4.

## Pré-requis

 - Python 3
 - Pygame
 - Manette DualShock 4

## Installation

1. Clonez de dépôt
2. Dans le dossier `settings`, copiez le fichier `dev.sample.json` et nommez la copie `dev.json`
3. Dans le fichier `dev.json`, modifiez `"<SERVER IP>"` pour l'adress ip du raspberry py

## Utilisation

Pour lancer le client, vous devez executer la commande suivante.
Vous devez avoir un manette DualShock 4 connectée.

Windows:
```powershell
python .\main.py
```

Linux:
```powershell
python3 ./main.py
```