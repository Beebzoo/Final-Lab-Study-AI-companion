# Project Handover — AI Companion Modality & Self-Disclosure

**Prepared:** 3 June 2026
**Purpose:** Full record of the data preparation, AI coding, and analysis done in this session, so the
project can be continued locally (VS Code) without losing context.

---

## 1. The research question

Across several studies, participants describe a recent **challenging interaction** to an AI companion in
one of two **modalities**:

- **VR** — spoken, in a VR environment (Condition 1)
- **Text** — typed, via a messaging interface (Condition 2)

The core question: **does modality affect how much people self-disclose?** Disclosure is measured two ways:
- **Behavioural disclosure depth** — coded from the participant's words using a rubric (the focus of this session).
- **Self-reported disclosure** — survey items (DC scale), in the studies that have them.

---

## 2. Datasets

| Study | Format | N | Response location | Disclosure scores | Notes |
|-------|--------|---|-------------------|-------------------|-------|
| **Lab Study** | multi-turn conversation | 190 (188 transcripts) | external (Word docs → `Transcripts.xlsx`) | coded this session (DD_R1/R2) | the original `.sav` |
| **Study 5** | multi-turn conversation | 181 (filter→179) | in-file `transcript` | already had `DD_S`/`DD_L` | has rich mediators (IC, AF, PP, …) + `filter_$` |
| **Study 1** | one-shot typed | 265 | in-file `VR_F/VR_M/Text_F/Text_M` | coded this session | no prior DD |
| **Study 2** | one-shot typed | 761 | in-file `VR_M/Text_M` | coded this session (+ existing `DD`) | has `filter_$` |
| **Study 3** | one-shot typed | 414 | in-file `Text_M` (`Final_Full.sav`) | coded this session (+ existing `DD`, `DD1`) | two human raters already present |

> **Important nuance:** the rubric document calls the Lab Study and "Study 3" *multi-turn*, but the
> Study 3 data actually supplied (`Final_Full.sav`, `Text_M`) is **one-shot typed responses**. It was
> therefore coded with the one-shot rules. Confirm this is the intended Study 3 data.

### Modality coding
`Condition` / `Modality`: **1 = VR, 2 = Text** (consistent across files). In Study 1/2 the modality is
inferred from which response column is filled (`VR_*` vs `Text_*`).

---

## 3. The coding rubric (Disclosure Depth)

Two parallel scales, scored on **content only — never length**:

- **Rubric 1 / `DD_S` (0–3):** 0 None · 1 Surface (facts only) · 2 Moderate (any inner state) · 3 Deep (raw vulnerability).
- **Rubric 2 / `DD_L` (0–6):** finer split of the same construct.
- **Consistency check (enforced):** R1=0→R2=0 · R1=1→R2∈{1,2} · R1=2→R2∈{3,4} · R1=3→R2∈{5,6}.
- **Topic-sensitivity tiebreaker:** borderline cases on a sensitive topic (health, grief, abuse, romance,
  finances, family, …) tip up one level. Tagged High/Medium/Low/None.
- **Multi-turn rules (Lab Study):** anchor to the disclosure episode (ignore smalltalk/researcher chatter);
  let signals accumulate across turns; **credit only what the participant originates** (strip the AI's
  emotional reframes — agreement with the AI is not disclosure); probing-extracted depth still counts on content.
- **One-shot rules (Studies 1/2/3):** same base scale, no multi-turn logic (single response).

Full text: `coding_work/RUBRIC.md` (multi-turn) and `study12_work/RUBRIC_oneshot.md` (one-shot).

---

## 4. How the coding was done

Because the brief required a *genuine line-by-line reading, not keyword matching*, every transcript/response
was read and scored by an LLM (Claude) acting as a qualitative coder:

1. Responses/transcripts were exported to individual text files and split into batches.
2. Parallel coding agents each read the rubric and scored their batch, emitting strict JSON
   (`R1`, `R2`, `topic_sensitivity`, `justification`).
3. Results were merged, the **R1↔R2 consistency check was validated (0 violations across all studies)**,
   and the scores were written back into the `.sav` files as new variables.

