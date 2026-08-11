"""Pure game rules - no GUI, easy to unit test."""

SYMBOLS = ("rock", "paper", "scissors")
NAME = {"rock": "Rock", "paper": "Paper", "scissors": "Scissors"}
BEATS = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
WIN_SCORE = 5


def round_winners(choices):
    """Indices that win this round. Empty list means a tie."""
    groups = {}
    for i, c in enumerate(choices):
        groups.setdefault(c, []).append(i)
    kinds = list(groups.keys())
    if len(kinds) == 1 or len(kinds) >= 3:
        return []
    # exactly two distinct symbols -> the one that beats the other
    if BEATS[kinds[0]] == kinds[1]:
        return groups[kinds[0]]
    return groups[kinds[1]]
