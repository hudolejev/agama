FROM ubuntu:focal

RUN apt-get update && \
    apt-get --yes install python3-flask-sqlalchemy python3-pymysql && \
    apt-get clean

WORKDIR /agama

COPY agama.py .

ENV AGAMA_DATABASE_URI=sqlite:////agama/db.sqlite3
ENV FLASK_APP=agama

EXPOSE 8000/tcp

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
