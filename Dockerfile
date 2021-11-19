FROM ubuntu:focal

RUN apt-get update && \
    apt-get --yes install python3-flask-sqlalchemy python3-pymysql wget && \
    apt-get clean && \
    mkdir /agama && \
    wget --secure-protocol=TLSv1_2 -O/agama/agama.py https://raw.githubusercontent.com/hudolejev/agama/master/agama.py

ENV AGAMA_DATABASE_URI=sqlite:////agama/db.sqlite3
ENV FLASK_APP=agama

EXPOSE 8000/tcp

WORKDIR /agama

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
