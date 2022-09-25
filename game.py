#!/usr/bin/env python3
from collections import namedtuple
from itertools import islice


Throw = namedtuple("Throw", "frame strike spare points")


def evaluate_game(game):
    """
    >>> evaluate_game('--|--|--|--|--|--|--|--|--|--||')
    0
    >>> evaluate_game('1-|--|--|--|--|--|--|--|--|--||')
    1
    >>> 'foobarbaz' # doctest: +ELLIPSIS
    'foo...baz'
    >>> try:
    ...     evaluate_game('77|--|--|--|--|--|--|--|--|--||')
    ...     assert False
    ... except AssertionError:
    ...     pass
    >>> evaluate_game('11|11|11|11|11|11|11|11|11|11||')
    20
    >>> evaluate_game('X|--|--|--|--|--|--|--|--|--||')
    10
    >>> evaluate_game('X|1-|--|--|--|--|--|--|--|--||')
    12
    >>> evaluate_game('X|1-|1-|--|--|--|--|--|--|--||')
    13
    >>> evaluate_game("1/|11|--|--|--|--|--|--|--|--||") #Spare
    13
    >>> evaluate_game('X|11|--|--|--|--|--|--|--|--||')
    14
    >>> evaluate_game("1/|--|--|--|--|--|--|--|--|--||") #Spare
    10
    >>> evaluate_game("X|X|-2|--|--|--|--|--|--|--||") #Two Strikes
    34
    """
    score = 0

    for (
        throw_before_last_throw,
        last_throw,
        throw,
    ) in iter_over_throws(game.split("|"), window_size=3):
        if throw.frame >= 11:
            return score
        score += throw.points
        if last_throw and (last_throw.spare or last_throw.strike):
            score += throw.points
        elif throw_before_last_throw and throw_before_last_throw.strike:
            score += throw.points

    raise Exception("need 10 throws")


def iter_over_throws(frames, window_size):
    """
    >>> list(iter_over_throws(['12'], window_size=3))
    [(None, None, Throw(frame=1, strike=False, spare=False, points=1)), (None, Throw(frame=1, strike=False, spare=False, points=1), Throw(frame=1, strike=False, spare=False, points=2))]
    """

    def get_throws():
        for i in range(1, window_size):
            yield None
        for i, frame in enumerate(frames, 1):
            yield from evaluate_frame(number=i, frame=frame)

    yield from window(list(get_throws()), size=window_size)


def window(iterable, size):
    """
    >>> list(window([None, None, 1,2,3],size=3))
    [(None, None, 1), (None, 1, 2), (1, 2, 3)]
    """
    return zip(*[islice(iterable, s, None) for s in range(size)])


def evaluate_frame(number, frame):
    """
    >>> list(evaluate_frame(number=1, frame='X'))
    [Throw(frame=1, strike=True, spare=False, points=10)]
    >>> list(evaluate_frame(number=1, frame='1-'))
    [Throw(frame=1, strike=False, spare=False, points=1), Throw(frame=1, strike=False, spare=False, points=0)]
    >>> list(evaluate_frame(number=1, frame='11'))
    [Throw(frame=1, strike=False, spare=False, points=1), Throw(frame=1, strike=False, spare=False, points=1)]
    >>> try:
    ...     list(evaluate_frame(number=1, frame='66'))
    ...     assert False
    ... except AssertionError:
    ...     pass
    >>> try:
    ...     list(evaluate_frame(number=1, frame='123'))
    ...     assert False
    ... except AssertionError:
    ...     pass
    >>> try:
    ...     list(evaluate_frame(number=1, frame='1'))
    ...     assert False
    ... except AssertionError:
    ...     pass
    >>> try:
    ...     list(evaluate_frame(number=1, frame='-/'))
    ...     assert False
    ... except AssertionError:
    ...     pass
    >>> list(evaluate_frame(number=1, frame='1/'))
    [Throw(frame=1, strike=False, spare=False, points=1), Throw(frame=1, strike=False, spare=True, points=9)]
    """
    if frame == 'X':
        yield Throw(frame=number, strike=True, spare=False, points=10)
        return
    points = 0
    if number >= 11:
        assert frame == ''
        yield Throw(frame=number, strike=False, spare=False, points=0)
        return
    assert len(frame) == 2

    for throw in frame:
        if throw == '-':
            yield Throw(frame=number, strike=False, spare=False, points=0)
        elif '1' <= throw <= '9':
            points += int(throw)
            yield Throw(frame=number, strike=False, spare=False, points=int(throw))
        elif throw == '/':
            assert points > 0
            yield Throw(frame=number, strike=False, spare=True, points=10 - points)
    assert 0 <= points <= 10


if __name__ == '__main__':
    from sys import stdin

    for line in stdin:
        print(evaluate_game(line))
