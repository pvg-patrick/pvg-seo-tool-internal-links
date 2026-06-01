"""
SF Linking Monitor — Auto-Runner
==================================
Legt alle Ergebnisse in output/ ab und schreibt dashboard_data.js für monitor.html.

Ordnerstruktur:
  data/
    sf-intern-YYYY-MM.csv      SF Bulk Export → Links → All Internal Links
    sf-html-YYYY-MM.csv        SF Internal → Tab "HTML" → Export  (optional)
    gsc-YYYY-MM.csv            GSC → Links → Interne Links → Top Zielseiten  (optional)
  output/
    dashboard_data.js          für monitor.html  (auto-generiert)
    linking_history.json       KPI-Verlauf
    linking_baseline.json      Baseline-KPIs
    YYYY-MM_*.csv              Problem-Listen pro Monat

Aufruf:
  python run.py                       alle Monate in data/ verarbeiten
  python run.py --month 2026-04       nur diesen Monat
  python run.py --baseline 2026-03    Baseline auf diesen Monat setzen
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("\n  FEHLER: pandas nicht installiert — pip install pandas\n")
    sys.exit(1)

from sf_linking_monitor import (
    analyse_links,
    analyse_html_pages,
    analyse_gsc,
    load_baseline,
    save_baseline,
    update_history,
    GENERIC_ANCHORS,
)

DATA_DIR   = Path("data")
OUTPUT_DIR = Path("output")
HISTORY_FILE = Path("output") / "linking_history.json"
BASELINE_FILE = Path("output") / "linking_baseline.json"


# ── File discovery ──────────────────────────────────────────────────────────

def discover_months(only_month=None):
    """Scannt data/ nach sf-intern-YYYY-MM.csv und gibt Liste von Monats-Dicts zurück."""
    if not DATA_DIR.exists():
        print(f"\n  FEHLER: Ordner '{DATA_DIR}/' nicht gefunden.")
        print(f"  Bitte anlegen und CSVs ablegen:\n")
        print(f"    mkdir data")
        print(f"    # dann sf-intern-2026-04.csv, gsc-2026-04.csv usw. reinkopieren\n")
        return []

    sf_files = {}
    for f in sorted(DATA_DIR.glob("sf-intern-????-??.csv")):
        m = re.search(r"sf-intern-(\d{4}-\d{2})\.csv", f.name)
        if m:
            sf_files[m.group(1)] = f

    if not sf_files:
        print(f"\n  Keine sf-intern-YYYY-MM.csv Dateien in '{DATA_DIR}/' gefunden.")
        print(f"  Erwartetes Format: sf-intern-2026-04.csv\n")
        return []

    months = []
    for month, sf_path in sorted(sf_files.items()):
        if only_month and month != only_month:
            continue
        months.append({
            "month":   month,
            "sf":      sf_path,
            "sf_html": DATA_DIR / f"sf-html-{month}.csv",
            "gsc":     DATA_DIR / f"gsc-{month}.csv",
        })

    return months


def print_discovery(months):
    print(f"\n  Gefunden: {len(months)} Monat(e)\n")
    print(f"  {'Monat':<12} {'SF-Links':>10} {'SF-HTML':>8} {'GSC':>5}")
    print(f"  {'-'*12}  {'-'*10}  {'-'*8}  {'-'*5}")
    for entry in months:
        has_html = "✓" if entry["sf_html"].exists() else "–"
        has_gsc  = "✓" if entry["gsc"].exists()     else "–"
        sf_size  = f"{entry['sf'].stat().st_size / 1024 / 1024:.1f} MB"
        print(f"  {entry['month']:<12} {sf_size:>10}  {has_html:>8}  {has_gsc:>5}")
    print()


# ── Process one month ────────────────────────────────────────────────────────

def process_month(entry):
    month = entry["month"]
    print(f"  ── {month} ────────────────────────────────────────")

    link_data = analyse_links(str(entry["sf"]))

    html_data = None
    if entry["sf_html"].exists():
        html_data = analyse_html_pages(str(entry["sf_html"]), link_data["all_dests"])
    else:
        print(f"    sf-html-{month}.csv nicht gefunden — Tiefe-Analyse übersprungen")

    gsc_data = None
    if entry["gsc"].exists():
        gsc_data = analyse_gsc(str(entry["gsc"]), link_data["all_dests"])
    else:
        print(f"    gsc-{month}.csv nicht gefunden — Prioritäts-Gaps übersprungen")

    t       = link_data["total"]
    content = link_data["content"]

    kpis = {
        "month":                    month,
        "total_links":              t,
        "nav_links":                link_data["nav"],
        "content_links":            content,
        "footer_links":             link_data["footer"],
        "header_links":             link_data["header"],
        "aside_links":              link_data["aside"],
        "content_link_share_pct":   round(content / t * 100, 1) if t else 0,
        "unique_dest_urls":         len(link_data["all_dests"]),
        "orphan_count":             len(link_data["orphans"]),
        "generic_anchor_count":     link_data["gen_count"],
        "generic_anchor_share_pct": link_data["gen_share"],
    }

    if html_data:
        kpis["indexable_pages"]       = html_data["indexable"]
        kpis["median_unique_inlinks"] = html_data["median_inlinks"]
        kpis["mean_unique_inlinks"]   = html_data["mean_inlinks"]
        kpis["deep_underlinked"]      = len(html_data["deep_underlinked"])

    problems = _build_problems(link_data, html_data, gsc_data)
    return kpis, problems


def _build_problems(link_data, html_data, gsc_data):
    """Baut das Problems-Dict für dashboard_data.js."""
    problems = {}

    if len(link_data["orphans"]):
        problems["orphans"] = (
            link_data["orphans"][["dest"]]
            .rename(columns={"dest": "url"})
            .to_dict("records")
        )

    if gsc_data is not None and len(gsc_data["priority_gaps"]):
        cols = ["url", "gsc_links", "content_inlinks", "rank_gap"]
        problems["gaps"] = (
            gsc_data["priority_gaps"][cols]
            .head(100)
            .to_dict("records")
        )

    if html_data is not None and len(html_data["deep_underlinked"]):
        problems["deep"] = (
            html_data["deep_underlinked"][["url", "depth", "content_inlinks"]]
            .head(100)
            .to_dict("records")
        )

    if len(link_data["dilution"]):
        problems["dilution"] = (
            link_data["dilution"][["source", "unique_outlinks"]]
            .rename(columns={"source": "url"})
            .head(100)
            .to_dict("records")
        )

    if len(link_data["mono"]):
        mono = link_data["mono"].head(100).copy()
        cdf  = link_data["content_df"]
        def _anchor(url):
            rows = cdf[cdf["dest"] == url]["anchor"]
            return str(rows.iloc[0]) if len(rows) else ""
        mono["anchor"] = mono["dest"].apply(_anchor)
        problems["mono"] = (
            mono[["dest", "total_links", "unique_anchors", "anchor"]]
            .rename(columns={"dest": "url"})
            .to_dict("records")
        )

    top = link_data["top_anchors"].head(30)
    problems["top_anchors"] = [
        {
            "text":       str(anchor),
            "count":      int(count),
            "is_generic": str(anchor).lower().strip() in GENERIC_ANCHORS,
        }
        for anchor, count in top.items()
    ]

    return problems


# ── Write outputs ─────────────────────────────────────────────────────────────

def write_problem_csvs(month, problems):
    """Schreibt einzelne CSV-Dateien pro Problem-Typ nach output/."""
    skipped = {"top_anchors"}
    written = []
    for name, records in problems.items():
        if name in skipped or not records:
            continue
        out = OUTPUT_DIR / f"{month}_{name}.csv"
        with open(out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)
        written.append(f"      {name:<22} → {out}")
    if written:
        print("\n".join(written))


def write_dashboard_data(history, all_problems, baseline):
    """Schreibt output/dashboard_data.js — wird von monitor.html geladen."""
    months = [h["month"] for h in history]

    payload = {
        "generated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "months":    months,
        "history":   history,
        "problems":  all_problems,
        "baseline":  baseline or {},
    }

    js_path = OUTPUT_DIR / "dashboard_data.js"
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("/* Auto-generiert von run.py — nicht manuell bearbeiten */\n")
        f.write("window.LINKING_DATA = ")
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
        f.write(";\n")

    size_kb = js_path.stat().st_size / 1024
    print(f"\n  dashboard_data.js  → {js_path}  ({size_kb:.0f} KB)")


def _load_full_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return []


def _patch_history_file():
    """sf_linking_monitor schreibt linking_history.json ins CWD — wir wollen output/."""
    src = Path("linking_history.json")
    dst = HISTORY_FILE
    if src.exists() and src != dst:
        import shutil
        shutil.copy(src, dst)

    src_bl = Path("linking_baseline.json")
    dst_bl = BASELINE_FILE
    if src_bl.exists() and src_bl != dst_bl:
        import shutil
        shutil.copy(src_bl, dst_bl)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="SF Linking Monitor – Auto-Runner")
    p.add_argument("--month",    default=None, help="Nur diesen Monat (YYYY-MM)")
    p.add_argument("--baseline", default=None, help="Baseline auf diesen Monat setzen (YYYY-MM)")
    args = p.parse_args()

    print("\n" + "=" * 62)
    print("  SF LINKING MONITOR — Auto-Runner")
    print("=" * 62)

    OUTPUT_DIR.mkdir(exist_ok=True)

    months = discover_months(args.month)
    if not months:
        sys.exit(1)

    print_discovery(months)

    baseline      = load_baseline()
    all_problems  = {}
    processed_kpis = []

    for entry in months:
        kpis, problems = process_month(entry)
        processed_kpis.append(kpis)
        all_problems[kpis["month"]] = problems

        update_history(kpis)
        write_problem_csvs(kpis["month"], problems)
        print()

    _patch_history_file()

    # Baseline setzen
    if args.baseline:
        match = next((k for k in processed_kpis if k["month"] == args.baseline), None)
        if match:
            save_baseline(match)
            baseline = match
        else:
            print(f"  WARNUNG: --baseline {args.baseline} nicht in verarbeiteten Daten.\n")
    elif baseline is None and processed_kpis:
        save_baseline(processed_kpis[0])
        baseline = processed_kpis[0]
        print(f"  Erste Baseline gesetzt: {processed_kpis[0]['month']}\n")

    full_history = _load_full_history()
    write_dashboard_data(full_history, all_problems, baseline)

    print(f"\n  Fertig. monitor.html im Browser öffnen.\n")
    print("=" * 62 + "\n")


if __name__ == "__main__":
    main()
