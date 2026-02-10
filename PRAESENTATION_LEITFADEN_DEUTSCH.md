# CityBike Analytics Platform
## Präsentationsleitfaden für Klasse

**Geschätzter Präsentationszeit:** 15-20 Minuten

---

## FOLIE 1: Titelfolie

**Titel:** CityBike Analytics Platform - Bike-Sharing Datenanalyse

**Untertitel:** Ein Python-Projekt, das OOP, Designmuster und Data Science demonstriert

**Ihr Name:**  
**Datum:** 10. Februar 2026  
**Repository:** github.com/mutabazi105/citybike-capstone

---

## FOLIE 2: Projektübersicht (1 Min)

**Was ist CityBike?**
- Analysesystem für einen Bike-Sharing-Service
- Analysiert 100+ Fahrten über 10 Stationen
- Generiert Erkenntnisse über Nutzungsmuster

**Wichtigste Leistungen:**
✅ 9 Python-Module (3.500+ Zeilen Code)  
✅ 14 geschäftliche Analysefragen  
✅ 10+ professionelle Visualisierungen  
✅ Benutzerdefinierte Algorithmen mit Leistungsanalyse

**Sprechpunkte:**
- "Dieses Projekt zeigt, wie echte Datenanalyse funktioniert"
- "Wir verarbeiten Rohdaten durch eine komplette Pipeline"
- "Von der Belastung bis zu Visualisierungen in einem System"

---

## FOLIE 3: Problemstellung (1 Min)

**Die Herausforderung:**
Ein Bike-Sharing-Unternehmen muss:
- Verstehen, welche Stationen am beliebtesten sind
- Spitzenlastzeiten identifizieren
- Wartungskosten verfolgen
- Den Service basierend auf Daten verbessern

**Warum ist das wichtig:**
- Optimieren Sie die Fahrradplatzierung
- Planen Sie Wartungspläne
- Nachfrage vorhersagen
- Datengesteuerte Entscheidungen treffen

**Sprechpunkte:**
- "Viele Unternehmen sind mit ähnlichen Herausforderungen konfrontiert"
- "Dieses Projekt demonstriert echte Problemlösung"
- "Von Daten bis zu umsetzbaren Erkenntnissen"

---

## FOLIE 4: Architekturübersicht (1 Min)

**Systemdesign:**

```
┌─────────────────────────────┐
│   Dateneingabepunkt        │
│   (CitibikeMain.py)        │
└──────────────┬──────────────┘
               │
      ┌────────┼────────┐
      ▼        ▼        ▼
   ┌──────┐ ┌──────┐ ┌──────────┐
   │Models│ │Parser│ │Factories │
   └──────┘ └──────┘ └──────────┘
      │        │        │
      └────────┼────────┘
               ▼
         ┌──────────┐
         │Analyzer  │ ← 14 Fragen
         └──────────┘
         │  │  │  │
    ┌────┴──┴──┴──┴────┐
    ▼  ▼  ▼  ▼  ▼  ▼  ▼
```

**Sprechpunkte:**
- "System ist in Schichten organisiert"
- "Jedes Modul hat klare Verantwortung"
- "Einfach zu pflegen und zu erweitern"
- "Zeigt professionelles Softwaredesign"

---

## FOLIE 5: Schlüsseltechnologien (1 Min)

**Programmierwerkzeuge:**

| Technologie | Zweck |
|-----------|---------|
| **Python 3.8+** | Kernsprache |
| **Pandas** | Datenbelastung & Bereinigung |
| **NumPy** | Statistische Berechnung |
| **Matplotlib** | Datenvisualisierung |
| **Git** | Versionskontrolle |

**Warum diese?**
- Industriestandard für Data Science
- Leistungsstarke Analysebibliotheken
- Einfach zu erlernen und zu verwenden
- Breite Community-Unterstützung

**Sprechpunkte:**
- "Das sind die Tools, die Datenwissenschaftler weltweit verwenden"
- "Zeigt, dass ich den modernen Tech Stack verstehe"
- "Perfekt für Datenanalyseprojekte"

---

## FOLIE 6: Modul 1 - Modelle (2 Min)

**Zweck:** Geschäftsentitäten definieren

**Wichtigste Klassen:**

