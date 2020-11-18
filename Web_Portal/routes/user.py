from .__view_imports import *
@app.route('/login', methods=('GET', 'POST') )
def login():
    form: forms.users.Login = forms.users.Login()
    if form.validate_on_submit():
        user: User = User()
        user.username = str(str(escape(form.username.data)))
        user.password = str(str(escape(form.password.data)))
        user = user.get_user()
        if user is None:
            flash('Invalid Login!', 'danger')
        elif user.locked:
            flash('Account Locked!', 'danger')
        elif not user.verified:
            flash('Account Not Verified: Please check email to verify account!', 'danger')
        elif user.verify_login(escape(form.password.data)):
            session['username'] =  user.username
            session['admin'] = user.admin
            return user_home(session.get('username'))
        else:
            flash('Invalid Login!', 'danger')
    for er in form.errors:
        flash(er, 'danger')    
    return render_template('user/login.html', form=form, title='Login')

@app.route('/register', methods=('GET', 'POST'))
def register():
    form: forms.users.Register  = forms.users.Register()
    if form.validate_on_submit():
        user: User = User()
        profile: Profile = Profile()

        user.username = str(escape(form.username.data))
        user.password = str(escape(form.password.data))
        user.email = str(escape(form.email.data))
        user.created = datetime.now()
        user.verification_key =  secrets.token_hex(32)
        
        profile.first_name = str(escape(form.first_name.data))
        profile.last_name = str(escape(form.last_name.data)) 
        profile.address1 = str(escape(form.address1.data))
        profile.address2 = str(escape(form.address2.data))
        profile.city = str(escape(form.city.data))
        profile.state = str(escape(form.state.data))
        profile.zip = str(escape(form.zip.data))
        profile.home_phone = str(escape(form.home_phone.data))
        profile.mobile_phone = str(escape(form.mobile_phone.data))
        user.profile = profile

        if user.exists():
            flash("Username Taken! Please try again", 'info')
            return render_template('/admin/users/add.html', form=form, title='Add')
        elif User.get_first(email=user.email):
            flash("Email Already Registered! Please try again", 'info')
        else:
            user.add()
            if user.exists():
                flash("User Registered! Please validate email.")
                Email.send_verifaction(user)
                return redirect(url_for("home"))
            else:
                flash("Registration Failed")

    for er in form.errors:
        flash(er, 'danger')
    return render_template('/user/register.html', form=form, title='Register')
    
@app.route('/logout', methods=('GET', 'POST'))
@LoginRequired
def logout():
    session.clear() 
    return redirect(url_for("home"))

@app.route('/user/<username>')
@LoginRequired
def user_home(username):
    return redirect(url_for('meeting_view_redirect'))

@app.route('/user/forgot/<token>', methods=('GET', 'POST'))
def verify_forgot(token):
    user = User.verify_reset_token(token)
    form: forms.users.New_Password = forms.users.New_Password()
    if user.failed:
        flash(user.reason_fail, 'warning')
        return redirect(url_for('login'))
    elif form.validate_on_submit():
        if len(user.password) > 0:
            user.password = str(escape(form.password.data))
            user.update_pw()
            flash("Password Updated",'info')
            return redirect(url_for('login'))
    return render_template('/user/new_password.html', form=form, token=token)

@app.route('/user/forgot', methods=('GET', 'POST'))
def forgot():
    form: forms.users.Forgot_Password = forms.users.Forgot_Password()
    if form.validate_on_submit():
        user: User = User.get_first(email=str(escape(form.email.data)))
        if user:
            Email.send_forgot_password(user)
        flash ("Password reset link sent, Please check your email for link", 'info' )
        return redirect(url_for('login'))
    return render_template('./user/forgot.html', form=form)

@app.route('/user/<username>/password', methods=('GET', 'POST'))
@LoginRequired
def password(username):
    user: User = User(username=username).get_user()
    form: forms.users.Change_Password = forms.users.Change_Password()
    if form.validate_on_submit():
        user.password = escape(form.password.data)
        user.update_pw()
        flash('Password Updated!','info')
        return redirect(url_for('user_home', username=username))
    for error in form.errors:
        flash(error)

    return render_template('./user/password.html', form=form, user=user)

@app.route('/user/<username>/profile', methods=('GET', 'POST'))
@LoginRequired
def profile(username):
    """
    """
    user: User = User(username=username).get_user()
    profile: Profile = user.profile
    form: forms.users.Update = forms.users.Update()
  
    if form.validate_on_submit():
        profile.first_name = str(escape(form.first_name.data))
        profile.last_name = str(escape(form.last_name.data))
        profile.address1 = str(escape(form.address1.data))
        profile.address2 = str(escape(form.address2.data))
        profile.city = str(escape(form.city.data))
        profile.state = str(escape(form.state.data))
        profile.zip = str(escape(form.zip.data))
        profile.home_phone = str(escape(form.home_phone.data))
        profile.mobile_phone = str(escape(form.mobile_phone.data))
        user.email = str(escape(form.email.data))
        user.profile = profile
        user.update()
        flash("Profile Updated!",'info')
        return redirect(url_for('home'))
    for error in form.errors:
        flash(error)

    return render_template('./user/profile.html', form=form, user=user)

@app.route('/verify/<username>/<key>')
def new_user_verify(username, key):
    user: User = User(username=username).get_user()
    if key == user.verification_key:
        user.verified = True
        user.update()
        flash("Email Verified",'info')
        return redirect(url_for('login'))
    else:
        # add email sender
        return render_template('./error_pages/email_verify_error.html')