from .__view_imports import *
#########################################################################
#                             file Routes                            #
#########################################################################

@app.route('/admin/meeting/add', methods=('GET', 'POST') )
@AdminRequired
def meeting_add():
    title = "Meetings - Add"
    form: forms.meetings.Add = forms.meetings.Add()
    meeting: Meeting = Meeting()
    if form.validate_on_submit():
        date = datetime.strptime(str(escape(form.date.data)), '%Y-%m-%d')
        meeting.title = str(escape(form.title.data))
        meeting.description = str(escape(form.description.data))
        meeting.date = date
        meeting.dir = os.path.join(app.config.get('UPLOAD_FOLDER'), secure_filename(str(form.date.data)))

        if meeting.exists():
            flash(f"Meeting {meeting.title} already exists on for this '{date}'")
            return render_template('./meetings/add.html', form=form, title=title)
                
        # get file values from form file inputs
        video = request.files.get('video', None)
        files = request.files.getlist('files', None)
        
        # check for files 
        if not video and not files:
            flash("No files Selected", 'info')
            return render_template('./meetings/add.html', form=form, title=title)
           
        # upload files
        video_name, file_names = upload(video, files, meeting.dir)
        meeting.video = video_name
        meeting.documents = file_names
        meeting.add()
        if not meeting.exists():
            flash("UPLOAD FAILED ", "danger")
        else:
            flash("Meeting Added!", "info")
        return redirect(url_for('meeting_add'))
    return render_template('./meetings/add.html', form=form)


@app.route('/admin/meeting/edit/<id>', methods=('GET', 'POST') )
@AdminRequired
def meeting_edit(id):
    title= "Meeting - Edit"
    form: forms.meetings.Edit = forms.meetings.Edit()
    meeting: Meeting = Meeting.get_by_id(id)
    
    prev_dir = None
    if form.validate_on_submit():
        date = datetime.strptime(str(escape(form.date.data)), '%Y-%m-%d')
        meeting.title = str(escape(form.title.data))
        meeting.description = str(escape(form.description.data))
       
        if meeting.date != date:
            prev_dir = meeting.dir
            meeting.date = date
            meeting.dir = os.path.join(app.config.get('UPLOAD_FOLDER'), secure_filename(str(form.date.data)))
            if meeting.documents :
                meeting.documents = move_files(prev_dir, meeting.dir, meeting.documents)

            if meeting.video != '':
               meeting.video = move_files(prev_dir, meeting.dir, [meeting.video])[0]
    
        
        video = request.files.get('video', None)
        files = request.files.getlist('files', None)
        video_name, file_names = upload(video, files, meeting.dir)

        meeting.video = meeting.video or video_name 
        if meeting.documents:
            meeting.documents = file_names.extend(meeting.documents)
        else:
            meeting.documents = file_names or []
        meeting.update()
    else:   
        form.description.data = unescape(meeting.description)



    return render_template('./meetings/edit.html', meeting=meeting,form=form,title=title)

@app.route('/admin/meeting/manage', methods=('GET', 'POST') )
@AdminRequired
def meeting_manage(page=1, per_page=10):
    title = "Meetings - Manage "
    meetings: Meeting = Meeting.paginate(int(page), int(per_page), False, order_by=Meeting.id.desc())
    next_url = url_for('/meetings/manage.html', page=meetings.next_num)\
        if meetings.has_next else None
    prev_url = url_for('/meetings/manage.html', page=meetings.prev_num)\
        if meetings.has_prev else None
    return render_template('./meetings/manage.html',
                            title=title, 
                            page=page,
                            meetings=meetings)

@app.route('/meetings/<page>/<per_page>')
@LoginRequired
def meeting_view(page=1, per_page=10):
    title = "Meetings"
    user: User = User(username=session.get('username')).get_user()
    meetings: Meeting = Meeting.paginate(int(page), int(per_page), False, order_by=Meeting.id.desc())
    return render_template('/meetings/view.html',
                            title=title,
                            user=user, 
                            per_page=per_page,
                            meetings=meetings)

