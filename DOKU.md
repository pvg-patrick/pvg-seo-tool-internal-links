# SF Linking Monitor — Dokumentation

**Stand:** Juni 2026 · **Zielgruppe:** SEO, Content-Team

---

## Überblick

Zwei Tools in einem Repo:

| Tool | Datei | Wozu |
|------|-------|------|
| **SF Linking Monitor** | `run.py` + `monitor.html` | Monatliche Analyse der internen Verlinkungsstruktur auf Basis von Screaming Frog + GSC |
| **Link Converter** | `index.html` | HTML-Datei automatisch mit Keywords verlinken und Ratgeber-Widgets einfügen |

Die Tools sind über eine gemeinsame Navigation verknüpft. Beide laufen vollständig lokal — kein Server, kein Framework nötig.

---

## Setup (einmalig)

```bash
pip install pandas
```

Python 3.8+ vorausgesetzt. Das war es.

---

## Ordnerstruktur

```
pvg-seo-tool-internal-links/
│
├── data/                        ← CSVs hier ablegen (nicht ins Git!)
│   ├── sf-intern-2026-04.csv
│   ├── sf-html-2026-04.csv      (optional)
│   └── gsc-2026-04.csv          (optional)
│
├── output/                      ← auto-generiert von run.py
│   ├── dashboard_data.js        ← wird von monitor.html geladen
│   ├── linking_history.json     ← KPI-Verlauf aller Monate
│   ├── linking_baseline.json    ← Vergleichspunkt
│   ├── 2026-04_orphans.csv
│   ├── 2026-04_gaps.csv
│   ├── 2026-04_deep.csv
│   ├── 2026-04_dilution.csv
│   └── 2026-04_mono.csv
│
├── run.py                       ← Haupt-Script
├── sf_linking_monitor.py        ← Analyse-Engine (wird von run.py importiert)
├── monitor.html                 ← Dashboard
└── index.html                   ← Link Converter
```

> **Hinweis:** `data/` ist in `.gitignore` — CSVs kommen nicht ins Repo.

---

## Datei-Namenskonvention

Dateien in `data/` müssen exakt dieses Format haben:

| Datei | Quelle | Pflicht |
|-------|--------|---------|
| `sf-intern-YYYY-MM.csv` | SF Bulk Export → Links → All Internal Links | **Ja** |
| `sf-html-YYYY-MM.csv`   | SF Internal → Tab "HTML" → Export | Nein |
| `gsc-YYYY-MM.csv`       | GSC → Links → Interne Links → Top Zielseiten | Nein |

Beispiele:
```
sf-intern-2026-04.csv
sf-html-2026-04.csv
gsc-2026-04.csv
```

`run.py` erkennt alle Monate automatisch — einfach ablegen und loslaufen.

---

## Monatlicher Workflow (~20 Min.)

### Schritt 1 — Screaming Frog Crawl

Domain crawlen: `dsl.preisvergleich.de`

**Wichtig vor dem Crawl:**
- Configuration → Spider → Rendering: **JavaScript** (sonst fehlen Nav-Links)
- Configuration → Exclusions: `/content/AudioMP3/` ausschließen

---

### Schritt 2 — SF-Exporte

**Export 1 — All Internal Links** (Pflicht, ~17 MB):
```
Bulk Export → Links → All Internal Links
```
Speichern als: `data/sf-intern-2026-04.csv`

**Export 2 — HTML-Seiten** (empfohlen, für Tiefe-Analyse):
```
Internal → [Tab "HTML"] → Export
```
Speichern als: `data/sf-html-2026-04.csv`

---

### Schritt 3 — GSC-Export

```
Google Search Console → Links → Interne Links → Top Zielseiten → Exportieren
```
Speichern als: `data/gsc-2026-04.csv`

> Der GSC-Export enthält die Seiten, die Google intern am häufigsten verlinkt sieht (nav + content zusammen). Kombiniert mit den SF-Daten ergibt sich der **Prioritäts-Gap**: Seiten die Google wichtig findet, aber kaum Content-Links haben.

---

### Schritt 4 — Analyse ausführen

```bash
# Alle Monate in data/ verarbeiten
python run.py

# Nur einen Monat
python run.py --month 2026-04

# Baseline neu setzen (z. B. nach Fix-Sprint)
python run.py --baseline 2026-04
```

