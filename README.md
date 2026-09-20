# Bewerbungsmanager (Application Tracker)

## Das Ziel:

Der Bewerbung Tracker soll dabei helfen, Bewerbungen zentral zu verwalten und den aktuellen Stand jeder Bewerbung schnell zu erkennen.

Statt Informationen zu Bewerbungen über Notizen, Tabellen oder verschiedene Dateien zu verteilen, sollen die wichtigsten Daten an einem Ort strukturiert gespeichert werden.

## Hauptworkflow

    Unternehmen anlegen
            ↓
    Bewerbung erstellen
            ↓
    Status verfolgen
            ↓
    Bewerbung aktualisieren
            ↓
    nächste Aktion / Ergebnis

## Tech-Stack:
    
    | Bereich           | Technologie           |
    |   ---             |    ---                |
    | Frontend          | Angular               |
    | Backend           | Django                |
    | REST API          | Django REST Framework |
    | Datenbank         | SQLite                |
    | Kommunikation     | HTTP / JSON           |

## Geplante MVP-Funktionen

    1. Unternehmen erstellen
    2. Unternehmen (eine Liste) anzeigen
    3. Unternehmen bearbeiten
    4. Unternehmen löschen

    5. Bewerbung erstellen
    6. Bewerbung einer Firma zuordnen
    7. Bewerbungen anzeigen
    8. Status ändern
    9. Bewerbung bearbeiten
    10. Bewerbung löschen




### Unternehmen

- Unternehmen anlegen
- Unternehmen anzeigen
- Unternehmen bearbeiten
- Unternehmen löschen

### Bewerbung

- Bewerbung anlegen
- Bewerbung einem Unternehmen zuordnen
- Bewerbung anzeigen
- Bewerbung bearbeiten
- Bewerbung löschen
- Bewerbungsstatus verwalten

### Bewerbungsstatus

- Geplant
- Beworben
- Interview
- Zusage
- Absage

### Dashboard Beispiel

    Bewerbungen insgesamt: 18
    
    Geplant       3
    Beworben      8
    Interview     2
    Zusage        1
    Absage        4

## Datenmodel
...

## Systemarchitektur

```mermaid
flowchart TD
    F[Angular Frontend]
    API[Django REST Framework]
    D[Django]
    DB[(SQLite)]

    F -->|HTTP / JSON| API
    API --> D
    D -->|Django ORM| DB



    