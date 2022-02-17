import os 

from flask import Flask, jsonify, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

db_user= os.environ.get('CLOUD_SQL_USERNAME')

db_password= os.environ.get('CLOUD_SQL_PASSWORD')

db_name= os.environ.get('CLOUD_SQL_DATABASE_NAME')

db_connection_name= os.environ.get('CLOUD_SQL_CONNECTION_NAME')


app = Flask(__name__)
@app.route('/', methods=["POST","GET"])
def index():
    insert_stmt = ("INSERT INTO user (name, password)""VALUES (%s, %s)")
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
        if request.method == 'POST':
            name = request.form.get('name')
            password = request.form.get('password')
            a=name+','+password
            a =tuple(str(x) for x in a.split(","))
            with cnx.cursor() as cursor:
                cursor.execute(insert_stmt, a)
            cnx.close()
            return redirect(url_for('home'))
        else:
            return render_template("login.html")
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        if request.method == 'POST':
            name = request.form.get('name')
            password = request.form.get('password')
            a=name+','+password
            a =tuple(str(x) for x in a.split(","))
            with cnx.cursor() as cursor:
                cursor.execute(insert_stmt, a)
            cnx.close()
            return redirect(url_for('home'))
        else:
            return render_template("login.html")


   
   
    
    

    



@app.route('/home', methods=["POST","GET"])
def home():
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

    with cnx.cursor() as cursor:
        cursor.execute('select name from user;')
        result = cursor.fetchall()
        current_msg = result[0][0]
    cnx.close()

    return str(current_msg)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)