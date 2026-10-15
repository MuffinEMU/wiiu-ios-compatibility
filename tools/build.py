#!/usr/bin/env python3
"""Rebuilds the game table in README.md from data/games.json.

Run:    python3 tools/build.py          (rewrites README.md between the markers)
Check:  python3 tools/build.py --check  (exits 1 if README.md is out of date; CI uses this)

Copyright (c) 2026 MuffinEMU Development Team (Void). SPDX-License-Identifier: GPL-3.0-only
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!-- GAMES:START -->", "<!-- GAMES:END -->"

def load():
    with open(os.path.join(ROOT, "data", "games.json"), encoding="utf-8") as f:
        data = json.load(f)
    slugs = [g["slug"] for g in data["games"]]
    assert len(slugs) == len(set(slugs)), "duplicate slug in data/games.json"
    for g in data["games"]:
        assert g["status"] in data["statuses"], f'{g["slug"]}: unknown status {g["status"]}'
        assert re.fullmatch(r"[a-z0-9-]+", g["slug"]), f'{g["slug"]}: slug must be lowercase letters, digits and dashes'
    return data

def cell(text):
    return text.replace("|", "/").replace("\n", " ").strip()

def report_text(r):
    """One report as a short sentence: 'iPhone 16: 60 fps. Note.'"""
    device = "" if r["device"].lower() in ("", "not stated") else r["device"]
    fps = r["fps"].strip()
    if fps.lower() in ("", "not stated", "n/a"):
        fps = ""
    elif any(c.isdigit() for c in fps):
        fps += " fps"
    head = ": ".join(p for p in (device, fps) if p)
    parts = [p for p in (head, r["note"].strip().rstrip(".")) if p]
    return cell(". ".join(parts) + ".") if parts else "No details."

def table(data):
    labels = data["statuses"]
    out = ["| Game | Status | Reports | Footage |", "|---|---|---|---|"]
    for g in sorted(data["games"], key=lambda g: g["name"].lower()):
        reps = "<br>".join(report_text(r) for r in g["reports"]) or "No details yet"
        foot = ", ".join(f"[{i + 1}]({u})" for i, u in enumerate(g["footage"])) or "Wanted"
        out.append(f'| **{cell(g["name"])}** | {labels[g["status"]]} | {reps} | {foot} |')
    return "\n".join(out)

def main():
    data = load()
    path = os.path.join(ROOT, "README.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), START + "\n" + table(data) + "\n" + END, text, flags=re.S)
    if "--check" in sys.argv:
        if new != text:
            print("README.md is out of date. Run: python3 tools/build.py")
            sys.exit(1)
        print("README.md is up to date")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    print(f'{len(data["games"])} games written to README.md')

if __name__ == "__main__":
    main()
