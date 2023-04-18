from flask import *
import time
import os
import mysql.connector as sql

conn = sql.connect(host="localhost",user="root",passwd="pwdsql",db="users",autocommit=True)
c1 = conn.cursor()
app = Flask(__name__,static_url_path='',static_folder='static',template_folder='templates')
app.secret_key = "secret key"


@app.route("/",methods = ['POST','GET'])
@app.route('/login',methods = ['POST','GET'])
def index():
    if request.method=='POST':
        try:
            acc = request.form['Acc']
            pin = request.form['PIN']
            acc = int(acc)
            pin = int(pin)
            # data = [0,]
            # print("yes")
            c1.execute(f"SELECT pin FROM users where Acc_no={acc}")
            data = c1.fetchall()
            # print(data[0][0]==pin)
            if (data==[]):
                flash("User Login: Account Number entered is incorrect!")
                return render_template('login.html')
            elif data[0][0]!=pin:
                flash("User Login: Login Credentials are incorrect!")
                return render_template('login.html')
            else:
                return render_template('Users.html')

        except KeyError:
            email = request.form['email']
            pwd = request.form['pwd']
            # print("no")
            
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)