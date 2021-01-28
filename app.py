import json
import sqlite3

from flask import Flask, request

app = Flask(__name__)
connection = sqlite3.connect("log.db", check_same_thread=False)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

try:
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS people (name TEXT,age INT,id INT)")
    print('Table Created Successfully')
except Exception as e:
    print(e)


@app.route('/', methods=['GET'])
def root():
    response = {"message": "Welcome To Flask Server", "status": "Flask server running"}
    return json.dumps(response)


@app.route('/post', methods=['POST'])
def put_db():
    user = request.args.get('user')
    age = request.args.get('age')
    userId = request.args.get('id')
    params = (user, age, userId)
    if user is not None and age is not None and userId is not None:
        cursor.execute(f"INSERT INTO people VALUES (?,?,?)", params)
        connection.commit()
        return f'Data added Successfully for user: {user}'
    else:
        return "please submit all values"


@app.route('/get', methods=['GET'])
def get_db():
    user = request.args.get('user')
    Id = request.args.get('id')
    if user is not None:
        res = cursor.execute('select * from people where name=?', (user,)).fetchall()
        if len(res) == 0:
            return f"User {user} not found on database"
        else:
            result = cursor.execute("SELECT * FROM people WHERE name=?", (user,)).fetchall()
            response = {"users": [dict(i) for i in result]}
            return json.dumps(response)
    if Id is not None:
        res = cursor.execute('select * from people where id=?', (Id,)).fetchall()
        if len(res) == 0:
            return f"Id {Id} not found on database"
        else:
            result = cursor.execute("SELECT * FROM people WHERE id=?", (Id,)).fetchall()
            response = {"users": [dict(i) for i in result]}
            return json.dumps(response)
    else:
        result = cursor.execute("SELECT * FROM people").fetchall()
        response = {"users": [dict(i) for i in result]}
        return json.dumps(response)


@app.route('/update', methods=['PATCH'])
def update_db():
    user = request.args.get('user')
    age = request.args.get('age')
    Id = request.args.get('id')
    if user and Id is not None:
        res = cursor.execute('select * from people where id=?', (Id,)).fetchall()
        if len(res) == 0:
            return f"Id {Id} doesn't exists on database"
        else:
            cursor.execute('UPDATE people SET name=? WHERE id=?', (user, Id,))
            connection.commit()
        return "User updated Successfully"
    if age and Id is not None:
        res = cursor.execute('select * from people where id=?', (Id,)).fetchall()
        if len(res) == 0:
            return f"Id {Id} doesn't exists on database"
        else:
            cursor.execute('UPDATE people SET age=? WHERE id=?', (age, Id,))
            connection.commit()
        return "User updated Successfully"
    else:
        return "Provide value for update database"


@app.route('/delete', methods=['DELETE'])
def delete_db():
    Id = request.args.get('id')
    user = request.args.get('user')
    if Id is not None:
        res = cursor.execute('select * from people where id=?', (Id,)).fetchall()
        if len(res) == 0:
            return f"Id {Id} doesn't exists on database"
        else:
            cursor.execute('DELETE FROM people WHERE id=?', (Id,))
            connection.commit()
        return f"User {Id} deleted Successfully"
    elif user is not None:
        res = cursor.execute('select * from people where name=?', (user,)).fetchall()
        if len(res) == 0:
            return f"User {user} doesn't exists on database"
        else:
            cursor.execute('DELETE FROM people WHERE name=?', (user,))
            connection.commit()
        return f"User {user} deleted Successfully"
    else:
        return "please provide values to delete user"


if __name__ == "__main__":
    app.run(debug=True)