This replaces the external "GPT Table Worker" tool — no OpenAI key or third-party upload was needed.

---

## 5. Key findings

### 5.1 Main effect — modality on disclosure depth (Lab Study & Study 5)
- **Text participants disclose more deeply than VR participants.** Replicated in both the Lab Study and Study 5.
- **Raw** difference is small (significant on the 0–6 scale, marginal on 0–3).
- **VR participants write ~2× more words** (~322 vs ~149) — and word count is positively related to depth.
  This *suppresses* the text effect in a naïve comparison.
- **Adjusted for word count** (ordinal logistic regression), the text advantage is large:
  - Lab Study: OR ≈ 5 (R1), ≈ 7.7 (R2), both p < .001.
  - Study 5 (filter on): OR ≈ 6 (DD_S), ≈ 7.9 (DD_L), both p < .001.
- **Mechanism:** typing is deliberate and lower-pressure → more disclosure *per word*; speaking produces
  volume (filler, external narration), not depth.

### 5.2 Mediation in Study 5 — why IC / AF / PP "don't work"
- The modality manipulation **does not move any proposed experiential mediator** (information control,
  flow/absorption, presence): all a-paths non-significant, despite **100% correct manipulation recall**.
  With a null a-path, mediation is impossible — this is a genuine, reportable null, not a fixable error.
- **AF scale was unreliable (α = .57)** and redundant with PP (r = .76).
- AF/PP **predict self-reported disclosure (DC)** but not coded depth, and DC vs coded depth correlate only r = .22.
- **Word count** is the only active indirect path — and it is **suppression** (bootstrapped indirect
  −0.84, 95% CI [−1.22, −0.50], opposite sign to the direct effect).

### 5.3 Fixes applied (Study 5)
- **Combined "Immersion" factor** from AF+PP (7 items): one clean factor, **α = 0.85** (replaces the broken AF).
- **Bootstrapped mediation (5,000 resamples):** immersion paths null (CIs include 0); word-count suppression confirmed.

### 5.4 Coding distributions (`DD_S`, 0–3)
- **Lab Study:** 0→10 · 1→60 · 2→100 · 3→18 (n=188)
- **Study 1:** 0→33 · 1→145 · 2→83 · 3→4 (n=265; VR 133 / Text 132)
- **Study 2:** 0→40 · 1→338 · 2→330 · 3→53 (n=761; VR 384 / Text 377)
- **Study 3:** 0→26 · 1→154 · 2→187 · 3→47 (n=414)

### 5.5 AI vs human agreement (validity — Study 3)
Study 3 had two human raters (`DD`, `DD1`):
- Human `DD` vs `DD1`: **r = .90** (88% exact) — reliable human coding.
- AI `DD_S` vs human `DD`: **r = .78** (73% exact, 99.5% within 1 point).
- AI `DD_S` vs human `DD1`: **r = .74** (66% exact).

The AI is a solid third coder; humans agree slightly more with each other, as expected.

---

## 6. File inventory

### Data — delivered `.sav` files
- `Final Lab study AI companions.sav` — Lab Study + `transcript`, `DD_R1`, `DD_R2`, `WordCount`, `TopicSensitivity`; `Condition` labelled VR/Text.
- `Study_1_scored.sav` — + `DD_S`, `DD_L`, `Modality`.
- `Study_2_scored.sav` — + `DD_S`, `DD_L`, `Modality` (existing `DD` kept).
- `Study_3_scored.sav` — + `DD_S`, `DD_L`, `TopicSensitivity` (existing `DD`, `DD1` kept).
- `Study_3_original.sav` — the version without text (DD/DD1 only).
- *(Study 5 `.sav` was analysed from the uploaded copy; not committed.)*

### Spreadsheets
- `Transcripts.xlsx` — Lab Study transcripts matched to ID.
- `Transcripts_participant_only.xlsx` — participant-only columns, word count, and the coded scores + justifications.

### Reports (Word)
- `Modality_Disclosure_Report.docx` — Lab Study main analysis.
- `Study5_Disclosure_Report.docx` — Study 5 (filter on).
- `Study5_Mediation_Diagnostics.docx` — why IC/AF/PP don't mediate.
- `Study5_Fixes_Applied.docx` — Immersion factor + bootstrapped mediation.
- `DISCLOSURE_CODING_METHOD.md` — method note for the Lab Study coding.

