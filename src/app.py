import logging

from RSSifier.converter import create_csv_from_file

from flask import Flask
from flask import render_template, request, url_for, send_file

from io import BytesIO, StringIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ALLOWED_TYPES = ('txt', 'doc', 'docx', 'csv', 'xml', 'xlsx', 'xls', 'pdf',
                 'html')

app = Flask('app', template_folder='templates', static_folder='static')

global recent_files

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request', 400
    create_csv_from_file(request.files['file'], (data := StringIO()))
    logger.debug('Converting output to bytes')
    data = BytesIO(data.getvalue().encode())
    logger.info('Sending file')
    return send_file(data, download_name='tumblr_rss.csv', mimetype='text/csv', as_attachment=True)
