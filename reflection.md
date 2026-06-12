# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The first time I ran the game it launched fine but was effectively unplayable.
The hints pointed the wrong way — guessing too high told me to "Go HIGHER!" — and
on multi-digit numbers the direction was inconsistent because the secret was
being compared as text on every other turn. Worst of all, once a game ended,
clicking "New Game" left the board stuck on the "you already won / game over"
screen instead of starting fresh. Three concrete bugs stood out: the backwards
hints, the secret changing type mid-game, and the broken "New Game" reset.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Easy difficulty; secret `12` (from Debug panel); guess `18` on an odd-numbered attempt | Outcome "Too High" with a hint to go **lower** | Labeled "Too High" but hint read **"📈 Go HIGHER!"** | No exception; UI showed contradictory hint `📈 Go HIGHER!` |
| Normal difficulty; secret `80` (from Debug panel); first guess `9` (attempt count became 2 → even) | `9 < 80` → "Too Low", hint to go higher | Reported **"Too High"** — `int > str` raised `TypeError`, fallback compared `"9" > "80"` lexicographically (`True`) | `TypeError` caught internally; UI showed wrong hint `📈 Go HIGHER!` |
| Win or lose a game, then click **New Game 🔁** | Fresh playable game: attempts/score/history reset, new secret in current range | Board stayed in `won`/`lost`; next rerun hit `st.stop()` → **could not play**; secret regenerated as `1–100` ignoring difficulty | No error; page rendered "You already won…" / "Game over…" and stopped |

---

## 2. How did you use AI as a teammate?

I used an AI assistant (ChatGPT-style) to explain the bugs and propose fixes, and
I treated every suggestion as a hypothesis to verify rather than a final answer.

**Correct suggestion (accepted).** For the secret-changes-type bug, the AI
correctly identified the root cause: the app reassigned `secret = str(...)` on
even attempts, so `check_guess` compared an `int` to a `str`, raised `TypeError`,
and fell back to a *lexicographic* string comparison where `"9" > "80"` is
`True`. Its fix was to stop changing the type and always pass the integer secret,
then remove the now-dead `try/except` fallback. I accepted it after verifying:
`check_guess(9, 80)` now returns `("Too Low", …)` and a regression test for that
exact case passes.

**Incorrect / misleading suggestion (rejected).** For the backwards-hints bug,
the AI said the comparison logic was reversed and that I should flip the operator
from `if guess > secret` to `if guess < secret`. That sounded reasonable but was
wrong: the operators were fine — only the message *strings* were swapped. Flipping
the operator would make a guess above the secret return the outcome string
`"Too High"` from the `guess < secret` branch, corrupting the very label that
`update_score` and the win/loss flow depend on. I rejected it and instead swapped
the two hint messages, leaving the comparison intact. I confirmed the real fix
with `check_guess(60, 50) == ("Too High", "📉 Go LOWER!")`.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed only when I could (a) reproduce the original wrong
behavior, (b) apply the change, and (c) re-run a test or manual step that now
gave the correct result. For example, I wrote a pytest case
`test_single_digit_guess_below_multi_digit_secret` asserting
`check_guess(9, 80)` returns "Too Low" — it failed against the old lexicographic
logic and passed after the fix, which told me the type-coercion bug was actually
gone and not just hidden. The full suite of 13 tests passes
(`python -m pytest -q` → `13 passed`). AI helped me design the regression tests
by suggesting the specific multi-digit edge cases (9 vs 80, 100 vs 99) that
expose lexicographic comparison, which I would not have thought to isolate.

---

## 4. What did you learn about Streamlit and state?

Streamlit re-runs your entire script top to bottom every time the user interacts
with a widget — clicking a button or typing reruns the whole file. That means
any plain variable is recreated from scratch each run, so anything that must
persist (the secret number, score, attempts, status) has to live in
`st.session_state`, which Streamlit keeps across reruns. A lot of the bugs came
from misusing that model: the secret was mutated on reruns, and "New Game" only
reset part of the persistent state. I'd explain it to a friend as: "the script
runs again every click, so write your durable values into a special dictionary
that survives the rerun."

---

## 5. Looking ahead: your developer habits

The habit I want to keep is writing a failing regression test *before* trusting a
fix — seeing the test go red then green is far more convincing than eyeballing
the UI. Next time I'd give the AI more context up front (the actual file, not
just a description of the symptom) so it stops guessing at root causes and
reasons from the real code. Overall this project made me treat AI-generated code
as a confident first draft that is frequently wrong in subtle, plausible-sounding
ways — useful for speed, but something I have to reproduce and test before I
believe it.