```
Entity (Abstrakt)
  ├── Bike
  │   ├── ClassicBike
  │   └── ElectricBike
  │
  ├── User
  │   ├── CasualUser
  │   └── MemberUser
  │
  ├── Station
  ├── Trip
  └── MaintenanceRecord
```

**Merkmale:**
- ✅ Vererbung (DRY-Prinzip)
- ✅ Kapselung (Eigenschaften)
- ✅ Validierung (Fehlerprüfung)
- ✅ Typhinweise

**Code-Beispiel:**
```python
bike.is_available = False  # ✓ Funktioniert
bike.bike_id = -1          # ✗ Fehler (Validierung!)
```

**Sprechpunkte:**
- "Verwendet OOP zur Modellierung echter Konzepte"
- "Jede Klasse stellt etwas aus der Bike-Sharing-Welt dar"
- "Validierung gewährleistet Datenqualität"
- "Vererbung reduziert Codeduplizierung"

---

## FOLIE 7: Modul 2 - Fabriken (1 Min)

**Zweck:** Objekte flexibel erstellen

**Factory Pattern:**

```python
# Ohne Factory (schlecht)
if type == "classic":
    bike = ClassicBike(...)
elif type == "electric":
    bike = ElectricBike(...)

# Mit Factory (gut)
bike = create_bike("classic", ...)
```

**Vorteile:**
- ✅ Zentralisierte Erstellungslogik
- ✅ Einfach zu ändern
- ✅ Keine Codeduplizierung
- ✅ Professionelles Designmuster

**Sprechpunkte:**
- "Designmuster sind wiederverwendbare Lösungen"
- "Factory Pattern wird in großen Frameworks verwendet"
- "Zeigt, dass ich Softwaredesign verstehe"

---

## FOLIE 8: Modul 3 - Analytik (2 Min)

**Zweck:** 14 Geschäftsfragen beantworten

**Die 14 Fragen:**

```
1. Gesamtfahrten, Strecke, Durchschnittsdauer
2. Beliebteste Startstation
3. Spitzenlastzeiten während des Tages
4. Geschäftigster Wochentag
5. Durchschnittliche Strecke nach Benutzertyp
6. Fahrradauslastungsquote
7. Ridership-Trend monatlich
8. Top 15 aktive Benutzer
9. Wartungskosten nach Fahrradtyp
10. Beliebte Routen (von-zu Paare)
11. Trip-Abschlussquote
12. Durchschnittliche Fahrten pro Benutzer
13. Fahrräder mit hoher Wartungshäufigkeit
14. Ausreißer-Fahrten (ungewöhnliche Muster)
```

**Beispiel Q2 Ergebnisse:**
```
Top Stationen:
1. Harbor View       - 14 Fahrten
2. West End         - 14 Fahrten
3. University Campus - 12 Fahrten
```

**Sprechpunkte:**
- "Echte Geschäftsfragen brauchen Antworten"
- "Data Science geht um Erkenntnisse"
- "Jede Frage treibt Geschäftsentscheidungen"
- "System automatisiert komplexe Analysen"

---

## FOLIE 9: Modul 4 - Algorithmen (2 Min)

**Zweck:** Sortieren und Suchen mit Big-O-Analyse

**Implementierungen:**

```
Sortierung:
  • Merge Sort   - O(n log n) stabil
  • Quick Sort   - O(n log n) Durchschnitt
  • Bubble Sort  - O(n²) einfach

Suche:
  • Binary Search - O(log n) schnell
  • Linear Search - O(n) flexibel
```

**Benchmark-Ergebnisse:**
```
Sortierung 1000 Nummern:
  Python Builtin  → 0.2 ms  ✓ Schnellste
  Quick Sort      → 4.3 ms
  Merge Sort      → 4.8 ms
  Bubble Sort     → 128 ms  ✗ Langsamste
```

**Sprechpunkte:**
- "Algorithmische Analyse ist entscheidend in CS"
- "Big-O-Notation zeigt Skalierbarkeit"
- "Verschiedene Algorithmen für verschiedene Bedürfnisse"
- "Benchmarking beweist Leistung"

---

## FOLIE 10: Modul 5 - NumPy (1 Min)

**Zweck:** Statistische Berechnung mit NumPy

**Berechnete Statistiken:**

```
Für Trip-Dauer:
  • Mittelwert: 58,25 Minuten
  • Median: 53,00 Minuten
  • Std Abw: 34,48 Minuten
  • Min: 5 Min, Max: 119 Minuten
  • Q1: 31,75, Q3: 88,50

Für Trip-Strecke:
  • Mittelwert: 5,71 km
  • Median: 5,96 km
  • Bereich: 0,50 - 9,98 km
```

