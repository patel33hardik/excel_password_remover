# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, jsonify
import os

app = Flask(
    __name__,
    template_folder='frontend/templates',
    static_url_path='/frontend/static',
    static_folder='frontend/static'
)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    print('----------test-{}------'.format(request.files))
    if 'file' not in request.files:
        return jsonify({
            'Result': 'ERROR',
            'Message': 'No file part'
        })
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'Result': 'ERROR',
            'Message': 'No selected file'
        })
    if file:
        import_path = os.path.join(
            'import', file.filename
        )
        file.save(import_path)
        return jsonify({
            'Result': 'OK',
            'Message': 'File uploaded successfully'
        })


if __name__ == '__main__':
    app.run(debug=True)

