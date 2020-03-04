from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tasks.db'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto= db.Column(db.String(200))
    feito = db.Column(db.Boolean)
    def __init__(self,texto):
        self.texto = texto
db.create_all()

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html', tasks = tasks)

@app.route('/create-task', methods=['POST'])
def create():
    novo=Task(texto=request.form['texto'])
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/feito/<id>')
def feito(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.feito = not(task.feito)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<id>')
def delete(id):
    Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)