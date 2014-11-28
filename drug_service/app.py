#!flask/bin/python

from flask import Flask
from flask import request
from flask import jsonify
from flask import abort



import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory

from DrugAnalyzer import *


UPLOAD_FOLDER = '/home/user/wspace/labs/python/rest/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return "Know your drug -> Drug service"


@app.route('/drug_service/api/v1/check', methods=['POST'])
def check():
    if not request.json or not 'drug' in request.json:
         abort(400)

    #print "Drug check service called"
    drug = {
        'name': request.json['drug']
        # compound = {
        #     'compound': request.json['compound'],
        #     'weightage': request.json['weightage']
        # }
    }

    #print request.json
    d = DrugAnalyzer(request.json)
    d.add_summary("Summary item 1")
    d.check_data()
    # d.output()
    #
    # analysis = {
    #     'drug': request.json['drug'],
    #     'message' : "Drug analysis report goes here",
    #     'caution' : 'Not available'
    # }

    #return jsonify({'analysis': analysis}), 201
    return d.output(),201


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @app.route('/drug_service/api/v1/upload', methods=['GET', 'POST'])
# def upload_file():
#     print app.config['UPLOAD_FOLDER']
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#     return "file uploaded"

@app.route('/drug_service/api/v1/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))

@app.route('/drug_service/api/v1/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# @app.route('/drug_service/api/v1/uploads/<filename>')
# def uploaded_file(filename):
#     print app.config['UPLOAD_FOLDER']
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

if __name__ == '__main__':
    app.run(debug=True)



