import json
from flask import Flask, request
import psycopg2
import psycopg2.extras
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

hostname = 'localhost'
database = 'loginData'
username = 'postgres'
pwd = 'password'
port_id = 5432


def create_connection():
    connection = psycopg2.connect(host=hostname,
                                  dbname=database,
                                  user=username,
                                  password=pwd,
                                  port=port_id,
                                  )
    connection.autocommit = True

    return connection


@app.route('/signup', methods=['POST'])
def index():
    payload = request.json
    email = payload['email']
    password = payload['password']
    birthday = payload['birthday']
    connection = create_connection()
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = 'insert into userData(email,password,dob) values(%s,%s,%s)'
    cur.execute(query, (email, password, birthday))
    cur.close()
    connection.close()
    return {'status': 'success'}


@app.route('/login', methods=['POST'])
def login():
    payload = request.json
    email = payload['email']
    password = payload['password']
    connection = create_connection()
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query1 = 'select email,password from userdata where email=%s and password=%s'
    cur.execute(query1, (email, password,))
    if len(cur.fetchall()):
        cur.close()
        connection.close()
        return {'status': 'success'}

    else:
        cur.close()
        connection.close()
        return {'status': 'failed'}


if __name__ == "__main__":
    app.run(debug=True)
