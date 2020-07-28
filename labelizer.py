from time import sleep
import os
from flask import Flask, flash, render_template, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename

import label2pdf

UPLOAD_FOLDER = 'upload'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.secret_key = "RANDOMMMMSKEY"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/convert/<filename>', methods=['GET'])
def get_pdf(filename):
    filename += ".pdf"
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No files uploaded', 'danger')
            return redirect(request.url)
        files = request.files.getlist("file")
        # if user does not select file, browser also
        # submit an empty part without filename
        file = files[0]
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pdf = label2pdf.Label(path=os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                  output_path=os.path.join(app.config['OUTPUT_FOLDER'], filename))
            return pdf.name

    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=True, passthrough_errors=True)