[![ci](https://github.com/mobility-university/bowling/actions/workflows/ci.yml/badge.svg)](https://github.com/mobility-university/bowling/actions/workflows/ci.yml)
![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)
![coverage](https://raw.githubusercontent.com/mobility-university/bowling/main/.github/coverage.svg)


# Bowling

## Motivation

Bowling is a nice coding kata, cause score calculation is a bit tricky. A strike in this throw gives a point advantage for the next two throws for example.
So it is not valid to just iterate over the throws of a game to calculate points.
Here it is shown how to iterate with a window of 3 throws to have the point calculation logic as concise and readable as possible.

## Execute it as docker

```!sh
docker build -t bowling . &&
echo -n '11|11|11|11|11|11|11|11|11|11||' | docker run -i bowling
```
