from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/kenda/PycharmProjects/untitled1/TodoApp/todo.db'
app.secret_key = "jehatarmanc"  # *** can't use flash messages without this
db = SQLAlchemy(app)


@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)


@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    """if todo.complete:
        todo.complete = False
    else:
        todo.complete = True"""
    todo.complete = not todo.complete
    db.session.commit()
    if todo.complete:
        flash("Tamamladınız", "success")
    else:
        flash("Todo Sıfırlandı","info")
    return redirect(url_for("index"))


@app.route("/add", methods=["POST"])
def addTodo():
    try:
        title = request.form.get("title")
        newTodo = Todo(title=title, complete=False)
        db.session.add(newTodo)
        db.session.commit()
    except IntegrityError:
        flash("-- {} -- başlıklı todo zaten var".format(title), "danger")   # ***fix here***
        db.session.rollback()
    return redirect(url_for("index"))


@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    flash("- {} - isimli todo yok edildi".format(todo.title), "info")
    return redirect(url_for("index"))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False, unique=True)
    complete = db.Column(db.Boolean)

    def __repr__(self):
        return f"User('{self.username}')"


if __name__ == "__main__":
    app.run(debug=True)