**Erweiterte Funktionen:**
- Ausreißer-Erkennung (Z-Score, IQR)
- Entfernungsberechnung
- Vektorisierte Operationen (schnell!)

**Sprechpunkte:**
- "NumPy macht Analysen 1000x schneller"
- "Vektorisierung vs. Schleifen"
- "Professioneller Data-Science-Ansatz"

---

## FOLIE 11: Modul 6 - Preisstrategie (1 Min)

**Zweck:** Verschiedene Preismodelle mit Strategy Pattern

**Preisoptionen:**

```
Casual User:      €0,30/Minute (Pay-per-Ride)
Member User:      €0,18/Minute + 45 Minuten kostenlos
Peak Hour:        +50% Aufschlag (8-9 Uhr, 17-19 Uhr)
Distanz-basiert:  €0,80/Kilometer
```

**Berechnungsbeispiel:**
```
Trip: 50 Minuten, Member User
  Basispreis: €0,18 × 50 = €9,00
  Kostenloser Freibetrag: 45 Minuten
  Abrechenbar: 5 Minuten
  Endpreis: €0,90
```

**Strategy Pattern Vorteile:**
- ✅ Neue Preisgestaltung ohne Code-Änderung
- ✅ Einfach zwischen Strategien wechseln
- ✅ Professionelles Designmuster

**Sprechpunkte:**
- "Echte Geschäfte haben komplexe Preisgestaltung"
- "Strategy Pattern macht es flexibel"
- "Einfach verschiedene Geschäftsmodelle testen"

---

## FOLIE 12: Modul 7 - Visualisierungen (1 Min)

**10+ Professionelle Diagramme:**

```
1. Top Stationen (Bar)
2. Monatlicher Trend (Linie)
3. Dauerverlauf (Histogramm)
4. Streckenverlauf (Histogramm)
5. Benutzertyp-Vergleich (Box Plot)
6. Fahrradtyp-Vergleich (Box Plot)
7. Trip-Status (Pie)
8. Wartungskosten (Bar)
9. Wartungstypen (Bar)
10. Stündliches Nutzungsmuster (Linie)
```

**Diagramm-Eigenschaften:**
- ✅ Professionelle Formatierung
- ✅ Richtige Beschriftungen & Legenden
- ✅ Hochauflösendes PNG
- ✅ Präsentationsreif

**Sprechpunkte:**
- "Datenvisualisierung erzählt die Geschichte"
- "Diagramme zeigen Muster, die Zahlen verbergen"
- "Alle Diagramme sind veröffentlichungsreif"
- [Demo: Zeigen Sie 2-3 Diagramme aus output/figures/]

---

## FOLIE 13: Datenpipeline (1 Min)

**Kompletter Arbeitsablauf:**

```
Schritt 1: Daten laden
  ↓
Schritt 2: Bereinigung & Validierung
  ↓
Schritt 3: Gereinigte Daten exportieren
  ↓
Schritt 4: Numerische Analyse
  ↓
Schritt 5: Algorithmus-Benchmarks
  ↓
Schritt 6: Geschäftliche Analytik
  ↓
Schritt 7: Visualisierungen
  ↓
Schritt 8: Berichte generieren
```

**Was jeder Schritt macht:**
- Laden: CSV-Dateien lesen
- Bereinigen: Fehler, Duplikate entfernen
- Analysieren: Fragen beantworten
- Visualisieren: Diagramme erstellen
- Bericht: Ergebnisse exportieren

**Sprechpunkte:**
- "Pipeline gewährleistet Konsistenz"
- "Automatisierter Prozess"
- "Kann wiederholt ausgeführt werden"
- "Echter Produktions-Arbeitsablauf"

---

## FOLIE 14: Demo - Projekt ausführen (2 Min)

**Live-Demo (oder Konsolenausgabe anzeigen):**

