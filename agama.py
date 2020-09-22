import os
import sys

from flask import Flask
from flask import redirect
from flask import request
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment


if 'AGAMA_DATABASE_URI' not in os.environ:
    print('''
ERROR: Environment variable AGAMA_DATABASE_URI is not set.

AGAMA_DATABASE_URI uses the SQLAlchemy format.

For SQLite3 use

  AGAMA_DATABASE_URI=sqlite:////path/to/db.sqlite3  # yes, 4 slashes

For MySQL use

   AGAMA_DATABASE_URI=mysql://<username>:<password>@<server-address>/<db-name>

For other examples see
https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls.''')
    sys.exit(1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['AGAMA_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(999), unique=True, nullable=False)
    state = db.Column(db.Integer, default=0)


@app.before_request
def before_request():
    if not Item.metadata.tables[Item.__tablename__].exists(db.get_engine(app)):
        app.logger.info('Initializing the database...')
        init_db()


@app.route('/')
def index():
    return html(items=Item.query.all())


@app.route('/items/add', methods=['GET', 'POST'])
def item_add():
    item = request.form['new_item']
    if len(item) > 999:
        return html_error('The item you are trying to add seems too large; it should be shorter than 1000 characters.')

    if Item.query.count() >= 100:
        return html_error('You are trying to add too many items; you have 100 items added already.')

    existing_item = Item.query.filter_by(value=item).first()
    if existing_item:
        return html_error('Item [%s] already exists.' % item)

    if request.method == 'POST':
        app.logger.info("Adding item '%s'..." % item)
        db.session.add(Item(value=item))
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/items/<id>/delete')
def item_delete(id):
    item = Item.query.filter_by(id=id)
    if item:
        app.logger.info('Deleting item %s...' % id)
        item.delete()
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/items/<id>/swap-state')
def item_swap_state(id):
    item = Item.query.get(id)
    if item:
        app.logger.info('Swapping item %s state (current state: %s)...' % (id, item.state))
        item.state = 0 if item.state else 1
        db.session.commit()

    return redirect(url_for('index'))


def html_error(error_msg):
    return '<h2>Error</h2><p>%s</p><p><a href="/">Go back</a>.</p>' % error_msg.strip().replace('\n', '</p><p>')


def html(items=[]):
    return Environment(autoescape=True).from_string("""<!DOCTYPE html>
<html>
    <head>
        <title>AGAMA</title>
        <style>
            a.delete { text-decoration: none; }
            body { display: table-cell; text-align: center }
            div#logo { font-size: 6em }
            form { padding-top: 1em }
            html { display: table; margin: auto }
            input { font-size: large }
            p.footer { border-top: 1px solid #999; margin: 1em 4em 0 4em; padding-top: 1em }
            table { padding: 1em 0 0 3.5em; margin: auto }
            td.actions { padding: 1em; text-align: center }
            td.item { border: 1px solid #ddd  }
            td.item a { color: black; display: block; font-size: larger; padding: 1em; text-decoration: none }
            tr.item-0 td.item { background-color: #edd }
            tr.item-1 td.item { background-color: #ded }
        </style>
        <link rel="icon" href="data:image/x-icon;base64,
            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
        " />
    </head>
    <body>
        <div id="logo">🦎</div>
        <h1> AGAMA</h1>
        <h3>A (very) Generic App to Manage Anything</h3>
        <form action="items/add" method="POST">
             New item:
             <input type="text" name="new_item" autofocus />
             <input type="submit" value="Add" />
        </form>
        <table>
{% for item in items %}
            <tr class="item-{{ item['state'] }}">
                <td class="item"><a href="/items/{{ item['id'] }}/swap-state">{{ item['value'] }}</a></td>
                <td class="actions"><a class="delete" href="/items/{{ item['id'] }}/delete">❌</a</td>
            </tr>
{% endfor %}
        </table>
        <p>Hint: Click on item to change its state, or X to delete.</p>
        <p class="footer">
            AGAMA v0.1 running on {{ host }} |
            <a href="https://github.com/hudolejev/agama">GitHub</a>
        </p>
    <body>
</html>""").render(host=os.uname()[1], items=items)


def init_db():
    db.create_all()
    db.session.add(Item(value='A pre-created item with no particular meaning', state=1))
    db.session.add(Item(value='Another even less meaningful item'))
    db.session.commit()


if __name__ == '__main__':
    app.run()
