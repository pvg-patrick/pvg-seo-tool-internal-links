# PREISVERGLEICH.de Style Guide

**Version:** 2025  
**Letzte Aktualisierung:** Februar 2026

---

## Inhaltsverzeichnis

1. [Einleitung](#einleitung)
2. [Markenidentität](#markenidentität)
3. [Farbpaletten](#farbpaletten)
4. [Typografie](#typografie)
5. [Logos & Favicons](#logos--favicons)
6. [Designsystem](#designsystem)
7. [UI-Komponenten](#ui-komponenten)
8. [Spacing & Layout](#spacing--layout)
9. [Buttons & CTAs](#buttons--ctas)
10. [Icons & Grafiken](#icons--grafiken)
11. [Formulare & Eingabefelder](#formulare--eingabefelder)
12. [Responsive Design](#responsive-design)
13. [Best Practices](#best-practices)

---

## Einleitung

Dieser Style Guide definiert die visuellen und funktionalen Standards für PREISVERGLEICH.de. Er dient als zentrale Referenz für Designer, Entwickler und Content-Ersteller zur Sicherstellung einer konsistenten Markendarstellung über alle digitalen Touchpoints.

### Zielgruppe
- Frontend-Entwickler
- UI/UX-Designer
- Marketing-Team
- Content-Ersteller

---

## Markenidentität

### Brand Mission
PREISVERGLEICH.de ist Deutschlands führendes Vergleichsportal mit der BESTPREIS-Garantie. Wir helfen Verbrauchern, Zeit zu sparen und die besten Angebote auf dem Markt zu finden – kostenfrei, unabhängig und transparent.

### Markenwerte
- **Vertrauenswürdig**: #1 Preis-/Leistungssieger (DtGV)
- **Transparent**: Unabhängiger Vergleich ohne versteckte Kosten
- **Nutzerfreundlich**: Einfache Navigation und klare Vergleichsrechner
- **Zuverlässig**: Über 94% Kundenzufriedenheit

---

## Farbpaletten

### Primärfarben

Die Primärfarben repräsentieren die Marke PREISVERGLEICH.de und werden für Hauptelemente wie Header, Navigation und primäre CTAs verwendet.

| Farbe | Hex Code | RGB | Verwendung |
|-------|----------|-----|------------|
| **Primary Dark** | `#003043` | rgb(0, 48, 67) | Header, dunkle Hintergründe, Kontrast-Elemente |
| **Primary** | `#087E9F` | rgb(8, 126, 159) | Hauptmarkenfarbe, Links, primäre Buttons |
| **Primary Light** | `#429BB3` | rgb(66, 155, 179) | Hover-Zustände, sekundäre Elemente, Highlights |

```css
/* CSS-Variablen für Primärfarben */
:root {
  --color-primary-dark: #003043;
  --color-primary: #087E9F;
  --color-primary-light: #429BB3;
}
```

### Sekundärfarben

Die Sekundärfarben werden für Akzente, Warnungen und spezielle Hervorhebungen verwendet.

| Farbe | Hex Code | RGB | Verwendung |
|-------|----------|-----|------------|
| **Secondary Dark** | `#9C1A00` | rgb(156, 26, 0) | Dringliche Warnungen, wichtige Hinweise |
| **Secondary** | `#C62000` | rgb(198, 32, 0) | Fehler, kritische Informationen, Sale-Badges |
| **Secondary Light** | `#F13A00` | rgb(241, 58, 0) | Hover-Zustände für sekundäre Aktionen, Akzente |

```css
/* CSS-Variablen für Sekundärfarben */
:root {
  --color-secondary-dark: #9C1A00;
  --color-secondary: #C62000;
  --color-secondary-light: #F13A00;
}
```

### Graustufen (Neutrals)

Graustufen für Text, Hintergründe und Abstufungen.

| Farbe | Hex Code | RGB | Verwendung |
|-------|----------|-----|------------|
| **Gray 900** | `#444444` | rgb(68, 68, 68) | Haupttext, Headlines |
| **Gray 500** | `#AAAAAA` | rgb(170, 170, 170) | Sekundärtext, deaktivierte Elemente |
| **Gray 400** | `#BBBBBB` | rgb(187, 187, 187) | Borders, Trennlinien |
| **Gray 200** | `#EEEEEE` | rgb(238, 238, 238) | Hintergründe, Card-Backgrounds |
| **Gray 100** | `#F2F2F2` | rgb(242, 242, 242) | Helle Hintergründe, Sections |
| **Gray 50** | `#F8F8F8` | rgb(248, 248, 248) | Sehr helle Hintergründe, Wrapper |

```css
/* CSS-Variablen für Graustufen */
:root {
  --color-gray-900: #444444;
  --color-gray-500: #AAAAAA;
  --color-gray-400: #BBBBBB;
  --color-gray-200: #EEEEEE;
  --color-gray-100: #F2F2F2;
  --color-gray-50: #F8F8F8;
}
```

### Status & Feedback-Farben

Signalfarben für Rückmeldungen und Status-Informationen.

| Farbe | Hex Code | RGB | Verwendung |
|-------|----------|-----|------------|
| **Error / Red** | `#C41D1D` | rgb(196, 29, 29) | Fehlermeldungen, Validierungsfehler |
| **Warning / Yellow** | `#FEC002` | rgb(254, 192, 2) | Warnungen, wichtige Hinweise |
| **Success / Green** | `#54BF84` | rgb(84, 191, 132) | Erfolgsbestätigungen, positive Feedback |

```css
/* CSS-Variablen für Status-Farben */
:root {
  --color-error: #C41D1D;
  --color-warning: #FEC002;
  --color-success: #54BF84;
}
```

### Farbverwendung - Best Practices

#### Text auf Hintergründen
- Dunkler Text (`#444444`) auf hellen Hintergründen (`#F8F8F8`, `#FFFFFF`)
- Weißer Text (`#FFFFFF`) auf dunklen Hintergründen (`#003043`, `#087E9F`)
- Mindest-Kontrastverhältnis: 4.5:1 für normalen Text (WCAG AA)

#### Interaktive Elemente
```css
/* Button Primär */
.btn-primary {
  background-color: #087E9F;
  color: #FFFFFF;
}

.btn-primary:hover {
  background-color: #003043;
}

/* Button Sekundär */
.btn-secondary {
  background-color: #F13A00;
  color: #FFFFFF;
}

.btn-secondary:hover {
  background-color: #C62000;
}
```

---

## Typografie

### Schriftart: Rubik

**Primärschrift:** [Rubik](https://fonts.google.com/specimen/Rubik) (Google Fonts)

Rubik ist eine moderne, gut lesbare Sans-Serif-Schrift, die optimal für digitale Medien geeignet ist. Sie bietet hervorragende Lesbarkeit sowohl auf Desktop- als auch auf mobilen Geräten.

#### Schriftarten-Import

```html
<!-- Google Fonts Integration -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

```css
/* CSS Font Family */
body {
  font-family: 'Rubik', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
}
```

### Schriftgewichte

| Gewicht | Wert | Verwendung |
|---------|------|------------|
| Light | 300 | Dekorative Texte, große Headlines (selten) |
| Regular | 400 | Fließtext, Standardtext |
| Medium | 500 | Subheadlines, Hervorhebungen |
| Semi-Bold | 600 | Buttons, wichtige Labels |
| Bold | 700 | Headlines, Überschriften |

### Typografie-Skala

#### Desktop (Basis: 16px)

```css
:root {
  /* Headlines */
  --font-size-h1: 48px;      /* 3rem */
  --font-size-h2: 36px;      /* 2.25rem */
  --font-size-h3: 28px;      /* 1.75rem */
  --font-size-h4: 24px;      /* 1.5rem */
  --font-size-h5: 20px;      /* 1.25rem */
  --font-size-h6: 18px;      /* 1.125rem */
  
  /* Body Text */
  --font-size-base: 16px;    /* 1rem */
  --font-size-large: 18px;   /* 1.125rem */
  --font-size-small: 14px;   /* 0.875rem */
  --font-size-xs: 12px;      /* 0.75rem */
  
  /* Line Heights */
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
}
```

#### Mobile (< 768px)

```css
@media (max-width: 767px) {
  :root {
    --font-size-h1: 32px;      /* 2rem */
    --font-size-h2: 28px;      /* 1.75rem */
    --font-size-h3: 24px;      /* 1.5rem */
    --font-size-h4: 20px;      /* 1.25rem */
    --font-size-h5: 18px;      /* 1.125rem */
    --font-size-h6: 16px;      /* 1rem */
  }
}
```

### Text-Styles

#### Headlines
```css
h1, .h1 {
  font-size: var(--font-size-h1);
  font-weight: 700;
  line-height: var(--line-height-tight);
  color: var(--color-gray-900);
  margin-bottom: 24px;
}

h2, .h2 {
  font-size: var(--font-size-h2);
  font-weight: 700;
  line-height: var(--line-height-tight);
  color: var(--color-gray-900);
  margin-bottom: 20px;
}

h3, .h3 {
  font-size: var(--font-size-h3);
  font-weight: 600;
  line-height: var(--line-height-normal);
  color: var(--color-gray-900);
  margin-bottom: 16px;
}
```

#### Body Text
```css
body {
  font-size: var(--font-size-base);
  font-weight: 400;
  line-height: var(--line-height-normal);
  color: var(--color-gray-900);
}

p {
  margin-bottom: 16px;
}

.text-large {
  font-size: var(--font-size-large);
  line-height: var(--line-height-relaxed);
}

.text-small {
  font-size: var(--font-size-small);
  line-height: var(--line-height-normal);
}
```

#### Links
```css
a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}

a:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

## Logos & Favicons

### Hauptlogo

Das PREISVERGLEICH.de Logo existiert in mehreren Varianten:

#### Logo-Varianten
1. **Vollfarb-Logo** (Standard): Für helle Hintergründe
2. **Logo Weiß**: Für dunkle Hintergründe (z.B. Header `#003043`)
3. **Logo Monochrom**: Für spezielle Anwendungen

#### Logo-Dateiformate
- **SVG**: Bevorzugt für Web (skalierbar, klein)
- **PNG**: Für Anwendungen ohne SVG-Support (300 DPI für Druck)
- **ICO/PNG**: Favicon in verschiedenen Größen

#### Logo-Platzierung
- **Mindestabstand**: 20px Freiraum um das Logo
- **Mindestgröße Web**: 120px Breite
- **Mindestgröße Druck**: 30mm Breite

### Siegel & Badges

#### BESTPREIS-Garantie Siegel
- Verwendung auf Vergleichsrechnern und Zielseiten
- Immer in Originalfarben (Rot/Weiß)
- Mindestgröße: 60px Breite

#### DtGV Siegel
- "1. Platz Preisvergleichsportale"
- Verwendung auf Homepage und Marketing-Materialien
- Siegel nicht verzerren oder uneinfärben

---

## Designsystem

### Border Radius

Einheitliche Rundungen für ein konsistentes Erscheinungsbild.

```css
:root {
  --border-radius-sm: 3px;      /* Kleine Elemente (Tags, Badges) */
  --border-radius-md: 5px;      /* Standard (Buttons, Cards, Inputs) */
  --border-radius-lg: 8px;      /* Größere Container */
  --border-radius-xl: 12px;     /* Hero-Bereiche, große Cards */
  --border-radius-full: 9999px; /* Runde Buttons, Avatare */
}
```

#### Verwendungsbeispiele
```css
/* Button */
.btn {
  border-radius: var(--border-radius-md);
}

/* Card */
.card {
  border-radius: var(--border-radius-lg);
}

/* Input Field */
.input {
  border-radius: var(--border-radius-md);
}

/* Badge */
.badge {
  border-radius: var(--border-radius-sm);
}
```

### Schatten (Shadows)

Schatten zur Erzeugung von Tiefe und visueller Hierarchie.

```css
:root {
  --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
```

#### Anwendung
```css
/* Hover-Effekt auf Cards */
.card {
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: var(--shadow-lg);
}

/* Dropdown-Menü */
.dropdown {
  box-shadow: var(--shadow-xl);
}
```

### Transitions

Einheitliche Animationen für flüssige Interaktionen.

```css
:root {
  --transition-fast: 150ms ease;
  --transition-normal: 250ms ease;
  --transition-slow: 350ms ease;
}
```

```css
/* Standard-Transition für interaktive Elemente */
.btn, .link, .card {
  transition: all var(--transition-normal);
}

/* Schnelle Transition für kleine Änderungen */
.icon {
  transition: transform var(--transition-fast);
}

/* Langsame Transition für größere Änderungen */
.modal {
  transition: opacity var(--transition-slow);
}
```

---

## UI-Komponenten

### Cards

Cards sind Container für verwandte Informationen.

```css
.card {
  background-color: #FFFFFF;
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-gray-400);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition-normal);
}

.card:hover {
  box-shadow: var(--shadow-md);
}

/* Card Header */
.card-header {
  border-bottom: 1px solid var(--color-gray-200);
  padding-bottom: 16px;
  margin-bottom: 16px;
}

/* Card Title */
.card-title {
  font-size: var(--font-size-h4);
  font-weight: 600;
  color: var(--color-gray-900);
  margin-bottom: 8px;
}

/* Card Body */
.card-body {
  font-size: var(--font-size-base);
  line-height: var(--line-height-normal);
}
```

### Teaser / Promo-Kacheln

```css
.teaser {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  border-radius: var(--border-radius-xl);
  padding: 32px;
  color: #FFFFFF;
  position: relative;
  overflow: hidden;
}

.teaser-title {
  font-size: var(--font-size-h3);
  font-weight: 700;
  margin-bottom: 12px;
}

.teaser-subtitle {
  font-size: var(--font-size-large);
  opacity: 0.9;
  margin-bottom: 24px;
}
```

### Badges

```css
.badge {
  display: inline-block;
  padding: 4px 12px;
  font-size: var(--font-size-xs);
  font-weight: 600;
  line-height: 1;
  border-radius: var(--border-radius-sm);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-primary {
  background-color: var(--color-primary);
  color: #FFFFFF;
}

.badge-success {
  background-color: var(--color-success);
  color: #FFFFFF;
}

.badge-warning {
  background-color: var(--color-warning);
  color: var(--color-gray-900);
}

.badge-error {
  background-color: var(--color-error);
  color: #FFFFFF;
}
```

---

## Spacing & Layout

### Spacing-System (8px Grid)

Alle Abstände basieren auf einem 8px-Raster für konsistente vertikale und horizontale Rhythmen.

```css
:root {
  --spacing-xs: 4px;      /* 0.25rem */
  --spacing-sm: 8px;      /* 0.5rem */
  --spacing-md: 16px;     /* 1rem */
  --spacing-lg: 24px;     /* 1.5rem */
  --spacing-xl: 32px;     /* 2rem */
  --spacing-2xl: 48px;    /* 3rem */
  --spacing-3xl: 64px;    /* 4rem */
  --spacing-4xl: 96px;    /* 6rem */
}
```

#### Margin & Padding Utilities

```css
/* Margin */
.m-0 { margin: 0; }
.m-sm { margin: var(--spacing-sm); }
.m-md { margin: var(--spacing-md); }
.m-lg { margin: var(--spacing-lg); }
.m-xl { margin: var(--spacing-xl); }

/* Padding */
.p-0 { padding: 0; }
.p-sm { padding: var(--spacing-sm); }
.p-md { padding: var(--spacing-md); }
.p-lg { padding: var(--spacing-lg); }
.p-xl { padding: var(--spacing-xl); }

/* Margin Bottom (für vertikale Rhythmen) */
.mb-sm { margin-bottom: var(--spacing-sm); }
.mb-md { margin-bottom: var(--spacing-md); }
.mb-lg { margin-bottom: var(--spacing-lg); }
.mb-xl { margin-bottom: var(--spacing-xl); }
```

### Container & Layout-Struktur

```css
/* Haupt-Container */
.container {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 16px;
  padding-right: 16px;
}

/* Breiter Container */
.container-wide {
  max-width: 1440px;
}

/* Volle Breite Container */
.container-fluid {
  width: 100%;
  padding-left: 16px;
  padding-right: 16px;
}

/* Section Spacing */
.section {
  padding-top: var(--spacing-3xl);
  padding-bottom: var(--spacing-3xl);
}

@media (max-width: 767px) {
  .section {
    padding-top: var(--spacing-2xl);
    padding-bottom: var(--spacing-2xl);
  }
}
```

### Grid-System

```css
/* 12-Spalten Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--spacing-lg);
}

/* Grid-Varianten */
.grid-2 {
  grid-template-columns: repeat(2, 1fr);
}

.grid-3 {
  grid-template-columns: repeat(3, 1fr);
}

.grid-4 {
  grid-template-columns: repeat(4, 1fr);
}

/* Responsive Grid */
@media (max-width: 991px) {
  .grid-3, .grid-4 {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .grid-2, .grid-3, .grid-4 {
    grid-template-columns: 1fr;
  }
}
```

---

## Buttons & CTAs

### Button-Styles

```css
/* Base Button */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: 'Rubik', sans-serif;
  font-size: var(--font-size-base);
  font-weight: 600;
  line-height: 1;
  padding: 14px 28px;
  border-radius: var(--border-radius-md);
  border: none;
  cursor: pointer;
  text-decoration: none;
  transition: all var(--transition-normal);
  white-space: nowrap;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Primary Button */
.btn-primary {
  background-color: var(--color-primary);
  color: #FFFFFF;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* Secondary Button */
.btn-secondary {
  background-color: var(--color-secondary);
  color: #FFFFFF;
}

.btn-secondary:hover:not(:disabled) {
  background-color: var(--color-secondary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* Outline Button */
.btn-outline {
  background-color: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
}

.btn-outline:hover:not(:disabled) {
  background-color: var(--color-primary);
  color: #FFFFFF;
}

/* Ghost Button */
.btn-ghost {
  background-color: transparent;
  color: var(--color-primary);
}

.btn-ghost:hover:not(:disabled) {
  background-color: var(--color-gray-100);
}
```

### Button-Größen

```css
/* Small Button */
.btn-sm {
  font-size: var(--font-size-small);
  padding: 10px 20px;
}

/* Large Button */
.btn-lg {
  font-size: var(--font-size-large);
  padding: 18px 36px;
}

/* Full Width Button */
.btn-block {
  width: 100%;
  display: flex;
}
```

### Button mit Icon

```css
.btn-icon {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-icon svg,
.btn-icon img {
  width: 20px;
  height: 20px;
}
```

---

## Icons & Grafiken

### Icon-Größen

```css
:root {
  --icon-xs: 16px;
  --icon-sm: 20px;
  --icon-md: 24px;
  --icon-lg: 32px;
  --icon-xl: 48px;
}

.icon {
  display: inline-block;
  width: var(--icon-md);
  height: var(--icon-md);
}

.icon-sm { width: var(--icon-sm); height: var(--icon-sm); }
.icon-lg { width: var(--icon-lg); height: var(--icon-lg); }
.icon-xl { width: var(--icon-xl); height: var(--icon-xl); }
```

### Icon-Farben

Icons sollten standardmäßig die Textfarbe erben, können aber auch mit spezifischen Farben versehen werden:

```css
.icon-primary { color: var(--color-primary); }
.icon-secondary { color: var(--color-secondary); }
.icon-success { color: var(--color-success); }
.icon-warning { color: var(--color-warning); }
.icon-error { color: var(--color-error); }
```

### Bildoptimierung

- **WebP**: Bevorzugtes Format für moderne Browser (Fallback zu JPG/PNG)
- **Lazy Loading**: `loading="lazy"` für Bilder außerhalb des Viewports
- **Responsive Images**: `srcset` für verschiedene Auflösungen
- **Alt-Texte**: Immer beschreibende Alt-Attribute verwenden

```html
<picture>
  <source srcset="image.webp" type="image/webp">
  <source srcset="image.jpg" type="image/jpeg">
  <img src="image.jpg" alt="Beschreibender Text" loading="lazy">
</picture>
```

---

## Formulare & Eingabefelder

### Input Fields

```css
/* Base Input */
.input {
  width: 100%;
  font-family: 'Rubik', sans-serif;
  font-size: var(--font-size-base);
  padding: 12px 16px;
  border: 1px solid var(--color-gray-400);
  border-radius: var(--border-radius-md);
  background-color: #FFFFFF;
  color: var(--color-gray-900);
  transition: border-color var(--transition-normal), box-shadow var(--transition-normal);
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(8, 126, 159, 0.1);
}

.input:disabled {
  background-color: var(--color-gray-100);
  cursor: not-allowed;
  opacity: 0.6;
}

/* Input with Error */
.input.error {
  border-color: var(--color-error);
}

.input.error:focus {
  box-shadow: 0 0 0 3px rgba(196, 29, 29, 0.1);
}

/* Input Success */
.input.success {
  border-color: var(--color-success);
}
```

### Labels

```css
.label {
  display: block;
  font-size: var(--font-size-small);
  font-weight: 500;
  color: var(--color-gray-900);
  margin-bottom: 6px;
}

.label-required::after {
  content: " *";
  color: var(--color-error);
}
```

### Form Groups

```css
.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-help-text {
  font-size: var(--font-size-small);
  color: var(--color-gray-500);
  margin-top: 6px;
}

.form-error-text {
  font-size: var(--font-size-small);
  color: var(--color-error);
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}
```

### Select / Dropdown

```css
.select {
  width: 100%;
  font-family: 'Rubik', sans-serif;
  font-size: var(--font-size-base);
  padding: 12px 16px;
  border: 1px solid var(--color-gray-400);
  border-radius: var(--border-radius-md);
  background-color: #FFFFFF;
  color: var(--color-gray-900);
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,..."); /* Dropdown-Icon */
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
}

.select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(8, 126, 159, 0.1);
}
```

### Checkbox & Radio

```css
.checkbox,
.radio {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox input[type="checkbox"],
.radio input[type="radio"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: var(--color-primary);
}

.checkbox label,
.radio label {
  cursor: pointer;
  user-select: none;
}
```

---

## Responsive Design

### Breakpoints

```css
:root {
  --breakpoint-xs: 0;
  --breakpoint-sm: 576px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 992px;
  --breakpoint-xl: 1200px;
  --breakpoint-xxl: 1440px;
}
```

### Media Queries

```css
/* Mobile First Ansatz */

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
  /* Styles */
}

/* Medium devices (tablets, 768px and up) */
@media (min-width: 768px) {
  /* Styles */
}

/* Large devices (desktops, 992px and up) */
@media (min-width: 992px) {
  /* Styles */
}

/* Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
  /* Styles */
}
```

### Responsive Utilities

```css
/* Sichtbarkeit */
.hidden-mobile {
  display: none;
}

@media (min-width: 768px) {
  .hidden-mobile {
    display: block;
  }
}

.hidden-desktop {
  display: block;
}

@media (min-width: 768px) {
  .hidden-desktop {
    display: none;
  }
}
```

---

## Best Practices

### Performance

1. **CSS-Optimierung**
   - CSS minifizieren und komprimieren
   - Kritisches CSS inline laden
   - Nicht verwendete CSS entfernen

2. **Bilder**
   - Moderne Formate nutzen (WebP, AVIF)
   - Lazy Loading implementieren
   - Responsive Images verwenden

3. **Fonts**
   - `font-display: swap` verwenden
   - Nur benötigte Schriftschnitte laden
   - Font-Subsetting für kleinere Dateigrößen

### Accessibility (a11y)

1. **Farbe & Kontrast**
   - Mindestens WCAG AA-Standard erfüllen (4.5:1 für normalen Text)
   - Nicht nur Farbe zur Informationsvermittlung nutzen

2. **Fokus-Zustände**
   - Deutlich sichtbare Fokus-Indikatoren
   - Logische Tab-Reihenfolge

3. **Semantisches HTML**
   - Korrekte HTML5-Elemente verwenden
   - ARIA-Labels wo notwendig

4. **Responsive & Touch**
   - Mindestgröße für Touch-Targets: 44x44px
   - Ausreichend Abstand zwischen interaktiven Elementen

### Code-Qualität

1. **CSS-Namenskonventionen**
   - BEM-Methodik (Block__Element--Modifier)
   - Sprechende Klassennamen

2. **Kommentierung**
   - Komplexe Styles dokumentieren
   - Abschnitte klar strukturieren

3. **Wiederverwendbarkeit**
   - Utility-Klassen für häufige Muster
   - Komponenten-basierter Ansatz

---

## Version & Änderungshistorie

| Version | Datum | Änderungen |
|---------|-------|------------|
| 1.0 | Februar 2026 | Initiale Version des Style Guides |

---

**Kontakt & Feedback**

Für Fragen, Anregungen oder Aktualisierungen dieses Style Guides wenden Sie sich bitte an das Design-Team.

---

**© 2026 PREISVERGLEICH.de - GET Sol 1 GmbH**