```bash
$ python -m citybike.main

======================================================================
              CITYBIKE BIKE-SHARING ANALYTICS PLATFORM
======================================================================

Gestartet: 2026-02-10 10:08:54

► Schritt 1: System initialisieren
✓ BikeShareSystem initialisiert

► Schritt 2: Rohdaten laden
✓ Daten erfolgreich geladen
  Fahrten: 100 Datensätze
  Stationen: 10 Datensätze
  Wartung: 30 Datensätze

[... fortsetzung ...]

► Schritt 8: Visualisierungen generieren
✓ 10 Diagramme erfolgreich erstellt

======================================================================
                   ANALYTICS PIPELINE ABGESCHLOSSEN ✓
======================================================================

Generierte Dateien:
  • output/figures/ (10 PNG-Diagramme)
  • output/summary_report.txt
  • output/top_users.csv
  • output/top_routes.csv
```

**Ergebnisse anzeigen:**
- 📊 Auf Diagramm-Ordner zeigen
- 📝 Zusammenfassungsbericht anzeigen
- 📋 CSV-Exporte anzeigen

**Sprechpunkte:**
- "Projekt läuft in Sekunden"
- "Alle Ausgaben werden automatisch generiert"
- "Alles wird zur späteren Verwendung gespeichert"

---

## FOLIE 15: Wichtigste Merkmale Zusammenfassung (1 Min)

**Was macht dieses Projekt großartig:**

✅ **Objektorientierte Programmierung**
   - Klassen mit Vererbung
   - Polymorphismus, Kapselung

✅ **Designmuster**
   - Factory Pattern
   - Strategy Pattern
   - Gut organisierte Architektur

✅ **Data Science**
   - Pandas für Datenmanipulation
   - NumPy für statistische Analyse
   - 14 geschäftliche Erkenntnisse

✅ **Professioneller Code**
   - Umfangreiche Dokumentation
   - Typhinweise durchgehend
   - Sauberer, lesbarer Code
   - Git-Versionskontrolle

---

## FOLIE 16: Lernergebnisse (1 Min)

**Was ich beim Aufbau dieses Projekts gelernt habe:**

1. **OOP-Prinzipien**
   - Vererbung, Polymorphismus, Kapselung
   - Abstrakte Basisklassen
   - Property-Dekoratoren

2. **Designmuster**
   - Factory Pattern für Flexibilität
   - Strategy Pattern für Algorithmen
   - Wann und warum jedes zu verwenden

3. **Data-Science-Arbeitsablauf**
   - Laden und Bereinigen von Daten
   - Statistische Analyse
   - Datenvisualisierung

4. **Benutzerdefinierte Algorithmen**
   - Implementierung von Grund auf
   - Big-O-Komplexitätsanalyse
   - Leistungsoptimierung

5. **Professionelle Praktiken**
   - Code-Organisation
   - Dokumentation
   - Versionskontrolle
   - Testen

---

## FOLIE 17: Herausforderungen & Lösungen (1 Min)

**Herausforderung 1: Datenqualität**
- Problem: Fehlende Werte, Duplikate, ungültige Formate
- Lösung: Umfassende DataCleaner-Klasse

**Herausforderung 2: Komplexe Analyse**
- Problem: 14 verschiedene Abfragen auf gleiche Daten
- Lösung: BikeShareSystem-Orchestrator

**Herausforderung 3: Leistung**
- Problem: Langsame Berechnungen bei großen Datensätzen
- Lösung: NumPy-Vektorisierung

**Herausforderung 4: Code-Organisation**
- Problem: Zu viele Verantwortungen in einer Datei
- Lösung: Trennung von Modulen nach Zweck

**Sprechpunkte:**
- "Echte Projekte haben echte Herausforderungen"
- "Professionelle Lösungen zu Problemen"
- "Iterative Verbesserungsmentalität"

---

## FOLIE 18: Projektstatistiken (1 Min)

**Nach den Zahlen:**

```
Code:
  • 3.500+ Produktionszeilen
  • 9 Module
  • 25+ Klassen
  • 100+ Methoden
  • Typhinweise auf alle Funktionen

Dokumentation:
  • Umfangreiche Docstrings
  • Inline-Kommentare
  • README mit Beispielen
  • 50-seitiger Designleitfaden

Daten:
  • 100 Trip-Datensätze
  • 10 Stationen
  • 30 Wartungsdatensätze
  • 14 Analysefragen
  • 10+ Visualisierungen

Versionskontrolle:
  • 20 Git-Commits
  • Aussagekräftige Commit-Nachrichten
  • Komplette Commit-Chronologie
```

---

## FOLIE 19: GitHub-Repository (1 Min)

**Projekt auf GitHub:**

