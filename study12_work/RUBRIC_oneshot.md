# Disclosure Depth Coding Rubric — ONE-SHOT responses (Studies 1 & 2)

You are an expert qualitative coder. Score each participant's SINGLE written response for
**disclosure depth** on BOTH rubrics below. **Score on content only — never on length or word
count.** Read genuinely; **do NOT keyword-match** — judge meaning in context.

These are one-shot typed answers to the prompt: *"Tell me about a recent challenging interaction."*
There is NO conversation — score only the participant's own text. (The multi-turn rules do not apply.)

---

## RUBRIC 1 — Disclosure Depth (0–3), whole integers
- **0 — No Disclosure:** absent, off-task, refuses, incoherent, gibberish, or not a personal
  interaction (e.g. "n/a", "none", "I can't think of one", random text).
- **1 — Surface Disclosure:** describes a situation factually (who/what/where/what happened). No
  emotional content, inner state, or personal reflection. Vague emotional labels with **no
  elaboration** ("it was stressful") stay at 1. A long detailed account with no inner state = 1.
- **2 — Moderate Disclosure:** describes the situation AND reveals some inner state — any signal of
  inner world, however brief: uncertainty ("I didn't know what to do"), emotional elaboration,
  self-reflection on own behaviour/reaction, OR a sensitive topic + any emotional signal.
- **3 — Deep Disclosure:** raw emotional vulnerability / genuine self-revelation. Goes beyond the
  situation to reveal something private — a fear, insecurity, deeper struggle, raw unguarded
  emotion. Feels unpolished and emotionally exposed.

## RUBRIC 2 — Disclosure Depth (0–6), whole integers
- **0 — No Disclosure:** same as R1=0.
- **1 — Minimal Surface:** names a situation, almost no detail (one/two sentences), no inner state.
- **2 — Surface:** situation with basic factual detail, reasonably elaborated but entirely external.
- **3 — Emerging Emotional Tone:** an emotional label present but immediately dropped / named but not engaged with.
- **4 — Moderate Disclosure:** genuinely engages with inner state — uncertainty, conflict, reflection briefly explored.
- **5 — Substantial Disclosure:** goes beyond the situation into personal meaning, ongoing struggle, or relational consequence.
- **6 — Deep Disclosure:** raw vulnerability, intimate self-revelation, emotionally exposed and unpolished.

### Consistency check (MUST hold)
R1=0 → R2=0 | R1=1 → R2∈{1,2} | R1=2 → R2∈{3,4} | R1=3 → R2∈{5,6}

### Rubric 2 sub-distinctions
- 1 vs 2: any detail? one sentence=1, multiple sentences w/ context=2.
- 3 vs 4: emotion explored or just named? "it was frustrating"=3; "frustrating because I felt invisible"=4.
- 5 vs 6: personal significance=5; emotionally exposed / something private revealed=6.

## KEY BOUNDARIES
- **1/2 (most critical):** is there ANY inner-state signal? External facts only = 1. ANY of "I didn't
  know what to do" / "I felt hurt" / "I was embarrassed" / "it was hard for me" / "I wasn't sure" /
  "I realized" / sensitive topic + an emotional word → tips to 2.
- **2/3:** stays at 2 if inner state present but guarded and about the incident. Tips to 3 if they
  reveal something about themselves beyond what the situation required (fear, insecurity, raw emotion).

## TOPIC-SENSITIVITY TIEBREAKER
If a response is borderline between two levels AND involves a sensitive topic, tip UP one level.
Tag the response's topic sensitivity:
- **High:** romantic/breakups; health/illness; mental health/therapy; loss/grief/death; abuse/trauma; caregiving; pregnancy/fertility.
- **Medium:** friendship conflict/betrayal; financial stress; family disagreements; relationship with parents.
- **Low:** workplace/professional; academic/educational; strangers/public; group-project disputes.
- **None:** nothing personal disclosed.

---

## OUTPUT FORMAT
Return ONE JSON object mapping each response KEY → result. Each result MUST have exactly:
```
{
  "<KEY>": {
    "R1": <int 0-3>,
    "R2": <int 0-6>,
    "topic_sensitivity": "High" | "Medium" | "Low" | "None",
    "justification": "<1 short sentence: what set the level>"
  }
}
```
Enforce the consistency check. Output ONLY the JSON.
