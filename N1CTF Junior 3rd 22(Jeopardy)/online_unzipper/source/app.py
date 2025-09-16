import os
import uuid
from flask import Flask, request, redirect, url_for,send_file,render_template, session, send_from_directory, abort, Response

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "test_key")
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

users = {}

@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("upload"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return "用户名已存在"

        users[username] = {"password": password, "role": "user"}
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["username"] = username
            session["role"] = users[username]["role"]
            return redirect(url_for("upload"))
        else:
            return "用户名或密码错误"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        file = request.files["file"]
        if not file:
            return "未选择文件"

        role = session["role"]

        if role == "admin":
            dirname = request.form.get("dirname") or str(uuid.uuid4())
        else:
            dirname = str(uuid.uuid4())

        target_dir = os.path.join(UPLOAD_FOLDER, dirname)
        os.makedirs(target_dir, exist_ok=True)

        zip_path = os.path.join(target_dir, "upload.zip")
        file.save(zip_path)

        try:
            os.system(f"unzip -o {zip_path} -d {target_dir}")
        except:
            return "解压失败，请检查文件格式"

        os.remove(zip_path)
        return f"解压完成！<br>下载地址: <a href='{url_for('download', folder=dirname)}'>{request.host_url}download/{dirname}</a>"

    return render_template("upload.html")

@app.route("/download/<folder>")
def download(folder):
    target_dir = os.path.join(UPLOAD_FOLDER, folder)
    if not os.path.exists(target_dir):
        abort(404)

    files = os.listdir(target_dir)
    return render_template("download.html", folder=folder, files=files)

@app.route("/download/<folder>/<filename>")
def download_file(folder, filename):
    file_path = os.path.join(UPLOAD_FOLDER, folder ,filename)
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return Response(
            content,
            mimetype="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
