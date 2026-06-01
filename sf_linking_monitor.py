"""
SF Internal Linking Monitor
============================
Exporte aus Screaming Frog:
  --links: Bulk Export → Links → All Internal Links → alleinlinks_YYYY-MM.csv
  --html:  Internal → [Tab "HTML"] → Export → intern_alle_YYYY-MM.csv  (optional)
  --gsc:   GSC Links → Interne Links → Top Zielseiten → gsc_top_pages_YYYY-MM.csv  (optional)

Aufruf:
  python sf_linking_monitor.py --links alleinlinks_2026-04.csv --month 2026-04
  python sf_linking_monitor.py --links alleinlinks_2026-04.csv --html intern_alle_2026-04.csv --gsc gsc_top_pages_2026-04.csv --month 2026-04
  python sf_linking_monitor.py --links alleinlinks_2026-04.csv --month 2026-04 --export-csv --out-dir ./reports/2026-04
  python sf_linking_monitor.py --links alleinlinks_2026-04.csv --month 2026-04 --save-baseline
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("\n  FEHLER: pandas nicht installiert.")
    print("  Bitte ausführen:  python -m pip install pandas\n")
    sys.exit(1)

# ── Konfiguration ────────────────────────────────────────────────────────────

GENERIC_ANCHORS = {
    "mehr erfahren", "hier", "here", "mehr", "more", "weiter", "klicken",
    "click", "lesen", "read", "weiterlesen", "jetzt", "link", "seite",
    "info", "details", "ansehen", "anzeigen", "entdecken", "lesen >",
    "zum anbieter", "jetzt vergleichen", "quelle ansehen",
}

TARGETS = {
    "content_link_share_pct":   {"label": "Content-Link-Anteil %", "3m": 35,  "6m": 40,  "lib": False},
    "generic_anchor_share_pct": {"label": "Generisch-Anchor %",    "3m": 3,   "6m": 1,   "lib": True},
    "orphan_count":             {"label": "Seiten ohne Inlink",     "3m": 0,   "6m": 0,   "lib": True},
}

BASELINE_FILE = "linking_baseline.json"
HISTORY_FILE  = "linking_history.json"

# ── Laden ────────────────────────────────────────────────────────────────────

def load_csv(path):
    for enc in ("utf-8-sig", "latin-1", "cp1252"):
        try:
            df = pd.read_csv(path, encoding=enc, sep=None, engine="python")
            print(f"  Geladen: {Path(path).name}  ({len(df):,} Zeilen)")
            return df
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Encoding konnte nicht erkannt werden: {path}")

# ── Analyse Links ─────────────────────────────────────────────────────────────

def analyse_links(path):
    df = load_csv(path)

    df = df.rename(columns={
        "Quelle": "source", "Ziel": "dest", "Anker": "anchor",
        "Linkposition": "position", "Follow": "follow",
        "Status-Code": "status_code",
    })

    df_f = df[
        (df["follow"].astype(str).str.upper().isin(["WAHR", "TRUE"])) &
        (df["status_code"] == 200)
    ].copy()

    total   = len(df_f)
    pos     = df_f["position"].value_counts()
    nav     = int(pos.get("Navigation", 0))
    content = int(pos.get("Inhalt", 0))
    footer  = int(pos.get("Fußzeile", pos.get("Fu\x9a§zeile", pos.get("Fusszeile", 0))))
    header  = int(pos.get("Kopf", 0)) + int(pos.get("Header", 0))
    aside   = int(pos.get("Aside", 0))

    inlinks_all     = df_f.groupby("dest").size().reset_index(name="inlinks")
    content_df      = df_f[df_f["position"] == "Inhalt"].copy()
    content_inlinks = content_df.groupby("dest").size().reset_index(name="content_inlinks")

    all_dests = pd.DataFrame({"dest": df_f["dest"].unique()})
    all_dests = all_dests.merge(inlinks_all,     on="dest", how="left").fillna(0)
    all_dests = all_dests.merge(content_inlinks, on="dest", how="left").fillna(0)
    all_dests["inlinks"]         = all_dests["inlinks"].astype(int)
    all_dests["content_inlinks"] = all_dests["content_inlinks"].astype(int)
    orphans = all_dests[all_dests["inlinks"] == 0]

    content_df["anchor_lower"] = content_df["anchor"].astype(str).str.lower().str.strip()
    gen_mask  = content_df["anchor_lower"].isin(GENERIC_ANCHORS)
    gen_count = int(gen_mask.sum())
    gen_share = round(gen_count / content * 100, 1) if content else 0

    top_anchors = content_df["anchor"].value_counts().head(25)

    anchor_div = content_df.groupby("dest")["anchor"].agg(["nunique","count"]).reset_index()
    anchor_div.columns = ["dest", "unique_anchors", "total_links"]
    mono = anchor_div[(anchor_div["unique_anchors"] == 1) & (anchor_div["total_links"] >= 3)]

    outlinks = df_f.groupby("source")["dest"].nunique().reset_index(name="unique_outlinks")
    dilution = outlinks[outlinks["unique_outlinks"] > 40].sort_values("unique_outlinks", ascending=False)

    return {
        "total": total, "nav": nav, "content": content,
        "footer": footer, "header": header, "aside": aside,
        "all_dests": all_dests, "orphans": orphans,
        "content_df": content_df, "top_anchors": top_anchors,
        "mono": mono, "dilution": dilution,
        "gen_count": gen_count, "gen_share": gen_share,
    }

# ── Analyse HTML-Pages ───────────────────────────────────────────────────────

def analyse_html_pages(path, all_dests):
    df = load_csv(path)

    col_map = {}
    for col in df.columns:
        lc = col.lower().strip()
        if lc in ("adresse", "address", "url"):
            col_map[col] = "url"
        elif "tiefe" in lc or "depth" in lc:
            col_map[col] = "depth"
    df = df.rename(columns=col_map)

    if "url" not in df.columns:
        # Fallback: first column is usually the URL
        df = df.rename(columns={df.columns[0]: "url"})

    for status_col in ("Status Code", "Status-Code", "status_code", "Statuscode"):
        if status_col in df.columns:
            df = df[pd.to_numeric(df[status_col], errors="coerce") == 200].copy()
            break

    if "depth" not in df.columns:
        df["depth"] = None

    df["depth"] = pd.to_numeric(df["depth"], errors="coerce")

    pages = df[["url", "depth"]].copy()
    pages = pages.merge(
        all_dests[["dest", "content_inlinks"]].rename(columns={"dest": "url"}),
        on="url", how="left"
    ).fillna({"content_inlinks": 0})
    pages["content_inlinks"] = pages["content_inlinks"].astype(int)

    indexable       = len(pages)
    median_inlinks  = round(float(pages["content_inlinks"].median()), 1) if indexable else 0
    mean_inlinks    = round(float(pages["content_inlinks"].mean()),   1) if indexable else 0

    deep_underlinked = pd.DataFrame()
    if pages["depth"].notna().any():
        deep_underlinked = pages[
            (pages["depth"] >= 4) & (pages["content_inlinks"] <= 3)
        ].sort_values("content_inlinks")

    return {
        "pages": pages, "indexable": indexable,
        "median_inlinks": median_inlinks, "mean_inlinks": mean_inlinks,
        "deep_underlinked": deep_underlinked,
    }

# ── Analyse GSC ──────────────────────────────────────────────────────────────

def analyse_gsc(path, all_dests):
    df = load_csv(path)

    col_map = {}
    for col in df.columns:
        lc = col.lower().strip()
        if any(k in lc for k in ("seite", "page", "ziel", "adresse", "address")):
            if "url" not in col_map.values():
                col_map[col] = "url"
        elif any(k in lc for k in ("link", "intern")):
            if "gsc_links" not in col_map.values():
                col_map[col] = "gsc_links"
    df = df.rename(columns=col_map)

    if "url" not in df.columns:
        df = df.rename(columns={df.columns[0]: "url"})
    if "gsc_links" not in df.columns:
        num_cols = [c for c in df.columns if c != "url" and pd.api.types.is_numeric_dtype(df[c])]
        if num_cols:
            df = df.rename(columns={num_cols[0]: "gsc_links"})
        else:
            print("  WARNUNG: Keine Link-Zahl-Spalte in --gsc Export gefunden.")
            return None

    df["gsc_links"] = pd.to_numeric(df["gsc_links"], errors="coerce").fillna(0).astype(int)
    df = df.sort_values("gsc_links", ascending=False).reset_index(drop=True)

    content_map = all_dests.set_index("dest")["content_inlinks"].to_dict()
    df["content_inlinks"] = df["url"].map(content_map).fillna(0).astype(int)

    df["rank_gap"] = (df["gsc_links"] / (df["content_inlinks"] + 1)).round(1)
    priority_gaps = df[df["content_inlinks"] < df["gsc_links"] * 0.3].sort_values("rank_gap", ascending=False)

    return {"gsc_df": df, "priority_gaps": priority_gaps}

# ── Report ───────────────────────────────────────────────────────────────────

def delta(cur, prev, lib=False):
    if prev is None: return ""
    diff = cur - prev
    if diff == 0: return "  ±0"
    good = (diff < 0) if lib else (diff > 0)
    return f"  {'↑' if diff>0 else '↓'} {'+' if diff>0 else ''}{diff:.1f} {'✓' if good else '✗'}"

def print_report(kpis, link_data, html_data=None, gsc_data=None, baseline=None):
    b = baseline or {}
    t = kpis["total_links"]

    print("\n" + "=" * 62)
    print(f"  SF LINKING REPORT  ·  {kpis['month']}")
    print("=" * 62)

    print("\n── LINK-VERTEILUNG ──────────────────────────────────────────")
    print(f"  Gesamt (follow, 200er):  {t:>8,}")
    for label, val in [
        ("Navigation",  kpis["nav_links"]),
        ("Content",     kpis["content_links"]),
        ("Fußzeile",    kpis["footer_links"]),
        ("Header/Kopf", kpis["header_links"]),
        ("Aside",       kpis["aside_links"]),
    ]:
        pct = f"{val/t*100:.1f}%" if t else "–"
        bar = "█" * int(val / t * 24) if t else ""
        print(f"  {label:<14} {val:>8,}  {pct:>6}  {bar}")

    print(f"\n── ZIEL-URLs & ORPHANS ──────────────────────────────────────")
    print(f"  Unique Ziel-URLs:        {kpis['unique_dest_urls']:>8,}")
    print(f"  Ohne Inlink (Orphan):    {kpis['orphan_count']:>8,}{delta(kpis['orphan_count'], b.get('orphan_count'), lib=True)}")
    for _, row in link_data["orphans"].iterrows():
        print(f"    → {row['dest'].replace('https://dsl.preisvergleich.de','')}")

    if html_data:
        print(f"\n── SEITEN-TIEFE & INLINKS ───────────────────────────────────")
        print(f"  Indexierbare Seiten:     {html_data['indexable']:>8,}")
        print(f"  Median Content-Inlinks:  {html_data['median_inlinks']:>8}{delta(html_data['median_inlinks'], b.get('median_unique_inlinks'))}")
        deep = html_data["deep_underlinked"]
        if len(deep):
            print(f"  Tiefe 4+ schwach (≤3):   {len(deep):>8,}{delta(len(deep), b.get('deep_underlinked'), lib=True)}")
            for _, row in deep.head(10).iterrows():
                depth_str = str(int(row['depth'])) if pd.notna(row['depth']) else '?'
                print(f"    Tiefe {depth_str}  {row['url'].replace('https://dsl.preisvergleich.de','')}")

    print(f"\n── ANCHOR-ANALYSE (Content-Links) ───────────────────────────")
    print(f"  Generisch:               {kpis['generic_anchor_count']:>8,}  ({kpis['generic_anchor_share_pct']}%){delta(kpis['generic_anchor_share_pct'], b.get('generic_anchor_share_pct'), lib=True)}")
    print(f"\n  Top Anchors:")
    for anchor, count in link_data["top_anchors"].head(15).items():
        tag = " ⚠" if str(anchor).lower().strip() in GENERIC_ANCHORS else ""
        print(f"    {count:>5}×  {anchor}{tag}")

    mono = link_data["mono"]
    if len(mono):
        print(f"\n── EINTÖNIGE ANCHORS ({len(mono)} Seiten) ───────────────────────")
        cdf = link_data["content_df"]
        for _, row in mono.head(12).iterrows():
            sample = cdf[cdf["dest"] == row["dest"]]["anchor"].iloc[0]
            tag    = " ⚠" if str(sample).lower().strip() in GENERIC_ANCHORS else ""
            short  = row["dest"].replace("https://dsl.preisvergleich.de","")
            print(f"    {int(row['total_links']):>3}×  '{sample}'{tag}  →  {short}")

    dil = link_data["dilution"]
    if len(dil):
        print(f"\n── LINK DILUTION >40 Outlinks ({len(dil)} Seiten) ───────────────")
        for _, row in dil.head(10).iterrows():
            print(f"    Out={int(row['unique_outlinks'])}  {row['source'].replace('https://dsl.preisvergleich.de','')}")

    if gsc_data:
        gaps = gsc_data["priority_gaps"]
        if len(gaps):
            print(f"\n── PRIORITÄTS-GAPS ({len(gaps)} Seiten) ──────────────────────────")
            print(f"  {'URL':<55} {'GSC':>5}  {'Content':>7}  {'Gap':>6}")
            for _, row in gaps.head(10).iterrows():
                short = row["url"].replace("https://dsl.preisvergleich.de","")[:54]
                print(f"  {short:<55} {int(row['gsc_links']):>5}  {int(row['content_inlinks']):>7}  {row['rank_gap']:>6.1f}")

    print(f"\n── ZIELABGLEICH ─────────────────────────────────────────────")
    print(f"  {'KPI':<28} {'Ist':>7}  {'3M':>5}  {'6M':>5}")
    print(f"  {'-'*28}  {'-'*7}  {'-'*5}  {'-'*5}")
    for key, cfg in TARGETS.items():
        val = kpis.get(key, "–")
        t3, t6, lib = cfg["3m"], cfg["6m"], cfg["lib"]
        ok   = (val <= t3) if lib else (val >= t3)
        flag = "✓" if ok else "✗"
        print(f"  {cfg['label']:<28} {str(val):>7}  {str(t3):>5}  {str(t6):>5}  {flag}")

    print("\n" + "=" * 62 + "\n")

# ── Baseline & History ───────────────────────────────────────────────────────

def load_baseline():
    if Path(BASELINE_FILE).exists():
        with open(BASELINE_FILE) as f:
            return json.load(f)
    return None

def save_baseline(kpis):
    with open(BASELINE_FILE, "w") as f:
        json.dump(kpis, f, indent=2, ensure_ascii=False)
    print(f"  Baseline gespeichert → {BASELINE_FILE}")

def update_history(kpis):
    history = []
    if Path(HISTORY_FILE).exists():
        with open(HISTORY_FILE) as f:
            history = json.load(f)
    history = [h for h in history if h.get("month") != kpis["month"]]
    history.append(kpis)
    history.sort(key=lambda x: x["month"])
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print(f"  Verlauf gespeichert  → {HISTORY_FILE}")

# ── CSV-Export ───────────────────────────────────────────────────────────────

def export_csvs(link_data, html_data, gsc_data, month, out_dir):
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    exports = [
        ("orphans",      link_data["orphans"],  {"dest": "url"}),
        ("dilution",     link_data["dilution"], {"source": "url", "unique_outlinks": "unique_outlinks"}),
        ("mono_anchors", link_data["mono"],      {"dest": "url", "total_links": "total_links", "unique_anchors": "unique_anchors"}),
    ]

    if html_data and len(html_data["deep_underlinked"]):
        exports.append(("deep_underlinked", html_data["deep_underlinked"][["url","depth","content_inlinks"]], {}))

    if gsc_data and len(gsc_data["priority_gaps"]):
        exports.append(("priority_gaps", gsc_data["priority_gaps"][["url","gsc_links","content_inlinks","rank_gap"]], {}))

    for name, df, rename in exports:
        if not len(df): continue
        out = f"{out_dir}/{month}_{name}.csv"
        df.rename(columns=rename).to_csv(out, index=False)
        print(f"  {name:<22} → {out}")

# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="SF Internal Linking Monitor")
    p.add_argument("--links",         required=True, help="All Internal Links CSV (Bulk Export → Links → All Internal Links)")
    p.add_argument("--html",          default=None,  help="HTML-Seiten Export (Internal → Tab 'HTML' → Export)")
    p.add_argument("--gsc",           default=None,  help="GSC Top-Zielseiten CSV (GSC → Links → Interne Links → Top Zielseiten)")
    p.add_argument("--month",         default=datetime.now().strftime("%Y-%m"))
    p.add_argument("--save-baseline", action="store_true")
    p.add_argument("--export-csv",    action="store_true")
    p.add_argument("--out-dir",       default="reports")
    args = p.parse_args()

    baseline = load_baseline()
    if baseline:
        print(f"\n  Baseline: {BASELINE_FILE} (Monat: {baseline.get('month','?')})")
    else:
        print(f"\n  Kein Baseline gefunden — wird nach diesem Lauf angelegt.")

    link_data = analyse_links(args.links)

    html_data = analyse_html_pages(args.html, link_data["all_dests"]) if args.html else None
    gsc_data  = analyse_gsc(args.gsc, link_data["all_dests"])         if args.gsc  else None

    t       = link_data["total"]
    content = link_data["content"]

    kpis = {
        "month":                    args.month,
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

    print_report(kpis, link_data, html_data, gsc_data, baseline)

    if args.save_baseline or baseline is None:
        save_baseline(kpis)

    update_history(kpis)

    if args.export_csv:
        print("── CSV-EXPORT ───────────────────────────────────────────────")
        export_csvs(link_data, html_data, gsc_data, args.month, args.out_dir)
        print()

if __name__ == "__main__":
    main()
