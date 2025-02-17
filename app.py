from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee_management.db'
app.config['SECRET_KEY'] = "secretkey"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    return Employee.query.get(int(userid))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    department = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route("/")
def home():
    return render_template('register.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name_html = request.form['name']
        department_html = request.form['department']
        password_html = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password_html).decode('utf-8')
        employee = Employee(name=name_html, department=department_html, password=hashed_password)
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('login'))
    return "TEST"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name_login = request.form['name']
        password_login = request.form['password']
        employee = Employee.query.filter_by(name=name_login).first()
        if employee and bcrypt.check_password_hash(employee.password, password_login):
            login_user(employee)
            return "Logged in successfully"
    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
