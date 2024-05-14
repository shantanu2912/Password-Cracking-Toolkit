from flask import Flask, render_template, request, session, flash, redirect
from hybrid import PasswordCracker
from dictionary import DictionaryAttack
from brute_force import BruteForcePasswordCracker
from database import *
from werkzeug.utils import secure_filename
import os
import plotly.express as px
import pandas as pd
from password_generator import generate_password

app = Flask(__name__)
app.secret_key = "aksdjaksjd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pct.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_PATH'] = 'static/uploads'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pwd']
        db = get_db()
        user = db.query(User).filter(User.username==username).first()
        if user and user.password == password:
            session['uname'] = username
            session['id'] = user.id
            session['isauth'] = True
            db.close()
            return redirect('/application')
        else:
            return "Username or password is incorrect"
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        save_to_db(
            User(
                username = request.form['uname'],
                password = request.form['pwd']
            )
        )
        return f'User created'
    else:
        return render_template('register.html')

@app.route('/application', methods=['GET','POST'])
def project():
    if not session.get('isauth', False):
        return redirect("/login")
    if request.method == 'POST':
        if request.form['submit'] == 'Brute Force':
            brute = BruteForcePasswordCracker(request.form['max_length'])
            target_password = request.form['target_password'] or "a"
            brute.crack_password(target_password)
            flash("Task completed and logged", 'success')
        elif request.form['submit'] == 'Dictionary':
            dictionary = DictionaryAttack(dictionary_file = r"C:\Users\shantanu sharma\Downloads\words.txt")
            target_password = request.form['target_password']
            dictionary.crack_password(target_password)
            flash("Task Completed and logged", 'success')
        elif request.form['submit'] == 'Hybrid':
            hybrid = PasswordCracker(dictionary_file = r"C:\Users\shantanu sharma\Downloads\words.txt", max_length = request.form['max_length'])
            target_password = request.form['target_password']
            hybrid.load_dictionary()
            hybrid.crack_password(target_password)
            flash("Task Completed and logged", 'success')
        return redirect('/statistics')
    else:
        return render_template('application.html')
    

@app.route('/application/files/<int:fileid>', methods=['GET', 'POST'])
def project_files(fileid):
    if not session.get('isauth', False):
        return redirect("/login")
    db = get_db()
    upload = db.query(Upload).get(fileid)
    with open(upload.path, errors="ignore") as file:
        password_list = file.readlines()
        if not password_list:
            flash("No passwords in files",'danger')
        else:
            for password in password_list:
                hybrid = PasswordCracker(dictionary_file = r"static/dictionaries/words.txt", max_length = 10, fileid = fileid)
                hybrid.load_dictionary()
                hybrid.crack_password(password)
                flash("Task Completed and logged", 'success')
                return redirect('/statistics')
    return "error"


@app.route('/feedback', methods=['GET','POST'])
def feedback():
    if request.method == 'POST':
        save_to_db(
            Feedback(
                       feedback_content = request.form['feedback']
                    )
                )
        return f"Feedback submitted successfully"
    else:
        return render_template('feedback.html')

@app.route('/statistics')
def statistics():
    if not session.get('isauth', False):
        return redirect("/login")
    db = get_db()
    report = db.query(Report).order_by(Report.id.desc())

    if not report:
        return "No reports available"
    report_dict = []
    for row in report:
        report_dict.append(row.__dict__)
    df = pd.DataFrame(report_dict, columns=Report.__table__.columns.keys())
    fig1 = px.scatter(df, x='password', y='is_cracked', title='Password Cracking Report')
    #time consuming password
    fig2 = px.bar(df, x='password', y='time_taken', title='Time taken to crack password')
    table = df.to_html(classes='table table-striped table-hover')
    
    return render_template('statistics.html', report=report_dict[0], fig1 = fig1.to_html(full_html=False), fig2 = fig2.to_html(full_html=False), table = table)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('isauth', False):
        return redirect("/login")
    db = get_db()
    uploads = db.query(Upload).all()
    if request.method == "POST":
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        if filename != '':
            if not os.path.exists(app.config['UPLOAD_PATH']):
                os.makedirs(app.config['UPLOAD_PATH'])
            path = os.path.join(app.config['UPLOAD_PATH'],filename)
            file.save(path)
        save_to_db(Upload(path=path, user_id=session.get('id', 1)))
        flash("file uploaded successfully", 'success')
        return redirect('/upload')
    return render_template("upload.html", uploads=uploads)

@app.route('/view/<int:id>')
def get_upload_content(id):
    if not session.get('isauth', False):
        return redirect("/login")
    db = get_db()
    upload = db.query(Upload).get(id)
    with open(upload.path) as file:
        content = file.read()

    return content.splitlines()

@app.route('/delete/<int:fileid>')
def delete(fileid):
    db = get_db()
    upload = db.query(Upload).get(fileid)
    db.delete(upload)
    db.commit()
    return redirect('/upload')

@app.route('/save/password', methods=['GET', 'POST'])
def save_password_to_vault():
    if not session.get('isauth', False):
        return redirect("/login")
    if request.method == 'POST':
        title = request.form['title']
        password = request.form['password']
        if not title or not password:
            flash("Title and password are required", 'danger')
            return redirect('/application')
        db = get_db()
        save_to_db(
            Vault(
                passfor = title,
                password = password,
                user_id = session.get('id', 1)
            )
        )
        flash("Password added successfully to vault", 'success')
        return redirect('/application')
    
@app.route('/delete/password/<int:id>')
def delete_vault_password(id):
    db = get_db()
    vault = db.query(Vault).get(id)
    db.delete(vault)
    db.commit()
    flash("Password deleted successfully", 'success')
    return redirect('/vault')   
    
@app.route('/vault', methods=['GET', 'POST'])
def get_password_from_vault():
    if not session.get('isauth', False):
        return redirect("/login")
    db = get_db()
    vault = db.query(Vault).all()
    return render_template('vault.html', vault=vault)


# htmx api
@app.route('/generate/password')
def generate_password_api():
    password = generate_password()
    return password


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 