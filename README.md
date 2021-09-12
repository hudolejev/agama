# AGAMA: A (very) Generic App to Manage Anything

Simple (and mostly pointless) list management app in Python, Flask and
SQLAlchemy.

![Screenshot](./agama-screenshot.png)


## Purpose

This app is written mainly for demo purposes. It is used to illustrate various
aspects of app _deployment_ (not development) and system administration.

Do not treat this code as an example how to write Flask apps -- you can surely
find some better ones.


## Requirements

 - Python 3 (known to work on v3.8.10, v3.6.9)
 - [Flask](https://flask.palletsprojects.com/en/1.1.x/)
   (known to work on v1.1.2, v1.1.1)
 - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
   (known to work on v2.4.4, v2.1)

Optional for closer-to-production setups:

 - MySQL or any other database that
   [SQLAlchemy supports](https://docs.sqlalchemy.org/en/13/core/engines.html#supported-databases)
 - uWSGI or any other app server that
   [can run Flask apps](https://flask.palletsprojects.com/en/1.1.x/deploying)
 - Nginx or any other web server that can 'talk' to your app server of choice


## Installation

Install dependencies; recommended way is to use OS package manager, example for
Debian/Ubuntu:

	apt install python3-flask-sqlalchemy

Alternative way is to use `pip` -- but deploying to Python Virtualenv is
**strongly** recommended in this case:

	/path/to/pip install Flask-SQLAlchemy

Note: do not use both `pip` and `apt`! Choose _one_ method only.

Download the [agama.py](https://raw.githubusercontent.com/hudolejev/agama/master/agama.py)
to the desired location.

That's it -- you're ready to go.


## Configuration

AGAMA is configured with environment variables. Currently the only supported
parameter is `AGAMA_DATABASE_URI` which uses the same format as
[SQLAlchemy database URLs](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls),
example for SQLite:

	AGAMA_DATABASE_URI=sqlite:////path/to/db.sqlite3


## Running

Running manually -- only for development and/or testing purposes, example with
SQLite:

	export AGAMA_DATABASE_URI=sqlite:////path/to/db.sqlite3
	/path/to/python3 /path/to/agama.py

Running with [uWSGI](https://uwsgi-docs.readthedocs.io) -- example with MySQL;
database, database user and local system user `agama` should be created first:

	[uwsgi]
	chdir = /path/to/agama/dir
	module = agama:app
	env = AGAMA_DATABASE_URI=mysql://<username>:<password>@<db-host>/<db-name>
	plugins = python3
	socket = localhost:5000
	uid = agama

You can also run it manually with MySQL backend, or with uWSGI and SQLite
backend if you want.

Example Nginx configuration for uWSGI setup:

	server {
		listen 80 default_server;
		server_name _;

		location / {
			uwsgi_pass localhost:5000;
			include uwsgi_params;
		}
	}


## Contributing

[Issue reports](https://github.com/hudolejev/agama/issues) and
[pull requests](https://github.com/hudolejev/agama/pulls) are warmly welcome.


## Author

[Juri Hudolejev](https://github.com/hudolejev) -- initial design and implementation.

Special thanks to
 - [Roman Kuchin](https://github.com/romankuchin) for testing
 - [Margus Laanem](https://github.com/marguslaanem) for Docker file improvements


## License

MIT