@app.route('/meetings')
def meeting_view_redirect():
    return redirect(url_for('meeting_view', page=1, per_page=10))


@app.route('/admin/meetings/delete/<id>')
@AdminRequired
def meeting_delete(id):
    meeting: Meeting = Meeting.get_by_id(int(id))
    if meeting.video:
        delete_file(meeting.dir,meeting.video)
    
    for doc in meeting.documents:
        delete_file(meeting.dir,doc)

    meeting.delete()
    return "", 200


@app.route('/meeting_exists/<date>/<title>')
@app.route('/meeting_exists/')
@AdminRequired
def meeting_exists(date ='', title=''):
        meeting: Meeting = Meeting()
        msg =f"Meeting {title} already exists on for this '{date}'"
        date = str(escape(date))
        title = str(escape(title))
        meeting.date = datetime.strptime(date, '%Y-%m-%d')
        meeting.title = title
        if meeting.exists():
            return msg , 200, {'Content-Type': 'text/markdown'}
        else:
            return 'false', 200, {'Content-Type': 'text/markdown'}


@app.route('/download/<date>/<file>')
@LoginRequired
def download(date, file):
    file_path = ".." + os.sep + app.config.get('UPLOAD_FOLDER') + os.sep + date + os.sep + file
    return send_file(file_path) 

@app.route('/admin/meeting/<id>/<file>/delete/')
@AdminRequired
def file_delete(id, file):
    meeting: Meeting = Meeting.get_by_id(id)
    if meeting.video == file:
        meeting.video=""
    elif file in meeting.documents:
            docs = list(meeting.documents)
            docs.remove(file)
            meeting.documents = docs

    if os.path.exists(os.path.join(meeting.dir, secure_filename(file))):
        os.remove(os.path.join(meeting.dir, secure_filename(file)))
    meeting.update()
    return "", 200
    
def upload(video, files, path)-> tuple:
    file_names = []
    video_name = ''
    # make directory
    try:
        os.mkdir(path)
    except:
        pass
    # upload video
    if video and video.filename.split('.')[-1].lower() in app.config.get('ALLOWED_EXTENSIONS_VIDEO'):
        
        video_name = secure_filename(video.filename)
        if os.path.isfile(os.path.join(path, video_name)):
            video_name = rename_file(path, video_name)
        video.save(os.path.join(path, video_name))
        flash(f"Video file {video_name} uploaded", "success")

    # upload list of files  
    for file in files:
        if file and file.filename.split('.')[-1].lower() in app.config.get('ALLOWED_EXTENSIONS_DOCS'):
            filename = secure_filename(file.filename)
            if os.path.isfile(os.path.join(path, filename)):
                filename = rename_file(path, filename)
            file_names.append(filename)
            file.save(os.path.join(path, filename))
            flash(f"Document { filename } uploaded!", "success")
    return video_name, file_names

def delete_file(path, file)-> None:
    if os.path.exists(os.path.join(path, file)):
        os.remove(os.path.join(path, file))

    # delete directorey if emtpy           
    if os.path.exists(path) and len(os.listdir(path)) == 0:
        os.rmdir(path)
    return

def move_files(prev_path, path, filenames)-> list:
    try:
        os.mkdir(path)
    except:
        pass

    moved = list()

    for filename in filenames:
        prev_file_loc = os.path.join(prev_path, filename)
        new_file_loc = os.path.join(path, filename)
        # check file to move exists
        if os.path.isfile(prev_file_loc):
            new_filename = filename
            # check new path for duplicate named file
            if os.path.isfile(new_file_loc):
                new_filename = rename_file(path, filename)
            # move file         
            os.rename(os.path.join(prev_path, filename), os.path.join(path, new_filename))
            
            moved.append(new_filename)
    # delete directorey if emtpy           
    if os.path.exists(prev_path) and len(os.listdir(prev_path)) == 0:
        os.rmdir(prev_path)
    return moved

def rename_file(path, filename)-> str:
    for i in range(1000):
        new_filename = filename.replace('.', f'_{i}.')
        if not os.path.isfile(os.path.join(path, new_filename)):
            return new_filename