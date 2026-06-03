#!/usr/bin/env python3
"""Assemble the final spreadsheet with a participant-only column.

VR (spoken) rows  -> reconstructed verbatim from LLM-classified participant
                     segment indices in vr_work/out_*.json.
TEXT (chat) rows  -> regex extraction of the "you" segments (validated).
Blank rows        -> left blank.
Text is never altered; only AI / researcher turns are removed.
"""
import glob
import json
import re
import openpyxl

SRC = "Transcripts.xlsx"
OUT = "Transcripts_participant_only.xlsx"
NEWCOL = "Participant responses (timestamps kept)"

# ---- load VR classification ----
segs = json.load(open("vr_work/vr_segments.json"))
sel = {}
for f in sorted(glob.glob("vr_work/out_*.json")):
    sel.update(json.load(open(f)))


def build_vr(pid):
    by = {s[0]: s for s in segs[pid]}
    return "  ".join(f"{by[i][1]} {by[i][3]}" for i in sorted(sel[pid]) if i in by)


# ---- TEXT extraction (participant label == "you") ----
seg_re = re.compile(r"(\w+)\s*Today at\s*(\d{1,2}:\d{2}\s*[AaPp][Mm])")


def build_text(t):
    out, prev = [], 0
    for m in seg_re.finditer(t):
        label = m.group(1)
        time = re.sub(r"\s+", " ", m.group(2)).strip()
        msg = t[prev:m.start()].strip()
        if label.lower() == "you" and msg:
            msg = re.sub(r"https?://\S*fireflies\S*", "", msg, flags=re.I).strip()
            if msg:
                out.append(f"{time} {msg}")
        prev = m.end()
    return "  ".join(out)


def classify(t):
    has_spk = "Speaker 1" in t or "Speaker 2" in t
    if has_spk and "Today at" not in t:
        return "VR"
    if "Today at" in t and not has_spk:
        return "TEXT"
    return "OTHER"


wb = openpyxl.load_workbook(SRC)
ws = wb.active
header = [c.value for c in ws[1]]
tcol = next(i for i, h in enumerate(header, 1) if h and "transcript" in str(h).lower())
idcol = next(i for i, h in enumerate(header, 1) if str(h).strip().lower() == "id")
new_i = ws.max_column + 1
ws.cell(1, new_i, NEWCOL)

n = {"VR": 0, "TEXT": 0, "BLANK": 0, "OTHER": 0}
for r in range(2, ws.max_row + 1):
    raw = ws.cell(r, tcol).value
    pid = str(ws.cell(r, idcol).value)
    t = (raw or "").strip()
    if not t:
        n["BLANK"] += 1
        continue
    fmt = classify(t)
    n[fmt] += 1
    if fmt == "VR" and pid in sel:
        ws.cell(r, new_i, build_vr(pid))
    elif fmt == "TEXT":
        ws.cell(r, new_i, build_text(t))

wb.save(OUT)
print("wrote", OUT, "| breakdown:", n)
