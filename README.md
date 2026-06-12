# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

An AI was asked to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, declared it production-ready, and left behind a game that
was unplayable: you couldn't win reliably, the hints lied about direction, and
the secret number changed type mid-game.

## 🎯 Purpose

*Glitchy Guesser* is a Streamlit number-guessing game. The player picks a
difficulty (Easy / Normal / Hard), which sets a numeric range and an attempt
limit. A secret number is generated once and stored in `st.session_state`. Each
turn the player enters a guess; the app parses it, compares it to the secret,
shows a higher/lower hint, updates a score, and tracks attempts. You win by
guessing the secret before running out of attempts. The investigation goal of
this project was to find, document, and fix the bugs that made the game behave
incorrectly.

## 🛠️ Setup & Run

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`

Open the **Developer Debug Info** expander in the app to see the secret number
while testing.

## 🐛 Bugs Found and Fixes Applied

- **Inverted hint direction.** `check_guess` returned "Too High" with the
  message "Go HIGHER!" (and the reverse for low guesses). *Fix:* swapped the two
  hint messages so "Too High" tells the player to go LOWER and "Too Low" tells
  them to go HIGHER. The operators were correct; only the message strings were wrong.
- **Secret changed type on even attempts.** The app stringified the secret on
  even turns, so `check_guess` compared an `int` guess to a `str` secret. That
  raised `TypeError`, fell back to a lexicographic string compare (`"9" > "80"`
  → `True`), and produced wrong hints on multi-digit numbers. *Fix:* removed the
  stringification and the lexicographic fallback so comparisons are always numeric.
- **"New Game" left the board frozen.** It reset only `attempts` and `secret`
  (hardcoded to `1–100`) and never reset `status`, so after a win/loss the next
  rerun hit `st.stop()` and the game was unplayable. *Fix:* "New Game" now clears
  `attempts`, `score`, `status`, and `history`, and reseeds the secret using the
  current difficulty's range.
- **Off-by-one attempts (low-risk extra).** `attempts` started at `1` and was
  incremented before validation, so the counter was wrong and invalid input
  burned a turn. *Fix:* `attempts` starts at `0` and increments only after a
  valid guess.
- **Hardcoded range text (low-risk extra).** The info banner always said
  "between 1 and 100." *Fix:* it now interpolates the active difficulty's range.

The four game-logic functions were refactored out of `app.py` into
`logic_utils.py`, which `app.py` now imports.

## 🧪 Running the Tests

```bash
python -m pytest -q
```

Expected output:

```
.............                                                            [100%]
13 passed in 0.02s
```

## 📸 Demo Walkthrough

A successful session after the fixes (Easy difficulty, secret revealed as `12`
in the Debug panel):

1. Launch with `python -m streamlit run app.py` and select **Easy**. The banner
   reads "Guess a number between 1 and 20. Attempts left: 6".
2. Enter `5` → hint shows "📈 Go HIGHER!" (5 is below 12). Attempts left: 5.
3. Enter `18` → hint shows "📉 Go LOWER!" (18 is above 12). Attempts left: 4.
4. Enter `12` → "🎉 Correct!", balloons, and "You won! The secret was 12."
5. Click **New Game 🔁** → the board resets to a fresh, playable game with a new
   secret inside the Easy range and score back to 0.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest -q
.............                                                            [100%]
13 passed in 0.02s
```

## 🚀 Stretch Features

- [ ] Not attempted. (If added later, document AI usage in `ai_interactions.md`.)
