from flask import (
    Flask,
    render_template, redirect, url_for,
    flash, request, session
)
import os
from email_verify import VerifyEmail
from Database.user import MyDB
from forms import SignupForm, LoginForm

# Connect the database
db = MyDB()

# Use the Framework
app = Flask(__name__)
app.config["SECRET_KEY"] = "this_is_a_secret_key"


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",title="Home")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        em = form.email.data
        gender = form.gender.data
        dob = form.dob.data
        pw = form.password.data

        v = VerifyEmail()

        if em:  # Ensure the email is not None
            if v.email_verify_smtp(em):
                flash("Email Validated Successfully!")
                response = db.insert_one_data(username, em, gender, dob, pw)
                flash(f"Successfully Registered {form.username.data} , {response}!")
            else:
                flash("Invalid email address!")

            return redirect(url_for("home"))

    return render_template("signup.html",title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Ensure form is submitted and valid
        em = form.email.data
        pw = form.password.data

        if em:  # Ensure the email is not None
            if db.search(email=em,password=pw):
                flash("Logged In successfully!!")
            else:
                flash("Email or password is Incorrect!!")
        else:
            flash("Email is required!")

        return redirect(url_for("home"))

    return render_template("login.html", title="Login", form=form)

@app.route("/generate_text", methods=["GET", "POST"])
def generate_text():
    if 'history' not in session:
        session['history'] = []

    if request.method == "POST":
        pdf_file = request.files.get('pdf_file')
        input_text = request.form.get('input_text')
        # Here you would generate text and add it to the session history
        generated_text = "Sample Generated Text"  # Replace with actual generation logic
        session['history'].append(generated_text)

    return render_template("generate_text.html", title="Generate Text", history=session['history'])


if __name__ == "__main__":
    app.run(debug=True)