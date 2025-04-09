# transit-route-planner
## Projektbeschreibung
Dieses Python-Projekt berechnet die Reisedauer und die Anzahl der Umstiege für Schüler auf dem Weg zu verschiedenen Schulen. Es verwendet die Google Maps Directions API, um Reisedaten (Dauer und Umstiege) auf Grundlage der Adressen der Schüler und Schulen abzurufen. Die Ergebnisse werden in mehreren Ausgabeformaten (CSV, JSON) gespeichert, um sie weiter analysieren oder verarbeiten zu können.

## Projektstruktur
```graphql
├── input/
│   ├── schools.csv        # CSV-Datei mit den Schulen und deren Adressen
│   ├── students.csv       # CSV-Datei mit den Schülern und deren Adressen
├── output/                # Ordner für die Ergebnisdateien
│   ├── output.csv         # Ergebnisse in CSV-Format
│   ├── output.json        # Ergebnisse in JSON-Format
│   ├── response.json      # Caching der API-Antworten
├── utils/                 # Hilfsdateien für API-Anfragen und Dateimanagement
│   ├── api_handler.py     # Verarbeitet API-Anfragen und Antworten
│   ├── config_loader.py   # Lädt die Konfigurationsdatei
│   ├── file_handler.py    # Speichert die Ergebnisse in verschiedenen Formaten
├── main.py                # Hauptskript, das die API-Anfragen ausführt und die Ergebnisse speichert
├── requirements.txt       # Python-Abhängigkeiten
├── config.ini             # Konfigurationsdatei für das Projekt
```
## Anforderungen
- Python 3.x
- Installierte Python-Bibliotheken:
    - requests für API-Anfragen
    - pandas für die Verarbeitung der CSV-Dateien

Führen Sie den folgenden Befehl aus, um die Anforderungen zu installieren:

```bash
pip install -r requirements.txt
```

## Virtuelle Umgebung (optional)
Es wird empfohlen, eine virtuelle Umgebung (venv) zu erstellen, um die Abhängigkeiten isoliert zu installieren. Dies kann wie folgt erfolgen:

```bash
python -m venv venv
source venv/bin/activate  # Für Linux/MacOS
venv\Scripts\activate     # Für Windows
```
Installieren Sie dann die benötigten Bibliotheken:
```bash
pip install -r requirements.txt
```

## Konfigurationsdatei (config.ini)
Die Konfiguration wird in der Datei ``config.ini`` gespeichert. Diese Datei sollte folgende Struktur haben:

```ini
[GENERAL]
datetime = 2025-04-10T08:00:00   # Das Datum und die Uhrzeit, zu der die Ankunft geplant ist

[FILES]
students_csv = input/students.csv    # Pfad zur Schüler-CSV-Datei
schools_csv = input/schools.csv      # Pfad zur Schulen-CSV-Datei
output_folder = output               # Ordner, in dem die Ausgabedateien gespeichert werden

[API]
api_key = YOUR_GOOGLE_API_KEY       # API-Schlüssel für Google Maps Directions API
```

## Verwendung
### Eingabedateien
1. ``schools.csv``
    
    Enthält die Liste der Schulen mit ihrer einzigartigen ``school_id`` und der ``address``.

    ```ini
    school_id;address
    0001;Hauptstraße 1, 12345 Berlin
    0002;Dorfplatz 2, 12345 Berlin
    0003;Marktplatz 3, 12345 Berlin
    ```
2. ``students.csv```
    
    Enthält die Liste der Schüler mit ihrer einzigartigen ``student_id`` und der ``address``.

    ```ini
    student_id;address
    123456;Marktplatz 1, 12345
    123457;Dorfplatz 2, 12345
    ```
### Utility-Skripte
- ``api_handler.py``: Verwaltet Anfragen an die Google Maps Directions API und ruft Reisedaten (Dauer und Umstiege) zwischen den Adressen der Schüler und Schulen ab.

- ``config_loader.py``: Lädt die Konfiguration aus einer INI-Datei, einschließlich Pfaden für Eingabedateien, API-Schlüsseln und Ausgabeverzeichnissen.

- ``file_handler.py``: Verantwortlich für das Speichern der Ergebnisse in CSV- und JSON-Formaten. Es fügt Daten zu den Ausgabedateien hinzu oder erstellt neue, falls sie nicht existieren.

### Hauptskript
``main.py``: Das Hauptskript, das:
- Die Konfiguration und Eingabedateien lädt.
- Die Schüler- und Schul-Daten durchläuft, um Reisedaten von der API abzufragen.
- Die Ergebnisse in output.csv, output.json und response.json speichert.


Stelle sicher, dass die erforderlichen Eingabedateien (``students.csv``, ``schools.csv``) im Arbeitsverzeichnis vorhanden sind.

Erstelle oder bearbeite die ``config.ini``-Datei mit der notwendigen Konfiguration (API-Schlüssel, Dateipfade usw.).

Führe das Skript main.py aus:

```bash
python main.py
```

### Ausgabedateien
- ``output.csv``: Die primäre Ausgabedatei, die die Reisedauer und die Anzahl der Umstiege für jeden Schüler und jede Schule enthält.

- ``output.json``: Ein alternatives Ausgabeformat, das eine strukturierte JSON-Darstellung der Daten enthält.
- ``response.json``: Caching der rohen API-Antworten, um wiederholte Anfragen zu vermeiden und das Debuggen zu erleichtern.

## Dateibeschreibungen
- ``config.ini``: Konfigurationsdatei für den API-Schlüssel, Dateipfade und das Datum für API-Anfragen.`

- ``students.csv``: Enthält Schülerdaten (student_id, address).

- ``schools.csv``: Enthält Schulendaten (school_id, address).

- ``output.csv``: Speichert die Ergebnisse im CSV-Format (student_id, school_id, travel duration, transfers).

- ``output.json``: Speichert die Ergebnisse im JSON-Format.

- ``response.json``: Cacht die API-Antworten, um wiederholte API-Anfragen zu vermeiden.

## Beispielausführung
Nach der Ausführung des Skripts werden die Ergebnisse in den folgenden Dateien gespeichert:

- ``output.csv:``
    ```python-repl
    student_id;address;0531_duration;0531_transfers;0758_duration;0758_transfers;0688_duration;0688_transfers
    9543708;Aachener Strasse 13, 80804;45;1;55;2;30;1
    9246033;Abbachstraße 20, 80992;50;2;60;3;35;1
    5972663;Adam-Berg-Str. 184A, 81735;60;1;70;2;40;1
    ...
    ```

- ``output.json``:
    ```json
    {
    "123456": {
        "address": "Marktplatz 1, 12345",
        "schools": {
        "0001": {
            "duration": 45,
            "transfers": 1
        },
        "0002": {
            "duration": 55,
            "transfers": 2
        },
        "0003": {
            "duration": 30,
            "transfers": 1
        }
        }
    },
    "123457": {
        "address": "Dorfplatz 2, 12345",
        "schools": {
        "0001": {
            "duration": 50,
            "transfers": 2
        },
        "0002": {
            "duration": 60,
            "transfers": 3
        },
        "0003": {
            "duration": 35,
            "transfers": 1
        }
        }
    },
    ...
    }
    ```


- ``response.json``: Enthält die zwischengespeicherten API-Antworten, um wiederholte API-Aufrufe zu minimieren.

## Lizenz
Dieses Projekt ist unter der Apache 2.0-Lizenz lizenziert - siehe die LICENSE-Datei für Details.