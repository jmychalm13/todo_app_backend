from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
# /// = relative path, //// = absolute path
# /// = relative path, //// = absolute path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "complete": self.complete}


@app.route("/todos", methods=["GET"])
def home():
    todos = Todo.query.all()
    todo_list = [todo.to_dict() for todo in todos]

    return jsonify(todo_list)


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid Input"}), 400
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title is required"}), 400

    # create new todo
    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({"id": new_todo.id, "title": new_todo.title}), 201


@app.route("/update/<int:todo_id>", methods=["PATCH"])
def update(todo_id):
    data = request.get_json()
    todo = Todo.query.get_or_404(todo_id)
    if "title" in data:
        todo.title = data["title"]
        db.session.commit()
        return jsonify({"id": todo.id, "title": todo.title}), 200
    return jsonify({"error": "Title not provided"}), 400


@app.route("/delete/<int:todo_id>", methods=["DELETE"])
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message": "Todo Destroyed"}), 200
    return jsonify({"error": "Todo not found"}), 404


def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
