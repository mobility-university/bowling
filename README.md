[![ci](https://github.com/mobility-university/bowling/actions/workflows/ci.yml/badge.svg)](https://github.com/mobility-university/bowling/actions/workflows/ci.yml)
![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)
![coverage](https://raw.githubusercontent.com/mobility-university/bowling/main/.github/coverage.svg)


# Bowling

## Motivation

Bowling is a nice coding kata, cause score calculation is a bit tricky. A strike in this throw gives a point advantage for the next two throws for example.
So it is not valid to just iterate over the throws of a game to calculate points.
Here it is shown how to iterate with a window of 3 throws to have the point calculation logic as concise and readable as possible.

![Alt text](BowlingThrows.png?raw=true "Sliding Window over Throws")

The picture shows the three iterators. The current throw, the last throw and the throw before the last throw. The window helps to iterate all three together to express the scoring algorithm as understandable as possible.

```python
for throw_before_last_throw, last_throw, throw in iter_over_throws(
    game.split("|"), window_size=3
):
    score += throw.points
    if throw_before_last_throw and throw_before_last_throw.strike:
        score += throw.points
    if last_throw and (last_throw.spare or last_throw.strike):
        score += throw.points
```

As you see, in the code above, it is pretty readable how scoring is done. Taking the normal points and double points if throw before last throw was a strike or if the last throw was a strike/spare.

## Execute it as docker

```sh
docker build -t bowling . &&
echo -n '11|11|11|11|11|11|11|11|11|11||' | docker run -i bowling
```
