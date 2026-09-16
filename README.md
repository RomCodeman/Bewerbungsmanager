# Bewerbungsmanager (Application Tracker)

## Das Ziel:

Der Bewerbung Tracker soll dabei helfen, Bewerbungen zentral zu verwalten und den aktuellen Stand jeder Bewerbung schnell zu erkennen.

Statt Informationen zu Bewerbungen über Notizen, Tabellen oder verschiedene Dateien zu verteilen, sollen die wichtigsten Daten an einem Ort strukturiert gespeichert werden.

## Tech-Stack:
    
    | Bereich           | Technologie           |
    |   ---             |    ---                |
    | Frontend          | Angular               |
    | Backend           | Django                |
    | REST API          | Django REST Framework |
    | Datenbank         | SQLite                |
    | Kommunikation     | HTTP / JSON           |

## Geplante MVP-Funktionen

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