**Was passiert:**
1. `run.py` scannt `data/` nach Dateien mit der Namenskonvention
2. Für jeden Monat: SF-Links analysieren, HTML-Tiefe (falls vorhanden), GSC-Gaps (falls vorhanden)
3. KPIs in `output/linking_history.json` speichern
4. Problem-CSVs in `output/` schreiben
5. `output/dashboard_data.js` generieren (alle Daten für den Browser)

Ausgabe-Beispiel:
```
==============================================================
  SF LINKING MONITOR — Auto-Runner
==============================================================

  Gefunden: 2 Monat(e)

  Monat        SF-Links  SF-HTML  GSC
  ------------  --------  -------  ----
  2026-03       14.2 MB        ✓     ✓
  2026-04       17.1 MB        ✓     ✓

  ── 2026-04 ──────────────────────────────────────────────
  Geladen: sf-intern-2026-04.csv  (50.234 Zeilen)
  Geladen: sf-html-2026-04.csv    (1.609 Zeilen)
  Geladen: gsc-2026-04.csv        (312 Zeilen)
      orphans             → output/2026-04_orphans.csv
      gaps                → output/2026-04_gaps.csv
      deep                → output/2026-04_deep.csv

  dashboard_data.js  → output/dashboard_data.js  (87 KB)

  Fertig. monitor.html im Browser öffnen.
```

---

### Schritt 5 — Dashboard öffnen

`monitor.html` im Browser öffnen (Doppelklick oder `file:///...`).

Das Dashboard lädt `output/dashboard_data.js` automatisch. Kein Server nötig.

---

## Dashboard — Panels

### Dashboard
KPI-Karten für den aktuellen Monat:

| KPI | Was es misst | Ziel 3M | Ziel 6M |
|-----|-------------|---------|---------|
| Content-Link-Anteil % | Anteil redaktioneller Links an allen Links | 35% | 40% |
| Median Inlinks | Typische Verlinkungstiefe einer Seite | 5 | 8 |
| Generisch-Anchors % | Anteil "mehr erfahren" o. ä. | 3% | 1% |
| Orphan Pages | Seiten ohne jeden Inlink | 0 | 0 |
| Tiefe 4+ schwach | Seiten auf Crawltiefe ≥4 mit ≤3 Content-Inlinks | 60 | 40 |

---

### Empfehlungen

Das wichtigste Panel. Aggregiert priorisierte Maßnahmen aus allen geladenen Daten:

| Priorität | Quelle | Maßnahme |
|-----------|--------|----------|
| **Kritisch** | Orphan Pages | Mindestens 1 Content-Link aus thematisch passender Seite |
| **Kritisch** | Prioritäts-Gap (rank_gap > 50) | 2–3 Content-Links aus verwandten Artikeln |
| **Hoch** | Prioritäts-Gap (rank_gap > 15) | Content-Link ergänzen |
| **Mittel** | Tiefe 4+ schwach | Link aus höher gelegener Seite |
| **Mittel** | Generisch-Anchors > 3% | Anchors als Satzteil formulieren |
| **Niedrig** | Mono-Anchors | Anchor variieren wo redaktionell möglich |

**Prioritäts-Gap erklärt:**
`rank_gap = gsc_links / (content_inlinks + 1)`

Eine Seite mit 50 GSC-Links aber nur 2 Content-Inlinks hat `rank_gap = 50/3 ≈ 16.7`. Google "kennt" die Seite durch Navigation/Footer, aber kein redaktioneller Kontext stützt sie. Diese Seiten profitieren am meisten von gezielten Content-Links.

---

### Prioritäts-Gaps

Seiten mit hohem GSC-Gewicht aber wenigen Content-Inlinks. Nur verfügbar wenn `gsc-YYYY-MM.csv` vorhanden.

### Orphan Pages
Seiten ohne einen einzigen Inlink. Googlebot findet sie nur über die Sitemap — kein Equity, kein Kontext. **Sofort beheben.**

### Tiefe 4+ schwach verlinkt
Seiten tief im Crawlgraph mit wenig Content-Links. Kombination aus schlechter Erreichbarkeit und wenig Equity-Zufluss. Nur verfügbar wenn `sf-html-YYYY-MM.csv` vorhanden.

### Link Dilution
Seiten mit >40 unique Outlinks. Verteilt Equity zu breit. Besonders kritisch bei Seiten die selbst wenig Inlinks haben.

