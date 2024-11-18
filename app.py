from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Path to the database, this will create the database automatically.
app.secret_key = 'key'
db = SQLAlchemy(app) # Create an instance of slqalchemy and pass the app as a parameter. 

#Model Creation - this model will be stored in the sqlite database. We will store data using this model in the database.
class Todo(db.Model): 
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(200), nullable=False)

# To create the table in the database
with app.app_context():
    db.create_all()




@app.route('/',methods=['GET', 'POST'])
@app.route('/<int:todo_id>', methods=['GET', 'POST'])
def index(todo_id=None):
    if request.method == 'POST':
        title =  request.form.get('title')
        if todo_id is None:
            todo = Todo(title=title)
            db.session.add(todo) # To add title in the database
            db.session.commit() # To store title in the database
            flash('Todo item added successfully', 'success')
        else:
            todo = Todo.query.get(todo_id)
            if todo:
                todo.title = title
                db.session.commit()
                flash('Todo item updated successfully', 'success')
        
        return redirect(url_for('index'))


    todo = None
    if todo_id is not None:
        todo = Todo.query.get(todo_id)
    todos = Todo.query.order_by(Todo.id.desc()).all() # To get and show all the entries in the database.
 
    return render_template('index.html', todos = todos, todo=todo)

@app.route('/todo-delete/<int:todo_id>', methods=["POST"])
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash('Todo item deleted successfully', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)