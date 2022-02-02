import MySQLdb.cursors
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
import datetime

todayy = datetime.date.today()
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'new-password'
app.config['MYSQL_DB'] = 'product_data'
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)
mysql = MySQL(app)


@app.route('/post', methods=['POST'])
def index():
    if request.method == "POST":
        details = request.form
        Nama = details['name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO product(name, createdData) VALUES (%s, %s)", (Nama, todayy.strftime("%Y-%m-%d")))
        mysql.connection.commit()
        cur.close()
    return "OK"


@app.route('/', methods=['GET'])
def router():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM product")
    data = cur.fetchall()
    productData = []
    content = {}
    for result in data:
        content = {"id": result['id'], "name": result['name'], "createdData": result['createdData']}
        productData.append(content)
        content = {}
    return {"data": productData}


@app.route('/update', methods=['PUT'])
def update():
    print("triggered")
    cur = mysql.connection.cursor()
    form = request.form
    name = form["name"]
    productId = form["id"]
    print('UPDATE product SET name = %s WHERE ID = %s' % (name, productId))
    cur.execute("UPDATE product SET name = %s WHERE ID = %s", (name, productId))
    mysql.connection.commit()
    cur.close()
    return "OK"

@app.route('/delete', methods=['DELETE'])
def delete():
    cur = mysql.connection.cursor()
    form = request.form
    productId = request.args.get("id")
    print("DELETE FROM product WHERE ID = %s" % productId)
    cur.execute("DELETE FROM product WHERE ID = %s", [productId])
    mysql.connection.commit()
    cur.close()
    return "OK"

if __name__ == '__main__':
    app.run()
