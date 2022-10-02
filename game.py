#!/usr/bin/env python3
from collections import namedtuple
from itertools import islice

Throw = namedtuple("Throw", "frame strike spare points")


def evaluate_game(game):
    """
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|--||") #Correct Empty Input
    0
    >>> evaluate_game("1-|-5|12|--|9-|2-|--|3-|--|16||") #Normal Game
    30
    >>> evaluate_game("-/|--|--|--|--|--|--|--|--|--||") #Spare
    10
    >>> evaluate_game("X|--|--|--|--|--|--|--|--|--||") #Strike
    10
    >>> evaluate_game("-/|22|--|--|--|--|--|--|--|--||") #Spare (10 + 4 + 2)
    16
    >>> evaluate_game("X|22|-2|--|--|--|--|--|--|--||") #Strike (10 + (2+2) * 2 + 2)
    20
    >>> evaluate_game("X|X|-2|--|--|--|--|--|--|--||") #Two Strikes (10 + 10 + 10 + 2 + 2)
    34
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|5/||7") #Bonus Throw
    17
    >>> evaluate_game("3/|4/|--|--|--|--|--|--|--|--||") #Two Spares normal game
    24
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||72") #Valid Bonus Frames
    19
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|2/||7") #Valid Bonus Frames
    17
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||XX")
    30
    >>> evaluate_game("--|--|--|--|--|--|--|--|X|X||XX")
    60
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||X5")
    25
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||1/")
    20
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||12")
    13
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||7/")
    20
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|1/||2")
    12
    >>> try:
    ...     evaluate_game("--|--|--|--|--|--|--|--|--|X||3")
    ...     assert False
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("--|--|--|--|--|--|--|--|--|X||")
    ...     assert False
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("--|--|--|--|--|--|--|--|--|2/||71") #Valid Bonus Frames
    ...     assert False
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("--|--|--|--|-4|--|--|--|--|--||32") #InValid Bonus Frames
    ...     assert False
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("--|--|--|--|--|--|--|--|--|--|") #Only one pipe in the end
    ...     assert False
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("XX|--|--|--|--|--|--|--|--|--||") #Two strikes in one throw are not possible
    ...     assert False
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("123|--|--|--|--|--|--|--|--|--||") #Three throws in one frame
    ...     assert False
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("--|--|--|--|--|--|--|--|--|X||123") #Three throws in bonus frame (bonus frame is valid)
    ...     assert False
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("--|--|--|--|--|--|--|--|--|X||1")
    ...     assert False
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("--||--|--|--|--|--|--|--|--||--|") #Two pipes before the end
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("/-|--|--|--|--|--|--|--|--|--|--||") #Spare at the start of a frame
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("--|55|--|--|--|--|--|--|--|--||") #Sum of frame equals ten
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("--|57|--|--|--|--|--|--|--|--||") #Sum of frame greater than ten
    ... except Exception:
    ...     pass
    >>> try:
    ...     evaluate_game("--|1|--|--|--|--|--|--|--|--||") #Sum of frame greater than ten
    ... except Exception:
    ...     pass
    """
    score = 0

    for (throw_before_last_throw, last_throw, throw) in iter_over_throws(
        game.split("|"), window_size=3
    ):
        if throw.frame != 12:
            score += throw.points
        if last_throw and (last_throw.spare or last_throw.strike):
            score += throw.points
        if throw_before_last_throw and throw_before_last_throw.strike:
            score += throw.points

    assert not throw.strike
    assert not last_throw.strike
    assert last_throw.frame != 12 or throw.frame != 12 or throw_before_last_throw.strike
    assert last_throw.frame >= 10 or last_throw.spare

    return score


def iter_over_throws(frames, window_size):
    assert len(frames) == 12

    def get_throws():
        for i in range(1, window_size):
            yield None
        for i, frame in enumerate(frames, 1):
            yield from evaluate_frame(number=i, frame=frame)

    yield from window(list(get_throws()), size=window_size)


def window(iterable, size):
    """
    >>> list(window([None, None, 1,2,3], size=3))
    [(None, None, 1), (None, 1, 2), (1, 2, 3)]
    """
    return zip(*[islice(iterable, s, None) for s in range(size)])


def evaluate_frame(number, frame):
    """
    >>> list(evaluate_frame(number=1, frame='X'))
    [Throw(frame=1, strike=True, spare=False, points=10)]

    >>> list(evaluate_frame(number=1, frame='12'))
    [Throw(frame=1, strike=False, spare=False, points=1), Throw(frame=1, strike=False, spare=False, points=2)]

    >>> list(evaluate_frame(number=1, frame='3/'))
    [Throw(frame=1, strike=False, spare=False, points=3), Throw(frame=1, strike=False, spare=True, points=7)]

    >>> list(evaluate_frame(number=12, frame='2'))
    [Throw(frame=12, strike=False, spare=False, points=2)]

    >>> list(evaluate_frame(number=11, frame=''))
    []

    >>> try:
    ...     list(evaluate_frame(number=1, frame='55'))
    ...     assert False
    ... except AssertionError:
    ...     pass

    >>> try:
    ...     list(evaluate_frame(number=1, frame='123'))
    ...     assert False
    ... except Exception:
    ...     pass

    >>> try:
    ...     list(evaluate_frame(number=1, frame='1'))
    ...     assert False
    ... except Exception:
    ...     pass

    >>> try:
    ...     list(evaluate_frame(number=1, frame='/1'))
    ...     assert False
    ... except Exception:
    ...     pass

    >>> try:
    ...     list(evaluate_frame(number=1, frame='XX'))
    ...     assert False
    ... except Exception:
    ...     pass

    >>> try:
    ...     list(evaluate_frame(number=1, frame='//'))
    ...     assert False
    ... except Exception:
    ...     pass

    >>> try:
    ...     list(evaluate_frame(number=11, frame='23'))
    ...     assert False
    ... except Exception:
    ...     pass

    >>> try:
    ...     list(evaluate_frame(number=11, frame='23'))
    ...     assert False
    ... except Exception:
    ...     pass

    # >>> list(evaluate_frame(number=1, frame='XX'))
    # Traceback (most recent call last):
    #     ...
    # Exception: Two Strikes/Spares can't be in the same frame!
    """
    assert frame != "XX" or number == 12

    if number == 11:
        assert frame == ""
        return

    if frame == "X":
        yield Throw(frame=number, strike=True, spare=False, points=10)
        return

    points = 0

    for idx, hit in enumerate(frame):
        if hit == "-":
            yield Throw(frame=number, strike=False, spare=False, points=0)

        elif "1" <= hit <= "9":
            points += int(hit)
            assert points < 10
            yield Throw(frame=number, strike=False, spare=False, points=int(hit))

        elif hit == "/":
            yield Throw(frame=number, strike=False, spare=True, points=10 - points)

        else:
            assert hit == 'X'
            yield Throw(frame=number, strike=False, spare=False, points=10)

        assert idx != 0 or hit != "/"

    assert len(frame) == 2 or number == 12


if __name__ == "__main__":  # pragma: no mutate
    from sys import stdin

    for line in stdin:
        print(evaluate_game(line))
