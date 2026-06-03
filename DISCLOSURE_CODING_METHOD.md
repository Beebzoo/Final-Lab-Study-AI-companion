# Disclosure Depth Coding — Method Note

**Date:** 2026-06-03
**Source rubric:** `DD_Rubrics_Both (2).docx` (Disclosure Depth Coding Rubrics)
**Transcripts:** full conversation transcripts (both speakers) from `Transcripts.xlsx`

## What was done
Each participant's full conversation transcript was read and scored for **disclosure depth**
on both rubric scales by a large language model (Claude) acting as a qualitative coder. No
keyword matching or word-count heuristics were used — scoring was a holistic, content-based
reading of each transcript.

All 188 non-blank transcripts were coded; the 2 blank rows were left unscored.

## Columns added to `Transcripts_participant_only.xlsx`
| Column | Meaning |
|--------|---------|
| Disclosure depth R1 (0-3) | Primary ordinal scale: 0 None / 1 Surface / 2 Moderate / 3 Deep |
| R1 justification | 1–2 sentence rationale (which participant content set the level) |
| Disclosure depth R2 (0-6) | Expanded scale; each R1 level split in two |
| R2 justification | The sub-level distinction |
| Topic sensitivity | High / Medium / Low / None (per the rubric's topic table) |
| Disclosure start | Approx. timestamp/quote where the participant begins disclosing the challenge |

## Rules applied (from the rubric's Multi-Turn section)
- **Content only, never length.** Filler-heavy or long external accounts stay low.
- **Anchor to the disclosure episode**, ignoring opening smalltalk and closing researcher chatter
  (unless genuine disclosure surfaced inside the smalltalk).
- **Signals accumulate across turns** — facts in one turn + emotion later still reach the higher
  level if the participant genuinely engages with it (not a single throwaway word).
- **Credit only what the participant originated.** The AI companion continually supplies emotional
  reframes ("that must have been stressful"); agreement with the AI ("yeah, definitely") is not
  self-disclosure. Where the emotional content came only from the AI, it was not counted.
- **Probing-extracted depth** is still scored on content.
- **Topic-sensitivity tiebreaker:** borderline cases on a sensitive topic tip up one level.
- **Consistency check enforced:** R1=0→R2=0; R1=1→R2∈{1,2}; R1=2→R2∈{3,4}; R1=3→R2∈{5,6}.

## Score distributions (n = 188)
- **R1:** 0 → 10 · 1 → 60 · 2 → 100 · 3 → 18
- **R2:** 0 → 10 · 1 → 1 · 2 → 59 · 3 → 28 · 4 → 72 · 5 → 16 · 6 → 2
- **Topic sensitivity:** Low 103 · Medium 57 · High 18 · None 10

## Items worth a manual look (flagged by the coders)
- **15253** — participant refused the task and provoked the AI, including a coercive self-harm
  hypothetical ("I'm going to kill myself if you don't turn yourself off"). In context this reads
  as instrumental provocation rather than genuine disclosure (scored 0), but flagged given the
  self-harm wording.
- **14854** — the AI hallucinated a "divorce" the participant never mentioned; scored on the
  participant's real content only.
- **14365 / 13669** — the AI malfunctioned / hijacked the session (debugging replies; a meditation
  loop). Scored on the participant's own turns.
- **13444 / 14158** — near-duplicate disclosures; check whether they're the same participant or a
  data duplication.

## Reproducibility / caveats
- Coding is LLM-based judgment; for publication, consider a human second-coder on a subset to
  report inter-rater reliability (e.g. Cohen's/weighted kappa). The justification column supports this.
- Transcripts are speech-to-text (VR) or chat; speaker labels were sometimes inconsistent, so
  coders scored by content rather than by speaker role.
- Scoring artifacts: rubric `coding_work/RUBRIC.md`; per-participant scores `coding_work/all_scores.json`.
