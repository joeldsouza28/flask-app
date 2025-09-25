from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
Scss(app=app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app=app)


class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task {id}"


with app.app_context():
    db.create_all()


# Home Page
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        current_task = request.form["content"]
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")

        except Exception as ex:
            print(f"ERROR:{ex}")
            return f"ERROR:{ex}"

    else:
        tasks = MyTask.query.order_by(MyTask.created.desc()).all()

    return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id: int):
    delete_task = MyTask.query.get_or_404(id)

    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as ex:
        return f"ERROR:{ex}"


@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id: int):
    edit_task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        edit_task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as ex:
            return f"ERROR:{ex}"
    else:
        return render_template("edit.html", task=edit_task)


if __name__ == "__main__":
    app.run()
