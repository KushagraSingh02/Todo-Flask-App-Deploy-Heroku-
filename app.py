from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__) #initialising the app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #this line is just to remove the warning

db = SQLAlchemy(app)

#defining schema for the model we are going to take input
class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    data_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} " #f is when we want values along with normal text

@app.route("/" , methods = ["GET" , "POST"])
def hello_world():
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodos = Todo.query.all()

    # return "<p>Hello, World!</p>"
    return render_template("index.html" , allTodos = allTodos)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
    

@app.route("/update/<int:sno>" ,methods = ['GET','POST'])
def update(sno):

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
         
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.filter_by(sno=sno).first()
    
    return render_template('update.html',todo=todo)

if __name__ == "__main__":
    app.run(debug=True)