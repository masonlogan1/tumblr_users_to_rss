from RSSifier.converter import create_csv_from_file

from flask import Flask
from flask import render_template, request, url_for, send_file

from io import BytesIO, StringIO

ALLOWED_TYPES = ('txt', 'doc', 'docx', 'csv', 'xml', 'xlsx', 'xls', 'pdf',
                 'html')

app = Flask('app', template_folder='templates', static_folder='static')

global recent_files

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/tumblrss/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request', 400
    create_csv_from_file(request.files['file'], (data := StringIO()))
    print(data.read())
    data = BytesIO(data.getvalue().encode())
    return send_file(data, download_name='tumblr_rss.csv', mimetype='text/csv', as_attachment=True)
