from .._form_imports import *

class Edit(FlaskForm):

    title = StringField("Title", [DataRequired()])
    description = TextAreaField("Description")
    date = DateField("Date", [DataRequired()],  default=datetime.today)
    video = FileField("Zoom Recording")
    files = MultipleFileField("Documents")