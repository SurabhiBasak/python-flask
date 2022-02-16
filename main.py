
import os

import pymysql

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
host = '127.0.0.1'
cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

with cnx.cursor() as cursor:
    cursor.execute('select name from testtable;')
    result = cursor.fetchall()
    current_msg = result[0][0]
cnx.close()

return str(current_msg)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True)
