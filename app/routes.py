import os
from flask import (
    flash, render_template, request,
    redirect, send_from_directory, url_for)
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename

import label2pdf
from app import app
from app import db
from app.constants import OUTPUT_FOLDER, UPLOAD_FOLDER
from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.faq import FAQ


# UTLIS #
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() \
           in app.config['ALLOWED_EXTENSIONS']


# CONTEXT PROCESSORS #
@app.context_processor
def inject_loginforms():
    loginform = LoginForm()
    registrationform = RegistrationForm()
    return dict(loginform=loginform, registrationform=registrationform)


# ROUTES #
@app.route('/donate')
def donate():
    return render_template('donate.html')


@app.route('/faq')
def faq():
    return render_template('faq.html', faq=FAQ)


@app.route('/convert/<filename>')
def get_pdf(filename):
    filename += ".pdf"
    return send_from_directory(os.path.join(os.getcwd(),
                                            app.config[OUTPUT_FOLDER]),
                               filename, as_attachment=True)


@app.route('/how')
def how():
    return render_template('how.html')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return {"error": "auth"}

        if 'file' not in request.files:
            flash('No files uploaded', 'danger')
            return redirect(request.url)
        files = request.files.getlist("file")
        file = files[0]
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(os.getcwd(), app.config[UPLOAD_FOLDER],
                                filename)
            file.save(path)
            output_path = os.path.join(os.getcwd(), app.config[OUTPUT_FOLDER],
                                       filename)

            pdf = label2pdf.Label(path=path,
                                  output_path=output_path)
            return pdf.name

    return render_template("home.html")


@app.route('/welcome')
def signin_or_up():
    if current_user.is_authenticated:
        return redirect(url_for('upload_file'))
    loginform = LoginForm()
    registrationform = RegistrationForm()
    return render_template('registerorlogin.html', title='Sign In',
                           loginform=loginform,
                           registrationform=registrationform)


@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return {"error": "Username or password incorrect"}
        login_user(user, remember=form.remember_me.data)
        return {"success": True}
    return {"error": "Form not filled correctly"}


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('upload_file'))


@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return {"success": True}
    else:
        return {"errors": form.errors}
