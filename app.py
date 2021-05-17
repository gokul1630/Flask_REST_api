import json
import sqlite3

from flask import Flask, request

app = Flask(__name__)
connection = sqlite3.connect("log.db", check_same_thread=False)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()


def getAllResponse():
    result = cursor.execute("SELECT * FROM people").fetchall()
    jsonResponse = {"users": [dict(i) for i in result]}
    response = app.response_class(
        response=json.dumps(jsonResponse),
        status=200,
        mimetype='application/json'
    )
    return response


try:
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS people (name TEXT,age INT,id INT)")
    print('Table Created Successfully')
except Exception as e:
    print(e)


@app.route('/', methods=['GET'])
def root():
    message = {"message": "Welcome To Flask Server",
               "status": "Flask server running"}
    response = app.response_class(
        response=json.dumps(message),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/users', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def top_function():
    user = request.args.get('user')
    age = request.args.get('age')
    userId = request.args.get('id')
    params = (user, age, userId)
# POST
    if request.method == 'POST':
        if user is not None and age is not None and userId is not None:
            cursor.execute(f"INSERT INTO people VALUES (?,?,?)", params)
            connection.commit()
            return getAllResponse()
        else:
            return 'Please Provide All Values'


# GET
    elif request.method == 'GET':
        if user or userId is not None:
            res = cursor.execute(
                'select * from people where name=? or id=?', (user, userId,)).fetchall()
            if len(res) == 0:
                if(user != None):
                    return f"User {user} not found on database"
                else:
                    return f"userId {userId} not found on database"
            else:
                response = {"users": [dict(i) for i in res]}
                return json.dumps(response)
        else:
            return getAllResponse()


# PATCH
    elif request.method == 'PATCH':
        if user and userId is not None:
            res = cursor.execute(
                'select * from people where id=?', (userId,)).fetchall()
            if len(res) == 0:
                return f"id {userId} doesn't exists on database"
            else:
                cursor.execute(
                    'UPDATE people SET name=? WHERE id=?', (user, userId,))
                connection.commit()
                return getAllResponse()
        if age and userId is not None:
            res = cursor.execute(
                'select * from people where id=?', (userId,)).fetchall()
            if len(res) == 0:
                return f"id {userId} doesn't exists on database"
            else:
                cursor.execute(
                    'UPDATE people SET age=? WHERE id=?', (age, userId,))
                connection.commit()
                return getAllResponse()
        else:
            return "Provide userId value for update database"


# DELETE
    elif request.method == 'DELETE':
        if userId is not None:
            res = cursor.execute(
                'select * from people where id=?', (userId,)).fetchall()
            if len(res) == 0:
                return f"id {userId} doesn't exists on database"
            else:
                cursor.execute('DELETE FROM people WHERE id=?', (userId,))
                connection.commit()
                return getAllResponse()
        elif user is not None:
            res = cursor.execute(
                'select * from people where name=?', (user,)).fetchall()
            if len(res) == 0:
                return f"User {user} doesn't exists on database"
            else:
                cursor.execute('DELETE FROM people WHERE name=?', (user,))
                connection.commit()
                return getAllResponse()
        else:
            return "please provide Id value to delete user"


if __name__ == "__main__":
    app.run(debug=True)
