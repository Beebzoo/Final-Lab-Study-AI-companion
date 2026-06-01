#!/usr/bin/env python3
"""
Add a `transcript` column to the SPSS file by matching each participant's
Sona ID to their Word-document conversation transcript(s).

Matching rule:
  - The ID is the part of the filename before the first dash.
  - IDs are compared with leading zeros stripped, so doc "001" == SPSS "1".
  - If a participant has multiple matching docs, all transcripts are
    concatenated into the one cell, separated by a clear marker.
  - Participants with no doc (and docs with no participant) get reported.
"""
import glob
import os
import sys

import pyreadstat
from docx import Document

SAV_IN = "Final Lab study AI companions.sav"
SAV_OUT = "Final Lab study AI companions.sav"  # overwrite in place
DOC_FOLDERS = ["Rob P1", "Rob P2"]
OVERVIEW_TXT = "missing_transcripts_overview.txt"
SPSS_STR_LIMIT = 32767  # SPSS hard limit for a string variable (bytes)


def norm(raw):
    """Normalise an ID for matching: strip whitespace and leading zeros."""
    s = str(raw).strip()
    return s.lstrip("0") or "0"


def docx_text(path):
    """Extract full text from a .docx as newline-joined paragraphs."""
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def main():
    df, meta = pyreadstat.read_sav(SAV_IN)

    # --- index the Word documents by normalised ID -------------------------
    docs = {}  # norm_id -> list of (filename, path)
    for folder in DOC_FOLDERS:
        for path in sorted(glob.glob(os.path.join(folder, "*.docx"))):
            base = os.path.splitext(os.path.basename(path))[0]
            docs.setdefault(norm(base.split("-")[0]), []).append(
                (os.path.basename(path), path)
            )

    # --- build the transcript column ---------------------------------------
    transcripts = []
    matched_doc_ids = set()
    longest = 0
    for raw_id in df["ID"]:
        key = norm(raw_id)
        if key in docs:
            matched_doc_ids.add(key)
            files = docs[key]
            parts = []
            for i, (fname, path) in enumerate(files):
                header = "" if len(files) == 1 else f"===== FILE {i + 1} of {len(files)}: {fname} =====\n"
                parts.append(header + docx_text(path))
            text = "\n\n".join(parts)
        else:
            text = ""
        longest = max(longest, len(text.encode("utf-8")))
        transcripts.append(text)

    if longest > SPSS_STR_LIMIT:
        print(f"WARNING: longest transcript is {longest} bytes, "
              f"exceeds SPSS limit {SPSS_STR_LIMIT}. It will be truncated by SPSS.",
              file=sys.stderr)

    df["transcript"] = transcripts

    # --- preserve existing metadata, add a label for the new column --------
    col_labels = dict(zip(meta.column_names, meta.column_labels))
    col_labels["transcript"] = "Full conversation transcript (matched by Sona ID)"

    write_kwargs = dict(
        column_labels=col_labels,
        variable_value_labels=meta.variable_value_labels,
    )
    # keep original SPSS display formats (dates, etc.); transcript is inferred
    if getattr(meta, "original_variable_types", None):
        write_kwargs["variable_format"] = dict(meta.original_variable_types)
    if getattr(meta, "variable_measure", None):
        write_kwargs["variable_measure"] = dict(meta.variable_measure)

    pyreadstat.write_sav(df, SAV_OUT, **write_kwargs)

    # --- missing overview ---------------------------------------------------
    sav_keys = {norm(x): str(x).strip() for x in df["ID"]}
    missing_doc = sorted((sav_keys[k] for k in (set(sav_keys) - matched_doc_ids)),
                         key=lambda s: (len(s), s))
    orphan_docs = {k: docs[k] for k in (set(docs) - set(sav_keys))}
    dup_ids = {k: v for k, v in docs.items() if k in matched_doc_ids and len(v) > 1}

    lines = []
    lines.append("MISSING TRANSCRIPTS OVERVIEW")
    lines.append("=" * 60)
    lines.append(f"SPSS rows: {len(df)}   Word docs: {sum(len(v) for v in docs.values())}")
    lines.append(f"Participants matched to a transcript: {len(matched_doc_ids)}")
    lines.append("")
    lines.append(f"1) SPSS participants WITH NO Word document ({len(missing_doc)}):")
    lines.append("   (transcript cell left blank)")
    for i in missing_doc:
        lines.append(f"     - {i}")
    lines.append("")
    lines.append(f"2) Word documents WITH NO matching SPSS participant ({len(orphan_docs)}):")
    lines.append("   (not added to the file)")
    for k in sorted(orphan_docs):
        for fname, _ in orphan_docs[k]:
            lines.append(f"     - {fname}  (ID {k})")
    lines.append("")
    lines.append(f"3) Participants with MULTIPLE documents (all concatenated) ({len(dup_ids)}):")
    for k in sorted(dup_ids):
        lines.append(f"     - ID {sav_keys[k]}: " + ", ".join(f for f, _ in dup_ids[k]))

    report = "\n".join(lines)
    with open(OVERVIEW_TXT, "w", encoding="utf-8") as fh:
        fh.write(report + "\n")
    print(report)
    print(f"\nSaved updated SPSS file -> {SAV_OUT}")
    print(f"Saved overview          -> {OVERVIEW_TXT}")


if __name__ == "__main__":
    main()