### Scripts (reproducible)
| Script | What it does |
|--------|--------------|
| `build_transcripts.py` | Match Word docs → Lab Study `.sav` `transcript` column; missing-ID overview. |
| `extract_participant.py` / `assemble_final.py` | Build participant-only / text-only / word-count columns in the xlsx. |
| `analysis.py` | Lab Study modality analysis + figures + writes DD vars to `.sav`. |
| `study5_analysis.py` | Study 5 analysis (filter on) + figures. |
| `build_report.py`, `build_study5_report.py`, `build_mediation_doc.py`, `build_fixes_doc.py` | Generate the Word reports. |

### Working directories (intermediate coding artifacts)
- `coding_work/` — Lab Study: `RUBRIC.md`, per-batch + merged scores (`all_scores.json`), transcripts.
- `study12_work/` — Studies 1&2: `RUBRIC_oneshot.md`, extracted responses, batches, scores.
- `study3_work/` — Study 3: responses, batches, `all_scores.json`.

### Source docs
- `Rob P1/`, `Rob P2/` — 188 Lab Study conversation Word docs (filenames = Sona IDs).

---

## 7. Continuing locally — setup

```bash
# Python 3.11+
pip install pyreadstat pandas openpyxl python-docx statsmodels matplotlib scipy
```

To reproduce an analysis, e.g. the Lab Study:
```bash
python3 analysis.py        # reads the .sav + scores, writes figures + updates the .sav
python3 build_report.py    # builds the Word report
```

Reading an SPSS file in Python:
```python
import pyreadstat
df, meta = pyreadstat.read_sav("Study_2_scored.sav")
print(meta.column_names_to_labels)   # variable labels
print(meta.variable_value_labels)    # value labels (e.g. Condition 1=VR,2=Text)
```

> Note: `pyreadstat` preserves variable names, labels, value labels, and display formats, but **not**
> SPSS-specific extras (custom attributes, multiple-response sets, weighting). Open in SPSS to confirm.

---

## 8. Caveats (read before publishing)

1. **LLM single-rater coding.** `DD_S`/`DD_L` are AI-coded. For publication, have a human second-code a
   random subset per study and report inter-rater reliability (weighted κ). Study 3 already gives a strong
   benchmark (AI–human r ≈ .74–.78; human–human r = .90). Each score has a `justification` to support audit.
2. **Report raw AND adjusted results.** The modality effect is small unadjusted and large after the
   word-count adjustment — disclose both; pre-register the word-count-adjusted model as primary.
3. **Word count is a suppressor, not a clean mediator** — describe it correctly (inconsistent mediation).
4. **Mediation nulls are real.** Don't keep swapping mediators until one is significant; report the null.
5. **Decide one primary disclosure outcome a priori** (coded depth vs self-report — they correlate only ~.22).
6. **Confirm the Study 3 data** is the intended one-shot `Text_M` set (rubric implies multi-turn).
7. **Off-task/flagged cases** exist (refusals, AI hallucinations, spam URLs in responses, a self-harm
   provocation in Study 5 id 15253). Coders scored on genuine content; review flagged items manually.

---

## 9. Open / next steps

- [ ] Pool all studies for a combined modality analysis (mini meta-analysis); confirm which studies have a VR arm (Study 3 appears Text-only).
- [ ] Human second-coder subset + κ per study.
- [ ] Write Immersion factor + coded scores into the Study 5 `.sav` for SPSS use.
- [ ] Cross-study validity note (AI vs human agreement table).
- [ ] Decide primary DV; finalise the reframed model (behavioural = word-count/deliberation; subjective = immersion→DC).
- [ ] Reframed write-up: *modality shapes disclosure via deliberateness, not immersion.*

---

## 10. Git

All work is on branch **`claude/zealous-hypatia-6D21B`** of `Beebzoo/Final-Lab-Study-AI-companion`.
The commit history (see `git log`) is a step-by-step record of each stage above.
