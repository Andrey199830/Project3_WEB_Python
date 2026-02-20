from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, ForeignKey #, DateTime 
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:12345@localhost/AAA'
db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    id_subtask=db.Column(db.ForeignKey("tasks.id"))
    text = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=True)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    DateTime = db.Column(db.DateTime)
    

@app.route('/')
def index():
    return render_template('base.html',                        
        tasks=Task.query.filter(Task.id_subtask==None).order_by(Task.id).all(), 
        SubTasks=Task.query.filter(Task.id_subtask!=None).order_by(Task.id).all()
        )                                                                                     


@app.route('/addTask', methods=["POST"])
def addTask():
    text = request.form.get('task')
    details = request.form.get('Detalies')
    DateTimeObj = datetime.now()
    DateTime = DateTimeObj.strftime('%Y-%m-%d %H:%M:%S')
    db.session.add(Task(text=text, details=details, DateTime=DateTime))
    db.session.commit()
    return redirect(url_for('index'))
   

@app.route('/reopen', methods=["POST"])
def reopen():
    task_id = request.form.get('Reopen')
    DateTimeObj = datetime.now()
    DateTime = DateTimeObj.strftime('%Y-%m-%d %H:%M:%S')
    task = Task.query.get(task_id)

    if(task.id_subtask != None):
            task.is_done = False
            db.session.add(task)
            task.DateTime = DateTime
            db.session.add(task)

    else:
            task.is_done = False
            db.session.add(task)
            task.DateTime = DateTime
            db.session.add(task)
            db.session.query(Task).filter(Task.id_subtask == task_id).update({'is_done': False, 'DateTime': DateTime})
            
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/addSubTask', methods=["POST"])
def addSubTask():
    text = request.form.get('TextSubTask')
    id_subtask = request.form.get('idSubTask')
    details = request.form.get('Detalies')

    DateTimeObj = datetime.now()
    DateTime = DateTimeObj.strftime('%Y-%m-%d %H:%M:%S')

    db.session.add(Task(id_subtask=id_subtask, text=text, details=details, DateTime=DateTime))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear', methods=["POST"])
def clear():
    
    task_id = request.form.get('DelTaskSub')
    
    if (task_id == 'ALL'):
        Task.query.delete()    
        db.session.commit()
    else:
        task = Task.query.get(task_id)
        if(task.id_subtask != None):
            db.session.delete(task)
            db.session.commit()
        else:
            db.session.query(Task).filter(Task.id_subtask == task_id).delete()
            db.session.delete(task)
            db.session.commit()
    return redirect(url_for('index'))

@app.route('/done/<int:task_id>')
def done(task_id):
    task = Task.query.get(task_id)  

    if (task.id_subtask != None): 
        task.is_done = True
        DateTimeObj = datetime.now()
        DateTime = DateTimeObj.strftime('%Y-%m-%d %H:%M:%S') 
        db.session.add(task)  
        task.DateTime = DateTime
        db.session.add(task)
    else:
        task.is_done = True
        DateTimeObj = datetime.now()
        DateTime = DateTimeObj.strftime('%Y-%m-%d %H:%M:%S') 
        task.DateTime = DateTime
        db.session.add(task)
        db.session.query(Task).filter(Task.id_subtask == task_id, Task.is_done == False ).update({'is_done': True, 'DateTime': DateTime})  
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == "__main__":
        with app.app_context(): 
            db.drop_all() 
            db.create_all() 
            app.run(debug=True)
    
