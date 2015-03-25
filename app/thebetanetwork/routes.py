from thebetanetwork import app
from flask import Flask, render_template, request, flash, session, url_for, redirect
from forms import LeadForm, SignupForm, SigninForm
from flask_mail import Message, Mail
from models import db, User


mail = Mail()


@app.route('/', methods=['GET', 'POST'])
def home():
    form = LeadForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('home.html', form=form)
        else:
            msg = Message(subject='Lead from Beta Network', sender='notificationsbetanetwork@gmail.com', recipients=['your_email@example.com'])
            msg.body = """
            From: %s %s <%s>

            Lead submitted from The Beta Network.
            """ % (form.firstname.data, form.lastname.data, form.email.data)
            mail.send(msg)

            return render_template('home.html', success=True)

    elif request.method == 'GET':
        return render_template('home.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if 'email' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('profile'))

            return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('signin'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_form('signin'))
    else:
        return render_template('profile.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()

    if 'email' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.emai.data
            return redirect(url_for('dashboard'))

    elif request.method == 'GET':
        return render_template('signin.html', form=form)

@app.route('/signout')
def signout():

    if 'email' not in session:
        return redirect(url_for('signin'))

    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return "It works."
    else:
        return "Something is broken."
