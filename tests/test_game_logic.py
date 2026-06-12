from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# --- check_guess: normal behavior -------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win.
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # Guess above the secret -> "Too High".
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # Guess below the secret -> "Too Low".
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Regression: Bug 1 (inverted hint direction) ----------------------------

def test_too_high_hint_points_lower():
    # A "Too High" outcome must tell the player to go LOWER.
    _, message = check_guess(60, 50)
    assert "LOWER" in message


def test_too_low_hint_points_higher():
    # A "Too Low" outcome must tell the player to go HIGHER.
    _, message = check_guess(40, 50)
    assert "HIGHER" in message


# --- Regression: Bug 2 (lexicographic comparison on multi-digit numbers) ----

def test_single_digit_guess_below_multi_digit_secret():
    # 9 < 80 numerically. The old code compared "9" > "80" lexicographically
    # and wrongly returned "Too High".
    outcome, _ = check_guess(9, 80)
    assert outcome == "Too Low"


def test_multi_digit_guess_above_secret():
    # 100 > 99 numerically (old lexicographic compare made "100" < "99").
    outcome, _ = check_guess(100, 99)
    assert outcome == "Too High"


# --- parse_guess ------------------------------------------------------------

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True and value == 42 and err is None


def test_parse_empty_is_rejected():
    ok, value, err = parse_guess("")
    assert ok is False and value is None and err


def test_parse_non_number_is_rejected():
    ok, value, err = parse_guess("abc")
    assert ok is False and value is None and err


# --- update_score -----------------------------------------------------------

def test_first_guess_win_scores_full_points():
    assert update_score(0, "Win", 1) == 100


def test_wrong_guess_loses_points():
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too Low", 3) == -5


# --- get_range_for_difficulty -----------------------------------------------

def test_ranges_per_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)
    assert get_range_for_difficulty("Unknown") == (1, 100)
