from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm, EditForm
from .models import User, Contact
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
      g.user.last_seen = datetime.utcnow()
      db.session.add(g.user)
      db.session.commit()

@app.route('/')

@app.route('/login', methods=['GET'])
def login_form():

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_process():

    user_login = request.form["username"]
    user_password = request.form["password"]

    user = User.query.filter_by(user_login=user_login).first()

    if not user:
        flash("User does not exist. Please try again")
        return redirect("/login")

    if user.user_password != user_password:
        flash("Password is not correct. Please try again.")
        return redirect("/login")

    # session["user_id"] = user.user_id

    flash("You are logged in!")
    return redirect("/index")

@app.route('/index')
@login_required
def index():
    user = g.user
    notes = [
        {
            'author': {'nickname': 'Foz'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Gonz'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           notes=notes)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
  user = User.query.filter_by(nickname=nickname).first()
  if user == None:
    flash('User %s not found.' % nickname)
    return redirect(url_for('index'))
  notes = [
    {'author': user, 'body': 'Test reminder #1'},
    {'author': user, 'body': 'Test reminder #2'}
  ]
  return render_template('user.html',
                         user=user,
                         notes=notes)

@app.route('/contact/new', methods=['GET'])
def new_contact_form():

    return render_template("contact_new.html")

@app.route('/contact/new', methods=['POST'])
def new_contact_info():

    date_created = datetime.now()
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    middle_name = request.form["middle_name"]
    email = request.form['email']
    phone = request.form['phone']
    street_address_1 = request.form['address_1']
    street_address_2 = request.form['address_2']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zip_code']
    company = request.form['company']
    position = request.form['position']
    notes = request.form['note']

    new_contact = Contact(date_created=date_created, first_name=first_name, last_name=last_name, middle_name=middle_name, email=email, phone=phone, street_address_1=street_address_1, street_address_2=street_address_2, city=city, state=state, zip_code=zip_code, company=company, position=position, notes=notes)
    db.session.add(new_contact)
    db.session.commit()

    flash("Contact %s added." % first_name)
    return redirect(url_for('index'))

@app.route('/contact_list', methods=['POST'])
def contact_list():

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    
    contacts = Contact.query.filter_by(first_name=first_name, last_name=last_name).all()

    if not contacts:
        flash("Contact does not exist. Please try again")
        return redirect('/index')
    

    return render_template('contact_list.html', contacts=contacts, first_name=first_name, last_name=last_name)

@app.route('/contact/<int:id>', methods=['GET'])
def contact_list_view(id):

    contacts = Contact.query.filter_by(id = id).all()
    for contact in contacts:

        return render_template("contact_view.html", contacts=contacts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
  form = EditForm(g.user.nickname)
  if form.validate_on_submit():
    g.user.nickname = form.nickname.data
    db.session.add(g.user)
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('edit'))
  else:
    form.nickname.data = g.user.nickname
  return render_template('edit.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
