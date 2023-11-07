from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, render_template, request, jsonify
from ExcelPasswordRemover import removePassword
from ResumeExtractor import extract_resumes

import os
import shutil
import base64
import tempfile


app = Flask(
    __name__,
    template_folder='frontend/templates',
    static_url_path='/frontend/static',
    static_folder='frontend/static'
)

# Define a function to add the necessary CORS headers to responses
def add_cors_headers(response):
    # Replace '*' with the specific domain of your React app if needed
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    return response

# Register the CORS headers function as a after_request handler
app.after_request(add_cors_headers)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/extract_resume')
def extract_resume():
    return render_template('resume_extractor.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({
            'Result': 'ERROR',
            'Message': 'File not found'
        }), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'Result': 'ERROR',
            'Message': 'File name not found'
        }), 400

    try:
        if not os.path.exists('import'):
            os.makedirs('import')
        if not os.path.exists('export'):
            os.makedirs('export')
        import_path = os.path.join('import', file.filename)

        file.save(import_path)
        export_file, exception = removePassword('import', 'export')
        if export_file is None and exception != '':
            return jsonify({
                'Result': 'ERROR',
                'Message': exception
            }), 400
        # Read the binary content of the Excel file
        with open(export_file, 'rb') as file:
            excel_binary = file.read()

        # Encode the binary content as base64
        excel_base64 = base64.b64encode(excel_binary).decode('utf-8')
        return jsonify({
            'Result': 'OK',
            'Message': 'File password removed successfully.',
            'Binary': excel_base64,
            'FileName': os.path.basename(export_file)
        }), 200
    except Exception as e:
        return jsonify({
            'Result': 'ERROR',
            'Message': str(e)
        }), 400
    finally:
        shutil.rmtree('import', ignore_errors=True)
        shutil.rmtree('export', ignore_errors=True)


@app.route('/upload_resumes', methods=['POST'])
def upload_resumes():
    try:
        files = request.files.getlist('files[]')
        keywords = request.form.get('keywords')

        if not files:
            return jsonify({
                'Result': 'ERROR',
                'Message': 'No files provided'
            }), 400

        # Create a unique temporary folder
        app_dir = os.path.dirname(__file__)
        temp_folder = tempfile.mkdtemp(dir=app_dir)

        # Save each file to the temporary folder
        for file in files:
            filename = os.path.join(temp_folder, file.filename)
            file.save(filename)

        keyword_list = [keyword.strip() for keyword in keywords.split(',')]
        shortlisted_resumes, no_match_resumes = extract_resumes(temp_folder, keyword_list)
        shutil.rmtree(temp_folder)

        return jsonify({
            'Result': 'OK',
            'Message': 'Resume files extracted successfully.',
            'ShortListed': shortlisted_resumes,
            'NoMatch': no_match_resumes
        }), 200
    except Exception as e:
        return jsonify({
            'Result': 'ERROR',
            'Message': str(e)
        }), 400


if __name__ == '__main__':
    app.run(debug=True)