Repository: https://github.com/mutabazi105/citybike-capstone

**Was ist enthalten:**
- ✅ Vollständiger Quellcode
- ✅ Komplette Dokumentation
- ✅ Beispieldatendateien
- ✅ Beispielausgaben
- ✅ Anweisungen zum Ausführen

**Wie zugreifen:**
1. Besuchen Sie das Repository
2. Klicken Sie auf "Code" → "ZIP herunterladen"
3. Oder: `git clone https://github.com/mutabazi105/citybike-capstone.git`
4. README-Anweisungen befolgen

**Sprechpunkte:**
- "Professionelles Portfolio-Projekt"
- "Bereit für Arbeitgeber zur Überprüfung"
- "Zeigt echte Entwicklungsfähigkeiten"

---

## FOLIE 20: Zukünftige Verbesserungen (1 Min)

**Mögliche Verbesserungen:**

```
📊 Mehr Analytik:
  • Vorhersagemodellierung
  • Nachfrageprognose
  • Anomalieerkennung

🔧 Merkmale:
  • Web-Dashboard
  • Echtzeitp-Updates
  • Benutzeroberfläche

📈 Skalierbarkeit:
  • Millionen Fahrten verarbeiten
  • Mehrere Städte
  • Echter Datenbankbackend

🤖 Erweitert:
  • Machine Learning Modelle
  • Empfehlungsmaschine
  • Mobile App
```

**Sprechpunkte:**
- "Projekt ist erweiterbar"
- "Grundlage für größere Systeme"
- "Zeigt Architektur-Skalierbarkeit"

---

## FOLIE 21: Fazit (1 Min)

**Zusammenfassung:**

**CityBike Analytics Platform demonstriert:**

✅ Starkes Verständnis von **Objektorientierter Programmierung**  
✅ Wissen über **Softwaredesign-Muster**  
✅ Praktische **Data-Science** Fähigkeiten  
✅ **Algorithmus** Implementierung und Analyse  
✅ **Professionelle Softwareentwicklung** Praktiken  

**Wichtigste Erkenntnisse:**
"Dieses Projekt zeigt, wie man ein echtes Datenanalysesystem von Grund auf baut und dabei branchenweit etablierte Praktiken und Bibliotheken verwendet."

---

## FOLIE 22: Fragen & Diskussion (2 Min)

**Seien Sie vorbereitet zu diskutieren:**

**Technische Fragen:**
- "Warum haben Sie Factory Pattern verwendet?"
  - Antwort: Vereinfacht Objekterstellung, professionelles Design
  
- "Wie funktioniert Strategy Pattern?"
  - Antwort: Kapselt verschiedene Algorithmen mit gleicher Schnittstelle
  
- "Warum NumPy statt Listen?"
  - Antwort: Vektorisierung ist 1000x schneller
  
- "Wie würden Sie neue Analytik hinzufügen?"
  - Antwort: Neue Methode zur BikeShareSystem-Klasse hinzufügen

**Projektfragen:**
- "Was war der schwierigste Teil?"
  - Antwort: Datenbereinigungs- und Validierungsregeln
  
- "Wie lange hat das gedauert?"
  - Antwort: Mehrere Wochen Entwicklung
  
- "Würde Sie etwas ändern?"
  - Antwort: [Ihre ehrliche Antwort]

---

## PRÄSENTATIONS-CHECKLISTE

Vor der Präsentation müssen Sie sicherstellen:

**Vorbereitung:**
- [ ] Präsentation 2-3x üben
- [ ] Den ganzen Code kennen und erklären können
- [ ] Live-Demo vorbereiten oder Konsolenausgabe haben
- [ ] Üben Sie den Übergang zwischen Folien
- [ ] Kennen Sie die Antworten auf wahrscheinliche Fragen

**Präsentation:**
- [ ] Laptop mit offenem Projekt bereit
- [ ] Projektor/Bildschirmfreigabe testen
- [ ] Backup haben (USB, Cloud) der Präsentation
- [ ] Notizen mitbringen (Stichpunkte, keine vollständigen Sätze)
- [ ] Professionelle Kleidung tragen

**Während:**
- [ ] Blickkontakt mit Publikum
- [ ] Klar und in gleichmäßigem Tempo sprechen
- [ ] Folien nicht direkt ablesen
- [ ] Zeiger für wichtige Punkte verwenden
- [ ] Pausen für Fragen einplanen

