from flask import Flask, jsonify, redirect, request, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object("project.config.Config")

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return """
<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>Upload</title></head>
  <body>
    <h1>Upload an image</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/*" required>
      <button type="submit">Upload</button>
    </form>
  </body>
</html>
"""

    uploaded_file = request.files.get("file")
    if uploaded_file is None or uploaded_file.filename == "":
        return "No file selected", 400

    filename = secure_filename(uploaded_file.filename)
    if filename == "":
        return "Invalid filename", 400

    uploaded_file.save(f"{app.config['MEDIA_FOLDER']}/{filename}")
    return redirect(url_for("mediafiles", filename=filename))


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)
