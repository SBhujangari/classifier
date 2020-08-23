# Mostly working, for the indents I reindented it, probably was a mix of spaces and indents
# causing the problem. I haven't run it locally with tf yet, but all the parameters are there
# The below is thrown cause I haven't installed anything yet
# ModuleNotFoundError: No module named 'tensorflow'
# I think it tried to automatically run and create pycache, but that can be deleted
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    session,
    flash,
)
from flask_uploads import configure_uploads, UploadSet, IMAGES
from flask_wtf import FlaskForm
from wtforms import FileField
import os
from werkzeug.utils import secure_filename
import urllib.request
from peddie import predict_image, predict_sentence


UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

app = Flask(__name__)

app.config["SECRET_KEY"] = "secretkey"
app.config["UPLOADED_IMAGES_DEST"] = "uploads/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

images = UploadSet("images", IMAGES)
configure_uploads(app, images)


class MyForm(FlaskForm):
    image = FileField("image")


@app.route("/api", methods=["GET"])
def api():
    return {"userId": 1, "title": "Flask React Application", "completed": False}


@app.route("/test", methods=["POST"])
def test():
    data = request.form["title"]
    return {"title": data}


@app.route("/etc", methods=["GET", "POST"])
def index():
    form = MyForm()

    if form.validate_on_submit():
        filename = images.save(form.image.data)
        return render_template("index.html", form=form)

        return render_template("index.html", form=form)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def upload_form():
    return render_template("page.html")


@app.route("/", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("Select An Image")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash("Image successfully uploaded and displayed")
        # Passed in the filename, not the filepath
        # The text is in request.form['post']
        # I'm not sure if predict_sentence is supposed to be called seperately
        # predict_image(filename)
        predict_sentence(request.form["post"])
        return render_template("page.html", filename=filename, request=request)
    else:
        flash("We only accept png, jpg, jpeg, gif")
        return redirect(request.url)


@app.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for("static", filename="uploads/" + filename), code=301)


if __name__ == "__main__":
    app.run()
