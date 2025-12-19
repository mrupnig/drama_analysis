# Usability- und UX-Studie: Aufgabenstellungen für IDE-Vergleich (PyCharm vs. Spyder)

Grundlage ist das bereitgestellte Python-Projekt `drama_analysis`.  
Die folgenden Teilaufgaben sollen **in der jeweiligen IDE** bearbeitet werden.  
Die Aufgaben sind **offen formuliert**; es wird **kein konkreter Lösungsweg vorgegeben**.  
Der jeweils beschriebene *Idealpfad* dient ausschließlich der Auswertung und Beobachtung.

---
## Explorationsphase

---

## Teilaufgabe A – Projekt öffnen & Überblick verschaffen

### Kontext
Du arbeitest mit einem bestehenden Python-Projekt, das aus mehreren Dateien und Ordnern besteht.  
Ziel ist es, sich einen ersten Überblick über Struktur und Einstiegspunkt des Projekts zu verschaffen.

### Aufgabenstellung
Öffne das Projekt in der IDE und verschaffe dir einen Überblick über Aufbau und Inhalte.  
Führe anschließend das Programm aus.

### Idealpfad (nicht vorgeben)
- Projektordner als Projekt/Workspace in der IDE öffnen  
- Projektstruktur im Datei-/Projektbrowser erkunden  
- Datei `main.py` als Einstiegspunkt identifizieren  
- `main.py` im Editor öffnen  
- Programm über die IDE ausführen (z. B. Run-Button oder Run-Konfiguration)
- Abhängigkeiten installieren

### Misst
- Projektverwaltung / Projektöffnung
- Orientierung in der Projektstruktur
- Navigation zwischen Dateien
- Auffindbarkeit von Run-Funktionen
- Erstverständnis der IDE-Oberfläche

---

## Teilaufgabe B – Debugging

### Kontext
Das Programm lädt ein in TEI codiertes Drama und erstellt daraus
(1) einen Figuren-Graphen (Ko-Okkurrenz pro Szene) und
(2) eine Tabelle (CSV), wie oft Figuren als Sprecher*innen vorkommen.

In dieser Teilaufgabe sind **absichtlich Fehler (Bugs)** im Projekt eingebaut, die mit den Debugging-Funktionalitäten
der IDE identifiziert und behoben werden sollen.

### Aufgabenstellung
Führe das Projekt aus der IDE heraus aus.  
Behebe anschließend die folgenden Debugging-Fälle (B1–B3), sodass das Programm wieder erfolgreich durchläuft und alle Outputs erzeugt.

Erwartete Outputs nach erfolgreicher Fehlerbehebung:
- `output/character_graph.png`
- `output/character_speech_counts.csv`
- `output/character_graph.gexf`

Hinweis: Es ist erlaubt, Breakpoints zu setzen, Variablen zu inspizieren und Schritt-für-Schritt zu debuggen.

---

### Debugging-Fall B1 – Falscher TEI-Namespace / leere Trefferlisten

**Symptom (beim Ausführen):**
- Das Programm läuft ohne Crash, aber:
  - Graph hat 0 Knoten / 0 Kanten, oder
  - CSV ist leer, oder
  - es wird eine ValueError geworfen („Graph has no nodes“), je nach Implementierung der Visualisierung.

**Fehleridee (absichtlich im Code):**
In `drama_graph/dracor_reader.py` wird der TEI-Namespace falsch gesetzt, sodass XPath-Abfragen nichts finden.

**Beispiel für den eingebauten Fehler:**
```python
TEI_NS = {"tei": "http://www.tei-c.org/ns/10"}  # BUG: falsche Namespace-URL
```

**Was im Code zu beobachten ist (ohne Lösung vorzugeben):**

- `persons` ist leer
- `scenes` ist leer
- `scene_speakers` bleibt leer

**Idealpfad (nicht vorgeben)**

- Fehlverhalten (leere Outputs) erkennen
- Breakpoint in `parse_dracor_tei()` setzen
- Ergebnis der XPath-Abfragen inspizieren (Listenlänge / Inhalt)
- Ursache im Namespace/XPath lokalisieren
- Änderung testen, bis Figuren/Szenen gefunden werden

**Misst**

- Fähigkeit der IDE, „silent failures“ sichtbar zu machen (z. B. Watch/Variables)
- Debugger-Usability (Breakpoints, Step Into/Over, Inspect)
- Umgang mit Namespaces/XPath im Debugging

### Debugging-Fall B2 – Fehlerhafte Verarbeitung von who-Attributen (KeyError / falsche IDs)

**Symptom (beim Ausführen):**

Graph/CSV werden erzeugt, aber:

- viele Figuren heißen nur `„#…“` oder wirken ungemappt
- oder es tritt ein KeyError / unerwartetes Mapping-Verhalten auf, wenn IDs nicht bereinigt wurden.

**Fehler (absichtlich im Code):**
In `drama_graph/dracor_reader.py` wird die Normalisierung von `who="#ID"` falsch gemacht
(z. B. `rstrip("#")` statt `lstrip("#")`), dadurch stimmen IDs nicht mit `xml:id` überein.

Beispiel für den eingebauten Fehler:
```python
char_id = ref.rstrip("#")  # BUG: entfernt # am Ende statt am Anfang
```

**Beobachtungspunkte (ohne Lösung vorzugeben):**

- `char_id` enthält weiterhin `#…` oder wird falsch abgeschnitten
- `id_to_name.get(char_id)` liefert häufig Fallback statt echte Namen

