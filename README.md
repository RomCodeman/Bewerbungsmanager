# Bewerbungsmanager (Application Tracker)

## Das Ziel:
Webanwendung zur Verwaltung von Bewerbungen bei der Praktikums- und Jobsuche.

## Tech-Stack:
    
    | Bereich           | Technologie           |
    |   ---             |    ---                |
    | Frontend          | Angular               |
    | Backend           | Django                |
    | REST API          | Django REST Framework |
    | Datenbank         | SQLite                |
    | Kommunikation     | HTTP / JSON           |


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