#!/usr/bin/env python3
from collections import namedtuple
from itertools import islice, tee

Throw = namedtuple("Throw", "frame strike spare points")


def evaluate_game(game):
    """
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|--||") #Correct Empty Input
    0
    >>> evaluate_game("1-|-5|12|--|9-|2-|--|3-|--|16||") #Normal Game
    30
    >>> evaluate_game("1/|--|--|--|--|--|--|--|--|--||") #Spare
    10
    >>> evaluate_game("X|--|--|--|--|--|--|--|--|--||") #Strike
    10
    >>> evaluate_game("1/|22|--|--|--|--|--|--|--|--||") #Spare (10 + 4 + 2)
    16
    >>> evaluate_game("X|22|-2|--|--|--|--|--|--|--||") #Strike (10 + (2+2) * 2 + 2)
    20
    >>> evaluate_game("X|X|-2|--|--|--|--|--|--|--||") #Two Strikes (10 + 10 + 10 + 2 + 2)
    34
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|5/||7") #Bonus Throw
    17
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||72") #Valid Bonus Frames
    19
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|2/||7") #Valid Bonus Frames
    17
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||XX")
    30
    >>> evaluate_game("X|X|X|X|X|X|X|X|X|X||XX") # perfect game
    300
    >>> evaluate_game("--|--|--|--|--|--|--|--|X|X||XX")
    60
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||X5")
    25
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||1/")
    20
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||3")
    Traceback (most recent call last):
        ...
    AssertionError: throw before last throw cannot be strike
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||")
    Traceback (most recent call last):
        ...
    AssertionError: last throw cannot be a strike
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|2/||71")
    Traceback (most recent call last):
        ...
    AssertionError: a strike in the last regular frame provides two bonus throws
    >>> evaluate_game("--|--|--|--|-4|--|--|--|--|--||32")
    Traceback (most recent call last):
        ...
    AssertionError: a strike in the last regular frame provides two bonus throws
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|--|")
    Traceback (most recent call last):
        ...
    AssertionError: need to have 10 frames + bonus frame
    >>> evaluate_game("XX|--|--|--|--|--|--|--|--|--||")
    Traceback (most recent call last):
        ...
    AssertionError: two strikes cannot be in the same frame, except in bonus frame
    >>> evaluate_game("123|--|--|--|--|--|--|--|--|--||")
    Traceback (most recent call last):
        ...
    AssertionError: frame need to have length 2, if no strike or bonus frame
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||123")
    Traceback (most recent call last):
        ...
    AssertionError: a strike in the last regular frame provides two bonus throws
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||X1")
    21
    >>> evaluate_game("--|--|--|--|--|--|--|--|--|X||1")
    Traceback (most recent call last):
        ...
    AssertionError: throw before last throw cannot be strike
    >>> evaluate_game("--||--|--|--|--|--|--|--|--||--|")
    Traceback (most recent call last):
        ...
    AssertionError: need to have 10 frames + bonus frame
    >>> evaluate_game("--|55|--|--|--|--|--|--|--|--||")
    Traceback (most recent call last):
        ...
    AssertionError: cannot score 10 or higher, without strike/spare
    >>> evaluate_game("--|1|--|--|--|--|--|--|--|--||")
    Traceback (most recent call last):
        ...
    AssertionError: frame need to have length 2, if no strike or bonus frame
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

    assert not throw.strike, "last throw cannot be a strike"
    assert not last_throw.strike, "throw before last throw cannot be strike"
    assert (
        last_throw.frame != 12 or throw.frame != 12 or throw_before_last_throw.strike
    ), "a strike in the last regular frame provides two bonus throws"
    assert last_throw.frame >= 10 or last_throw.spare

    return score


def iter_over_throws(frames, window_size):
    """
    >>> len(list(iter_over_throws(['--'] * 10 + ['', ''], window_size=3)))
    20
    """
    assert len(frames) == 12, "need to have 10 frames + bonus frame"

    def get_throws():
        for i in range(1, window_size):
            yield None
        for i, frame in enumerate(frames, 1):
            yield from evaluate_frame(number=i, frame=frame)

    yield from window(get_throws(), size=window_size)


def window(iterable, size):
    """
    >>> list(window([None, None, 1,2,3], size=3))
    [(None, None, 1), (None, 1, 2), (1, 2, 3)]
    """
    return zip(
        *[
            islice(iterator, idx, None)
            for idx, iterator in enumerate(tee(iterable, size))
        ]
    )


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
    >>> list(evaluate_frame(number=1, frame='55'))
    Traceback (most recent call last):
        ...
    AssertionError: cannot score 10 or higher, without strike/spare
    >>> list(evaluate_frame(number=1, frame='1'))
    Traceback (most recent call last):
        ...
    AssertionError: frame need to have length 2, if no strike or bonus frame
    >>> list(evaluate_frame(number=1, frame='-/'))
    Traceback (most recent call last):
        ...
    AssertionError: spare cannot be the first throw in a frame
    >>> list(evaluate_frame(number=1, frame='//'))
    Traceback (most recent call last):
        ...
    AssertionError: spare cannot be the first throw in a frame
    >>> list(evaluate_frame(number=11, frame='23'))
    Traceback (most recent call last):
        ...
    AssertionError: bonus frame needs to be empty
    >>> list(evaluate_frame(number=1, frame='XX'))
    Traceback (most recent call last):
        ...
    AssertionError: two strikes cannot be in the same frame, except in bonus frame
    >>> list(evaluate_frame(number=1, frame='1Y'))
    Traceback (most recent call last):
        ...
    AssertionError: Y is an invalid throw
    """
    assert (
        frame != "XX" or number == 12
    ), "two strikes cannot be in the same frame, except in bonus frame"

    if number == 11:
        assert frame == "", "bonus frame needs to be empty"
        return

    if frame == "X":
        yield Throw(frame=number, strike=True, spare=False, points=10)
        return

    points = 0

    for throw in frame:
        if throw == "-":
            yield Throw(frame=number, strike=False, spare=False, points=0)
        elif "1" <= throw <= "9":
            points += int(throw)
            assert points < 10, "cannot score 10 or higher, without strike/spare"
            yield Throw(frame=number, strike=False, spare=False, points=int(throw))
        elif throw == "/":
            assert points > 0, "spare cannot be the first throw in a frame"
            yield Throw(frame=number, strike=False, spare=True, points=10 - points)
        else:
            assert throw == "X", f"{throw} is an invalid throw"
            yield Throw(frame=number, strike=False, spare=False, points=10)

    assert (
        len(frame) == 2 or number == 12
    ), "frame need to have length 2, if no strike or bonus frame"


if __name__ == "__main__":  # pragma: no mutate  # pragma: no cover
    from sys import stdin

    for line in stdin:
        print(evaluate_game(line))
