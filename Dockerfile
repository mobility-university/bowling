FROM python:3.10-alpine

COPY game.py /game.py

CMD ["/game.py"]
