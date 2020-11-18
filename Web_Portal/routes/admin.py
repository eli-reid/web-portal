from .__view_imports import *

#########################################################################
#                             Admin Routes                              #
#########################################################################

@app.route('/admin')
@AdminRequired
def admin():
    return redirect(url_for('useradmin'))

@app.route('/admin/users')
@AdminRequired
def useradmin():
    
    return render_template('/admin/users/users.html', 
                            users=User.get_all(),
                            current_user=session.get('username')
                            )

#########################################################################
#                            User Admin Routes                          #
#########################################################################

@app.route('/admin/users/add')
@AdminRequired
def useradmin_add():
    title: str = "Add User"
    form: forms.users.Add = forms.users.Add()
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
            return render_template('/admin/users/add.html', form=form, title='Add')
        else:
            user.add()
            # verify user was added 
            if user.exists():
                flash("User Added")
                return redirect(url_for("useradmin"))
            else:
                flash("Add User Failed")

    for er in form.errors:
        flash(er, 'danger')
    return  render_template('/admin/users/add.html', form=form, title=title)

@app.route('/admin/users/edit/<id>')
@AdminRequired
def useradmin_edit(id):
    user: User = User.get_by_id(id)
    form: forms.users.Edit = forms.users.Edit()
    return  render_template('/admin/users/update.html', user=user, form=form)

@app.route('/admin/users/delete/<id>')
@AdminRequired
def useradmin_delete(id):
    user: User = User.get_by_id(id)
    if user:
        user.delete()
    return  redirect('useradmin')

@app.route('/admin/users/tg_admin/<id>')
@AdminRequired
def toggle_admin(id):
    user: User = User.get_by_id(id)
    if user.exists():
        if user.admin:
            user.admin = False
        else:
            user.admin = True
        user.update()
    return redirect(url_for("useradmin"))

@app.route('/admin/users/tg_lock/<id>')
@AdminRequired
def toggle_locked(id):
    user: User = User.get_by_id(id)
    if user.exists():
        if user.locked:
            user.locked = False
        else:
            user.locked = True
        user.update()
    return redirect(url_for("useradmin"))

@app.route('/admin/users/tg_verify/<id>')
@AdminRequired
def toggle_verified(id):
    user: User = User.get_by_id(id)
    if user.exists():
        if user.verified:
            user.verified  = False
        else:
            user.verified = True
        user.update()
    return redirect(url_for("useradmin"))