from flask import Flask, render_template, request, jsonify, send_file
import os
from REP import removePassword

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

    if file:
        if not os.path.exists('import'):
            os.makedirs('import')

        import_path = os.path.join('import', file.filename)
        file.save(import_path)
        export_file = removePassword('import', 'export')

        return send_file(export_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