**Folien zum Anzeigen:**
- Architekturdiagramm anzeigen
- 2-3 Diagramme aus Ausgabe anzeigen
- Demo des laufenden Projekts
- GitHub-Repository anzeigen
- Code-Ausschnitte kurz anzeigen

---

## ZEITLICHE GLIEDERUNG

- Folie 1-2: Projektintro (2 Min)
- Folie 3-4: Problem & Architektur (2 Min)
- Folie 5-12: Module Übersicht (6 Min)
- Folie 13: Pipeline (1 Min)
- Folie 14: Live-Demo (2 Min)
- Folie 15-18: Zusammenfassung der Merkmale (3 Min)
- Folie 19-20: GitHub & Zukunft (2 Min)
- Folie 21-22: Fazit & F&A (2 Min)

**Gesamt: ~20 Minuten**

---

## WICHTIGE SPRECHPUNKTE ZUM MERKEN

1. **Starker Anfang:**
   "Dieses Projekt zeigt, wie echte Datenwissenschaftler arbeiten"

2. **Für Jedes Modul:**
   - Welches Problem löst es?
   - Welche Technologie wird verwendet?
   - Warum ist es so gestaltet?

3. **Betonen Sie:**
   - OOP und Design Patterns (professionelle Fähigkeiten)
   - Datenbereinigung (echte Herausforderung)
   - Automatisierte Pipeline (produktionsreif)
   - 14 geschäftliche Erkenntnisse (echter Wert)

4. **Seien Sie ehrlich:**
   - Was war herausfordernd
   - Was Sie gelernt haben
   - Was Sie anders machen würden
   - Zukünftige Verbesserungen

5. **Mit Lernen verbinden:**
   - Wie dieses Projekt Ihre Fähigkeiten verbessert hat
   - Was OOP/Design Patterns bedeuten
   - Warum Data Science wichtig ist
   - Professionelle Entwicklung

---

## PRÄSENTATIONSTIPPS

✅ **TUN Sie:**
- Mit Vertrauen sprechen
- Blickkontakt halten
- Pausen effektiv nutzen
- Auf spezifische Teile zeigen
- Fragen einladen
- Erklären Sie das Warum, nicht nur das Was
- Zeigen Sie Begeisterung

✗ **TUN Sie NICHT:**
- Folien direkt ablesen
- Vor dem Bildschirm stehen
- Sich durch Inhalte beeilen
- Zu viele Worte verwenden
- Entschuldigungen machen
- Sich für Code entschuldigen
- Zu schnell oder zu langsam sprechen

---

## SKRIPT BEISPIELE

**Eröffnung:**
"Hallo zusammen. Heute präsentiere ich mein Capstone-Projekt: CityBike Analytics Platform. Dies ist ein vollständiges Datenanalysesystem, das Bike-Sharing-Informationen verarbeitet und aussagekräftige Erkenntnisse generiert. Ich werde Sie durch die Architektur führen, zeige Ihnen einige Ergebnisse und erklären die Softwareentwicklungsprinzipien, die ich verwendet habe."

**Mitte:**
"Dieses Modul verwendet das Factory Pattern, ein professionelles Designmuster. Statt Objekte direkt an verstreuten Orten zu erstellen, zentralisieren wir die Logik hier. Wenn wir ändern müssen, wie Objekte erstellt werden, ändern wir nur diese eine Datei. Das ist viel besser, als die Logik überall zu duplizieren."

**Live-Demo:**
"Jetzt werde ich das Projekt live ausführen. Sie werden sehen, wie es Daten aus drei CSV-Dateien lädt, alles bereinigt, 14 verschiedene Analysefragen ausführt, Visualisierungen erstellt und Berichte exportiert - alles in etwa 10 Sekunden."

**Abschluss:**
"Dieses Projekt hat mich gelehrt, dass gutes Softwaredesign nicht nur darum geht, dass Dinge funktionieren - es geht darum, Dinge zu schaffen, die lesbar, wartbar und skalierbar sind. Die Design Patterns und OOP-Prinzipien, die ich hier verwendet habe, sind nicht nur akademisch; sie werden täglich in echten Produktionssystemen verwendet."

---

**Viel Erfolg bei Ihrer Präsentation! 🎤**

Sie schaffen das! Sie sollten stolz auf Ihr Projekt sein.