### Anchor-Analyse
Top 30 Anchor-Texte aus Content-Links. Generische Anchors sind rot markiert.

### Eintönige Anchors
Seiten die ≥3x mit exakt demselben Anchor verlinkt werden. Repetitives Exact-Match-Pattern, kein Mehrwert.

---

## Konfiguration anpassen

In `sf_linking_monitor.py`:

**Generische Anchors ergänzen:**
```python
GENERIC_ANCHORS = {
    "mehr erfahren", "hier", "entdecken", ...
    # eigene Begriffe ergänzen
}
```

**Zielwerte anpassen:**
```python
TARGETS = {
    "content_link_share_pct":   {"3m": 35, "6m": 40, ...},
    "generic_anchor_share_pct": {"3m": 3,  "6m": 1,  ...},
    "orphan_count":             {"3m": 0,  "6m": 0,  ...},
}
```

---

## Baseline-Strategie

Die Baseline (`output/linking_baseline.json`) ist der fixe Vergleichspunkt für alle Deltas.

- **Erste Baseline:** wird automatisch beim ersten `python run.py` gesetzt
- **Neue Baseline setzen:** nach einem gezielten Fix-Sprint — `python run.py --baseline YYYY-MM`
- **Nicht monatlich neu setzen** — sonst verliert man den Vergleich

---

## Troubleshooting

**`ModuleNotFoundError: sf_linking_monitor`**
`run.py` und `sf_linking_monitor.py` müssen im selben Ordner liegen. Ausführen aus dem Repo-Root.

**`UnicodeDecodeError`**
SF exportiert in Latin-1. Das Script probiert mehrere Encodings automatisch. Falls es trotzdem schlägt: Datei in einem Editor als UTF-8 neu speichern.

**`KeyError: 'Linkposition'` oder ähnliche Spalten**
Falscher Export. `sf-intern-*.csv` muss der "All Internal Links"-Export sein (Spalten: Quelle, Ziel, Anker, Linkposition, Follow, Status-Code).

**Footer-Links = 0**
SF benennt die Spalte je nach Spracheinstellung `Fußzeile` oder `Fu§zeile` (Encoding-Artefakt). Das Script behandelt beide. Falls trotzdem 0: prüfen ob Footer-Links in deinem Crawl als "Navigation" klassifiziert sind.

**Viele MP3-Dateien in der Tiefe-4+-Liste**
SF crawlt `/content/AudioMP3/` mit. In SF unter `Configuration → Exclusions` diesen Pfad ausschließen und neu crawlen.

**`data/sf-html-YYYY-MM.csv` nicht gefunden**
Die Tiefe-Analyse (deep_underlinked, median_unique_inlinks) wird dann übersprungen. Export: SF → Internal → Tab "HTML" → Export.

**Dashboard zeigt Demo-Daten**
`output/dashboard_data.js` existiert noch nicht. `python run.py` ausführen, dann `monitor.html` neu laden.

---

## Warum kein Browser-Upload der 17-MB-CSV?

Der "All Internal Links"-Export ist typischerweise 15–20 MB groß (~50.000 Zeilen). Im Browser würde das Parsen 5–10 Sekunden dauern und bei jedem Monatswechsel wiederholt. 

`run.py` reduziert die Rohdaten auf ~50–150 KB JSON. Der Browser lädt nur diese aufbereiteten Daten — schnell, ohne Wartezeit, persistent über Sessions.

---

## Quick Reference

```bash
# Setup (einmalig)
pip install pandas

# Monatlicher Workflow
cp ~/Downloads/alleinlinks_2026-04.csv  data/sf-intern-2026-04.csv
cp ~/Downloads/intern_alle_2026-04.csv  data/sf-html-2026-04.csv
cp ~/Downloads/gsc_top_pages_2026-04.csv  data/gsc-2026-04.csv
python run.py
# → monitor.html öffnen

# Nur einen Monat neu verarbeiten
python run.py --month 2026-04

# Neue Baseline nach Fix-Sprint
python run.py --baseline 2026-04

# Direkte Einzelanalyse (ohne run.py, für Debugging)
python sf_linking_monitor.py \
  --links data/sf-intern-2026-04.csv \
  --html  data/sf-html-2026-04.csv \
  --gsc   data/gsc-2026-04.csv \
  --month 2026-04
```
