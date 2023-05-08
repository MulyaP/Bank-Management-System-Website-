from flask import *
import time
import os
import mysql.connector as sql
import random
import string

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
                c1.execute(f"SELECT * FROM users where Acc_no={acc}")
                global user
                user = c1.fetchall()[0][0]
                return redirect('/users')

        except KeyError:

            emp = int(request.form['emp'])
            pwd = request.form['pwd']

            c1.execute(f"Select pwd from admin where emp_id={emp}")
            data = c1.fetchall()
            if (data==[]):
                flash("Admin Login: Employee ID entered is incorrect!")
                return render_template('login.html')
            elif data[0][0]!=pwd:
                flash("Admin Login: Login Credentials are incorrect!")
                return render_template('login.html')
            else:
                global admin
                admin = emp
                return redirect('/admin')
            
    return render_template('login.html')



@app.route('/admin',methods=['GET','POST'])
def admin():
    try:
        c1.execute(f"SELECT * from admin where emp_id={admin}")
        myadmin = c1.fetchall()
        return render_template('Admin/admin.html',admin=myadmin[0])
    except:
            return "Page not found",404

@app.route('/admin/Create-Account',methods=['GET','POST'])
def createAcc():
    try:
        c1.execute(f"SELECT * from admin where emp_id={admin}")
        myadmin = c1.fetchall()

        if request.method=='POST':
            acc = request.form.get('acc')
            name = request.form.get('Uname')
            bal = request.form.get('bal')
            ty = request.form.get('type')
            branch = request.form.get('branch')
            dob = request.form.get('dob')
            pin = request.form.get('pin')
            ph = request.form.get('ph')
            email = request.form.get('email')

            try:
                c1.execute(f"insert into users values('{acc}',{pin},'{name}','{ty}',{bal},'{branch}','{dob}','{ph}','{email}');")
                success = "Account successfully created!"
                return render_template('Admin/Create Account.html',admin=myadmin[0],success=success,fail='')

            except:
                fail = 'An error occurred..'
                return render_template('Admin/Create Account.html',admin=myadmin[0],success='',fail=fail)

        return render_template('Admin/Create Account.html',admin=myadmin[0],success='',fail='')
    except:
        return "Page not found",404

@app.route('/admin/Withdraw',methods=['GET','POST'])
def withdraw():
    try:
        c1.execute(f"SELECT * from admin where emp_id={admin}")
        myadmin = c1.fetchall()

        if request.method=='POST':
            acc = request.form.get('acc')
            amt = request.form.get('amt')
            
            try:
                c1.execute(f"select balance from users where Acc_no='{acc}';")
                bal = c1.fetchall()
                if (bal==[]):
                    fail = 'No such account exists'
                    return render_template('Admin/withdraw.html',admin=myadmin[0],success='',fail=fail)
                else:
                    bala = bal[0][0]
                    success = 'Amount successfully withdrawn'
                    c1.execute(f"update users set balance={bala-int(amt)} where Acc_no='{acc}';")
                    return render_template('Admin/withdraw.html',admin=myadmin[0],success=success,fail='')
                



            except:
                pass

        return render_template('Admin/withdraw.html',admin=myadmin[0],success='',fail='')
    except:
        
        return "Page not found",404

@app.route('/admin/Deposit',methods=['GET','POST'])
def deposit():
    try:
        c1.execute(f"SELECT * from admin where emp_id={admin}")
        myadmin = c1.fetchall()

        if request.method=='POST':
            acc = request.form.get('acc')
            amt = request.form.get('amt')
            
            try:
                c1.execute(f"select balance from users where Acc_no='{acc}';")
                bal = c1.fetchall()
                if (bal==[]):
                    fail = 'No such account exists'
                    return render_template('Admin/Deposit.html',admin=myadmin[0],success='',fail=fail)
                else:
                    bala = bal[0][0]
                    success = 'Amount successfully Deposited'
                    c1.execute(f"update users set balance={bala+int(amt)} where Acc_no='{acc}';")
                    return render_template('Admin/Deposit.html',admin=myadmin[0],success=success,fail='')
                



            except:
                pass

        return render_template('Admin/Deposit.html',admin=myadmin[0],success='',fail='')

    except:
        return "Page not found",404



@app.route('/users',methods=['GET','POST'])
def users():
    try:

        c1.execute(f"SELECT * from users where Acc_no={user}")
        myuser = c1.fetchall()
        return render_template ('Users/Users.html',user = myuser[0])

    except:
            return "Page not found",404
    

@app.route('/users/Credit',methods=['GET','POST'])
def credit():
    c1.execute(f"Select * from transactions where to_Acc={user};")
    Transaction = c1.fetchall()
    return render_template('Users/Credit.html',Transaction=Transaction)

@app.route('/users/Debit',methods=['GET','POST'])
def debit():
    c1.execute(f"Select * from transactions where from_Acc={user};")
    Transaction = c1.fetchall()
    return render_template('Users/Debit.html',Transaction=Transaction)

@app.route('/users/show-details',methods=['GET','POST'])
def showDetails():
    try:
        c1.execute(f"SELECT * from users where Acc_no={user}")
        myuser = c1.fetchall()
        if request.method == 'POST':
            acc = request.form.get('acc')
            # print(acc)
            c1.execute(f"UPDATE users SET pin={int(request.form.get('pin'))},name='{request.form.get('Uname')}' WHERE Acc_no={acc};")
            return redirect('/')
        return render_template('Users/show details.html',user = myuser[0])
    except:
        return "Page not found", 404

@app.route('/users/transfer',methods=['GET','POST'])
def transfer():
    try:
        c1.execute(f"SELECT * from users where Acc_no={user}")
        myuser = c1.fetchall()
        if request.method=='POST':
            pin = (request.form.get('pin'))
            acc = (request.form.get('Acc'))
            amt = (request.form.get('amt'))
            if (acc=='' or amt=='' or pin==''):
                fail = 'Account no. field, amount field and pin field cannot be empty!'
                return render_template('Users/transfer.html',user=myuser[0],fail=fail,success='')
            amt=int(amt)
            pin=int(pin)
            if (pin!=myuser[0][1]):
                fail = 'Incorrect Pin! Please try again'
                return render_template('Users/transfer.html',user=myuser[0],fail=fail,success='')
            else:
                c1.execute(f'SELECT balance FROM users where Acc_no={acc}')
                bal = c1.fetchall()
                if (bal==[]):
                    fail = 'No user with such account number exists'
                    return render_template('Users/transfer.html',user=myuser[0],fail=fail,success='')
                else:
                    c1.execute(f'UPDATE users SET balance={int(bal[0][0])+amt} where Acc_no={acc}')
                    c1.execute(f'SELECT balance FROM users WHERE Acc_no={user}')
                    bala = c1.fetchall()[0][0]
                    c1.execute(f'UPDATE users SET balance={bala-amt} WHERE Acc_no={user}')
                    t_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    c1.execute(f"insert into transactions values('{t_id}','{user}','{acc}',{amt});")
                    success = f'Amount successfully transfered! Your Transaction Id is {t_id}'
                    return render_template('Users/transfer.html',user=myuser[0],fail='',success=success)
                
                
        return render_template('Users/transfer.html',user = myuser[0],fail='',success='')
    
    except:
        return "Page not found",404

if __name__ == '__main__':
    app.run(debug=True)