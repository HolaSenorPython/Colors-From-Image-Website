from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_wtf.file import FileAllowed, FileRequired

class UploadForm(FlaskForm):
    image_file = FileField("Insert your image here.", validators=[FileRequired(),
                                                                  FileAllowed(['jpg', 'png', 'jpeg'],
                                                                              "Only Images allowed.")])
    submit = SubmitField("Submit your Image! 📁")