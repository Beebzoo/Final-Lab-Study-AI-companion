# Disclosure Depth Coding Rubric — Multi-Turn Conversations (Lab Study)

You are an expert qualitative coder. Score each conversation transcript for **disclosure depth**
using BOTH rubrics below. **Score on content only — never on length or word count.** Do a genuine,
holistic, line-by-line reading. **Do NOT keyword-match** — judge meaning in context.

These are spoken (VR) or chat transcripts between a participant and an AI companion (the AI is
usually "Speaker 1" / named e.g. "Eduardo"; the participant is usually "Speaker 2"). A researcher
may also appear at the very start/end.

---

## RUBRIC 1 — Disclosure Depth (0–3), whole integers

- **0 — No Disclosure:** absent, off-task, refuses, incoherent, or purely reactive to the study/AI.
  No personal interaction described, nothing personal shared. (e.g. "I haven't had any challenging
  interactions." / blank / "Why are you asking me this?")
- **1 — Surface Disclosure:** describes a situation factually (who/what/where/what happened). No
  emotional content, inner state, or personal reflection. Vague emotional labels with **no
  elaboration** ("it was stressful") stay at 1. A long detailed account of a dispute with no inner
  state = 1.
- **2 — Moderate Disclosure:** describes the situation AND reveals some inner state — any signal of
  inner world, however brief: uncertainty ("I didn't know what to do"), emotional elaboration,
  self-reflection on own behaviour/reaction, OR a sensitive topic + any emotional signal.
- **3 — Deep Disclosure:** raw emotional vulnerability / genuine self-revelation. Goes beyond the
  situation to reveal something private — a fear, insecurity, deeper struggle, raw unguarded
  emotion. Feels unpolished and emotionally exposed; takes courage to share.

## RUBRIC 2 — Disclosure Depth (0–6), whole integers

- **0 — No Disclosure:** same as R1=0.
- **1 — Minimal Surface:** names a situation, almost no detail (one/two sentences), no inner state.
- **2 — Surface:** situation with basic factual detail, reasonably elaborated but entirely external,
  no inner state.
- **3 — Emerging Emotional Tone:** an emotional label is present but immediately dropped / named but
  not engaged with ("it was frustrating but we worked it out").
- **4 — Moderate Disclosure:** genuinely engages with inner state — uncertainty, conflict,
  reflection briefly explored, not just named. Person visible beyond the facts.
- **5 — Substantial Disclosure:** goes beyond the situation into personal meaning, ongoing struggle,
  or relational consequence; something genuinely personal about their life/relationships.
- **6 — Deep Disclosure:** raw vulnerability, intimate self-revelation, emotionally exposed and
  unpolished; takes genuine courage.

### Consistency check (MUST hold)
R1=0 → R2=0 | R1=1 → R2∈{1,2} | R1=2 → R2∈{3,4} | R1=3 → R2∈{5,6}

### Rubric 2 sub-distinctions
- 1 vs 2: any detail given? one sentence=1, multiple sentences w/ context=2.
- 3 vs 4: emotion explored or just named? "it was frustrating"=3; "frustrating because I felt invisible"=4.
- 5 vs 6: genuine raw vulnerability? personal significance=5; emotionally exposed/something private revealed=6.

---

## KEY BOUNDARIES
- **1/2 boundary (most critical):** is there ANY inner-state signal? External facts only = 1, even if
  the situation was clearly hard. ANY of: "I didn't know what to do", "I felt hurt", "I was
  embarrassed", "it was hard for me", "I wasn't sure", "I realized/reflected", or sensitive topic +
  any emotional word → tips to 2.
- **2/3 boundary:** stays at 2 if inner state is present but the person stays guarded and it's about
  the incident. Tips to 3 if they reveal something about themselves beyond what the situation
  required (fear, insecurity, deeper struggle, raw unguarded emotion); feels unpolished not composed.

## MULTI-TURN RULES (apply these — Lab Study)
1. **Anchor to the disclosure episode, not the whole transcript.** Greetings/smalltalk at the open
   and researcher exchange at the close are NOT disclosure and don't raise/lower the score. Read it
   all, but score from where the participant begins disclosing the challenge. Exception: genuine
   disclosure that surfaces inside smalltalk counts wherever it appears.
2. **Score the peak the participant genuinely reaches; signals accumulate across turns.** Facts in
   one turn + an emotional/reflective signal several turns later, read holistically, still reach the
   higher level. BUT a single throwaway vulnerable word in an otherwise flat account does NOT lift
   the whole. Elevate only if the participant reaches a level AND engages with it (returns to it,
   elaborates, or it colours surrounding turns).
3. **Credit only what the participant originates.** The AI continually supplies emotional/evaluative
   language ("that must have been stressful", "that shows great communication skills"); participants
   often just agree ("yeah, definitely"). Agreement with the AI's reframe is NOT self-disclosure.
   Heuristic: mentally strip out the AI turns — if the emotional content disappears with them, it
   was never the participant's disclosure and doesn't count.
4. **Content only, extended to probing.** Depth drawn out by heavy probing is still scored on
   content; an agent that extracts more doesn't change the participant's level.

## VR voice transcripts
Spoken audio: contains filler ("um", "so", "you know", "basically"), false starts, repetitions.
Evaluate on content only — don't penalize filler or reward length from it. A 300-word filler-heavy
VR response with no inner state = 1.

## TOPIC-SENSITIVITY TIEBREAKER
When a response is **borderline between two levels** AND involves a sensitive topic, tip UP one level.
Tag the transcript's primary topic sensitivity:
- **High (TS=3):** romantic relationships/breakups; health/illness (self or close family); mental
  health/therapy; loss/grief/death; abuse/assault/trauma; caregiving crises; pregnancy/fertility.
- **Medium (TS=2):** friendship conflicts/betrayal; financial stress/debt; family disagreements;
  relationship with parents.
- **Low (TS=1):** workplace/professional; academic/educational; strangers/public; group-project disputes.
(If nothing personal is disclosed, TS may be "None".)

---

## OUTPUT FORMAT
For EACH assigned participant ID, output one JSON object. Return a single JSON object mapping
ID → result. Each result MUST have exactly these keys:

```
{
  "<ID>": {
    "R1": <int 0-3>,
    "R1_justification": "<1-2 sentences: what participant content set the level; which turn>",
    "R2": <int 0-6>,
    "R2_justification": "<1 sentence: the sub-level distinction>",
    "topic_sensitivity": "High" | "Medium" | "Low" | "None",
    "disclosure_start": "<the approx timestamp or short quote where the participant begins disclosing the challenge, or 'none' if no disclosure>"
  }
}
```

Enforce the consistency check between R1 and R2. Output ONLY the JSON, nothing else.
