from flask import Flask, render_template, request, jsonify
import csv
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    x = 3
    return render_template('index.html')

@app.route('/data')
def data():
    data = []
    with open('data.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return jsonify(data)


@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template("hello_there.html", username=name)

@app.route("/db")
def test_db():
    conn = sqlite3.connect('database.db')
    print('Opened database successfully', flush=True)
    
    conn.execute('DROP TABLE IF EXISTS students')
    conn.commit()
    conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, zip TEXT)')
    print('Table created successfully', flush=True)
    conn.close()
    return "Table created successfully"

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            zip = request.form['zip']
         
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name,addr,city,zip)VALUES (?,?,?,?)",(nm,addr,city,zip) )
            
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
      
        finally:
            con.close()
            return render_template("result.html",msg = msg)

@app.route('/list')
def list():
   con = sqlite3.connect("database.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)
