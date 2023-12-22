from datetime import datetime, timedelta
import hashlib
from io import BytesIO
import os
import threading
from matplotlib import image, pyplot as plt
from openpyxl import Workbook
from openpyxl.chart import Reference, PieChart
from openpyxl.drawing.image import Image
import sqlalchemy
from app import app, db
from flask import make_response, redirect, render_template, request, send_file, send_from_directory
from typing import List
import concurrent.futures
from app.models import Sessions, Users

from app.utils import generate_numbers, generate_fibonacci_numbers

@app.route('/', methods=['GET'])
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return "ERROR: {}".format(str(e))
    
@app.route('/signup', methods=['GET'])
def renderSignUp():
    try:
        return render_template("signup.html")
    except Exception as e:
        return "ERROR: {}".format(str(e))
    
@app.route('/signin', methods=['GET'])
def renderSignIn():
    try:
        return render_template("signin.html")
    except Exception as e:
        return "ERROR: {}".format(str(e))

@app.route('/signup', methods=['POST'])
def signupUser():
    try:
        if request.form == None:
            raise ValueError("Empty args!\n")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")
        if (password != confirmPassword):
            raise ValueError("Passwords dont match!\n")
        
        sql = sqlalchemy.text("SELECT * FROM users WHERE username=:username")
        user = db.session.execute(sql, {"username": username}).fetchone()

        if user:
            raise ValueError("User already exists!\n")
        
        db.session.add(Users(username = username, password = hashlib.sha256(password.encode("utf-8")).hexdigest()))
        db.session.commit()

        res = make_response(redirect("/"))
        res.set_cookie("session_id", str(signin(username=username, passwordPlain=password)))
        return res
    except Exception as e:
        return "ERROR: {}".format(str(e))
    
@app.route('/signin', methods=['POST'])
def signinUser():
    try:
        if request.form == None:
            raise ValueError("Empty args!\n")
        username = request.form.get("username")
        password = request.form.get("password")

        res = make_response(redirect("/"))
        res.set_cookie("session_id", str(signin(username=username, passwordPlain=password)))
        return res
    except Exception as e:
        return "ERROR: {}".format(str(e))

def signin(username, passwordPlain):
    sql = sqlalchemy.text("SELECT * FROM users WHERE username=:username")
    user = db.session.execute(sql, {"username": username}).fetchone()

    if hashlib.sha256(passwordPlain.encode("utf-8")).hexdigest() != user.password:
        raise ValueError("Wrong password!\n")

    db.session.add(Sessions(userId = user.id, expires = (datetime.utcnow() + timedelta(hours=24))))
    db.session.commit()

    sql = sqlalchemy.text("SELECT * FROM sessions WHERE userId=:userId")
    session = db.session.execute(sql, {"userId": user.id}).fetchone()
 
    return session.id

@app.before_request
def before_request():
    if request.endpoint in ['renderSignUp', 'renderSignIn', 'signupUser', 'signinUser']:
        return
    
    sessionId = request.cookies.get('session_id')

    sql = sqlalchemy.text("SELECT * FROM sessions JOIN users ON sessions.userId = users.id WHERE sessions.id=:sessionId")
    session = db.session.execute(sql, {"sessionId": sessionId}).fetchone()
    
    if session == None or datetime.fromisoformat(session.expires) < datetime.utcnow():
        return redirect('/signin')
    
    request.session = session
    
@app.route('/generateChart', methods=['POST'])
def generateChart():
    try:
        start = int(request.form['start'])
        end = int(request.form['end'])
        filename = f'number_comparison_{start}_{end}.xlsx'
        if os.path.exists(f"static/{filename}"):
            return render_template('result.html', filename=filename, chart_image_url=f'number_comparison_{start}_{end}.png')

        simple_numbers, prime_numbers = generate_numbers(start, end)
        fibonacci_numbers = generate_fibonacci_numbers(start, end)

        average_simple = sum(simple_numbers) / len(simple_numbers) if simple_numbers else 0
        average_prime = sum(prime_numbers) / len(prime_numbers) if prime_numbers else 0
        total_sum = sum(simple_numbers) + sum(prime_numbers)

        workbook = Workbook()
        sheet = workbook.active
        sheet['A1'] = 'Simple Numbers'
        sheet['B1'] = 'Prime Numbers'
        sheet['C1'] = 'Fibonacci Numbers'

        sheet['D1'] = 'Average of Simple Numbers'
        sheet['E1'] = 'Average of Prime Numbers'
        sheet['F1'] = 'Total Sum'
        sheet['D2'] = average_simple
        sheet['E2'] = average_prime
        sheet['F2'] = total_sum

        sheet_lock = threading.Lock()

        def write_numbers_to_column(column, value):
            with sheet_lock:
                for i, num in enumerate(value, start=2):
                    sheet[f'{column}{i}'] = num

        thread_a = threading.Thread(target=write_numbers_to_column, args=("A", simple_numbers))
        thread_b = threading.Thread(target=write_numbers_to_column, args=("B", prime_numbers))
        thread_c = threading.Thread(target=write_numbers_to_column, args=("C", fibonacci_numbers))

        thread_a.start()
        thread_b.start()
        thread_c.start()

        thread_a.join()
        thread_b.join()
        thread_c.join()

        labels = ['Simple Numbers', 'Prime Numbers']
        sizes = [len(simple_numbers), len(prime_numbers)]
        colors = ['red', 'green']
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Simple and prime number comparison chart')
        plt.text(0, 0, f'Avg Simple: {round(average_simple)}\nAvg Prime: {round(average_prime)}\nTotal Sum: {round(total_sum)}',
             horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes, fontsize=6)

        chart_image_url: str = f'number_comparison_{start}_{end}.png'
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        plt.savefig("static/" + chart_image_url)
        plt.close()

        img = Image(image_stream)
        img.anchor = 'D5'
        sheet.add_image(img)

        workbook.save("static/" + filename)

        return render_template('result.html', filename=filename, chart_image_url=chart_image_url)
    except Exception as e:
        return "ERROR: {}".format(str(e))
    
@app.route('/download/<filename>')
def download(filename: str):
    try:
        return send_file("../static/" + filename, as_attachment=True)
    except Exception as e:
        return "ERROR: {}".format(str(e))