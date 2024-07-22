from app import app, db, Todo

with app.app_context():
    todo1 = Todo(title="Finish interview prep", complete=False)
    todo2 = Todo(title="Feed dog", complete=False)
    todo3 = Todo(title="Get a real job", complete=False)
    todo4 = Todo(title="Feed plants", complete=False)

    db.session.add(todo1)
    db.session.add(todo2)
    db.session.add(todo3)
    db.session.add(todo4)
    db.session.commit()

    print("Todos added successfully!")