**Idealpfad (nicht vorgeben)**

- Breakpoint beim Parsen von `<sp who=...>` setzen
- `who`, `ref` und `char_id` vergleichen
- Diskrepanz zwischen `xml:id` und `who` nachvollziehen
- Fix validieren (Counts/Labels plausibel)

**Misst**

- Variablenvergleich/Inspektion über mehrere Iterationen
- „Data flow“-Verständnis (Input-Attribute → Normalisierung → Mapping)
- Debugging im Loop (Conditional Breakpoints optional)
---

## Teilaufgabe C – Refactoring

### Kontext
Das Projekt ist funktional korrekt, weist jedoch mehrere strukturelle und
wartungstechnische Probleme auf. Der Code wurde bewusst so gestaltet, dass er
zwar lauffähig ist, aber typische „Code Smells“ enthält.

In dieser Teilaufgabe soll der Code **refaktoriert** werden, ohne das
beobachtbare Verhalten zu verändern (keine neue Funktionalität, keine Bugfixes
im engeren Sinne).

### Aufgabenstellung
Analysiere den bestehenden Code und führe die Refactorings der Fälle durch.
Nutze dabei gezielt die Refactoring-Werkzeuge der IDE (z. B. Rename, Extract
Method, Move, Inline, Reformat, Optimize Imports).

Nach dem Refactoring muss:
- das Programm weiterhin korrekt laufen,
- die Ausgaben unverändert bleiben,
- der Code besser lesbar, strukturierter und wartungsfreundlicher sein.

---

### Refactoring-Fall C1 – Unklare oder irreführende Bezeichner

**Problem (Code Smell):**
Variablen- oder Funktionsnamen sind:
- zu kurz (`cnt`, `tmp`, `res`)
- zu generisch (`data`, `items`)
- fachlich unpräzise im Kontext von Dramenanalyse

**Beispiele:**
```python
res = build_character_graph(...)
tmp = []
cnt += 1
```
**Aufgabe:**

Benenne Variablen, Funktionen oder Attribute um, sodass ihre Rolle im
Projektkontext eindeutig wird.

Achte darauf, dass alle Verwendungen korrekt angepasst werden.

**Ziel des Refactorings:**

- Domänenklarheit (Drama / Figur / Szene)
- Reduktion kognitiver Last beim Lesen

**Misst**

- Rename Symbol (projektweit)
- Preview von Änderungen
- Sicherheit bei großflächigen Umbenennungen
---

### Refactoring-Fall C2 – Lange Funktionen / mangelnde Abstraktion

**Problem (Code Smell):**
Eine oder mehrere Funktionen sind sehr lang und erledigen mehrere Aufgaben
gleichzeitig (z. B. Parsing, Zählen, Normalisieren, Validieren).

**Typische Kandidaten:**
- `parse_dracor_tei()`
- Funktionen mit mehreren logisch getrennten Code-Blöcken

**Aufgabe:**
- Zerlege die Funktion in kleinere, klar benannte Hilfsfunktionen
  (z. B. `extract_persons`, `extract_scenes`, `count_speakers`).
- Stelle sicher, dass die öffentliche API unverändert bleibt.

**Ziel des Refactorings:**
- bessere Lesbarkeit
- klarere Verantwortlichkeiten
- leichtere Testbarkeit

**Misst**
- Extract Method
- Navigation zwischen Methoden
- Übersichtlichkeit nach Refactoring

---

## Teilaufgabe D – Autocompletion & Syntax-Highlighting

### Kontext
Das Projekt soll um eine kleine zusätzliche Funktion erweitert werden.  
Die Funktion ist vorgegeben und soll in eine bestehende Datei übernommen werden. Die Funktion soll anschließend in `main.py` importiert und an der richtigen Stelle aufgerufen werden.

### Aufgabenstellung
Erstelle diese Funktion in `visualize.py`. Ersetze den Color-Code in `render_graph_png()` durch einen Aufruf der neuen Funktion.

```python
def node_colors_by_speech_count(graph: nx.Graph):
    counts = [graph.nodes[n].get("speech_count", 1) for n in graph.nodes]
    m = max(counts)
    return [plt.cm.Blues(c / m) for c in counts]
```

### Misst
- Qualität der Autovervollständigung
- Lesbarkeit durch Syntax-Highlighting
- Unterstützung bei Typannotationen
- Fehler- und Warnhinweise während der Eingabe
- Schreibkomfort im Editor

---

## Teilaufgabe E – Versionierung (Git)

### Kontext
Das Projekt ist bereits als Git-Repository vorbereitet.  
Die vorgenommenen Änderungen sollen versioniert werden.

### Aufgabenstellung
Überprüfe den aktuellen Versionsstatus des Projekts und sichere deine Änderungen in einem Commit.  
Betrachte anschließend die vorgenommenen Änderungen.

### Idealpfad (nicht vorgeben)
- Git-Status in der IDE aufrufen
- Geänderte Dateien identifizieren
- Diff-Ansicht für mindestens eine Datei öffnen
- Commit mit aussagekräftiger Commit-Nachricht erstellen
- Optional: eine Änderung verwerfen oder rückgängig machen

### Misst
- Integration von Versionskontrolle in der IDE
- Verständlichkeit von Status- und Diff-Ansichten
- Usability des Commit-Workflows
- Unterstützung bei Revert/Discard-Aktionen
- Transparenz von Code-Änderungen

---
