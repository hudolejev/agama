FROM alpine:latest

RUN apk add python3 && \
    python3 -m ensurepip && \
    pip3 install Flask-SQLAlchemy && \
    mkdir /agama && \
    wget -O/agama/agama.py https://raw.githubusercontent.com/hudolejev/agama/master/agama.py

ENV AGAMA_DATABASE_URI=sqlite:////agama/db.sqlite3
ENV FLASK_APP=agama

EXPOSE 8000/tcp

WORKDIR /agama

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
