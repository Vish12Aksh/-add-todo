from flask import Flask, render_template, jsonify, request , redirect
import requests
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
 
@app.route('/', methods=['GET', 'POST'])
def Hee():

    if request.method == 'POST':
        # print('post request received')
        # print(request.form['title'])
        title  = request.form['title']
        desc = request.form['desc']

        todo_item = Todo(title= title, desc= desc)
        db.session.add(todo_item)
        # db.session.delete
        db.session.commit()
    all_Todo = Todo.query.all()
    # print(all_Todo)
    return render_template('index.html', all_Todos = all_Todo)

@app.route('/show')
def product(): 
    todos = Todo.query.all()
    print(todos)
    return 'ghbfgh n gfghfgh'

@app.route('/update/<int:sno>',  methods=['GET', 'POST'])
def update(sno): 
    
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todos = Todo.query.filter_by(sno = sno).first()
        todos.title = title
        todos.desc = desc
        db.session.add(todos)
        db.session.commit()
        return redirect('/')
        
    # print(todos)
    todos = Todo.query.filter_by(sno = sno).first()
    return render_template('update.html', todo = todos)

@app.route('/delete/<int:sno>')
def delete(sno): 
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    # print(todos)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
   