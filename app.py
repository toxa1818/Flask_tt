from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autoservice.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    experience = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Worker %r>' % self.id


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Service %r>' % self.id


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    client_name = db.Column(db.String(20), nullable=False)
    client_phone = db.Column(db.String(13), nullable=False)
    client_car = db.Column(db.String(30), nullable=False)


    def __repr__(self):
        return '<Entry %r>' % self.id


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/timetable')
def timetable():
    entries = Entry.query.order_by(Entry.start_time.asc()).all()
    return render_template('timetable.html', entries=entries)


@app.route('/create_entry', methods=['POST', 'GET'])
def create_entry():
    if request.method == 'POST':
        start_time = request.form['start_time']
        client_name = request.form['client_name']
        client_phone = request.form['client_phone']
        client_car = request.form['client_car']
        entry = Entry(start_time=datetime.strptime(start_time, '%Y-%m-%dT%H:%M'),
                      client_name=client_name, client_phone=client_phone, client_car=client_car)
        db.session.add(entry)
        db.session.commit()
        return redirect('/timetable')
    else:
        return render_template('create_entry.html')


@app.route('/workers')
def workers():
    return render_template('workers.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.run(debug=True)
