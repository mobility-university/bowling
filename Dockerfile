FROM python:3.10-alpine

COPY game.py /game.py

RUN python3 -m doctest /game.py

CMD ["/game.py"]
