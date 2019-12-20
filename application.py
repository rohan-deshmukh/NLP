import glob
import os
import json
from werkzeug.utils import secure_filename
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from utils import excel_extractor, excel_writer, file_utility
from models import gensim_tfidf

# Flask object instantiation
application = Flask(__name__)

# CORS for download route
cors = CORS(application, resources={r"/*": {"origins": "*"}})

# Configure data import folders
PREV_UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/data/prev_q_data/'
NEW_UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/data/new_q_data/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/data/completed_q_data/'

# API Status messages
api_running_msg = {'resp': 'API is running!', 'status': 200}
file_msg = {'resp': 'Successfully uploaded file!', 'status': 200}
file_err_msg = {'resp': 'Not a valid file. Please upload only .xlsx files', 'status': 404}
curl_msg = {'resp': 'Please check the curl command', 'status': 404}
empty_dir_msg = {'resp': 'Please upload previous and new questionnaires', 'status': 404}
json_error = {'resp': 'Please send json formatted data only', 'status': 404}
json_post_msg = {'resp': 'Successfully sent json data', 'status': 200}

# Model object instantiation
model_obj = gensim_tfidf.Model()


@application.route('/')
def homepage():
    """Route to verify if API is working"""
    resp = jsonify(api_running_msg)
    resp.headers.add('Access-Control-Allow-Origin', 'https://xoro.ai')
    return resp


@application.route('/upload_previous_excel', methods=['POST'])
def upload_prev_excel():
    """Route for uploading previous questionnaires-excel"""
    if request.method == 'POST':
        f = request.files['file']
        # Delete files from Previous folder
        if f and file_utility.allowed_file(f.filename):
            file_utility.remove_files(PREV_UPLOAD_FOLDER)
            filename = secure_filename(f.filename)
            f.save(os.path.join(PREV_UPLOAD_FOLDER, filename))

            resp = jsonify(file_msg)
            resp.headers.add('Access-Control-Allow-Origin', 'https://xoro.ai')
            return resp
        else:
            resp = jsonify(file_err_msg)
            resp.headers.add('Access-Control-Allow-Origin', 'https://xoro.ai')
            return resp
    else:
        resp = jsonify(curl_msg)
        resp.headers.add('Access-Control-Allow-Origin', 'https://xoro.ai')
        return resp


@application.route('/upload_new_excel', methods=['POST'])
def upload_new_excel():
    """Route for uploading new questionnaire-excel"""
    if request.method == 'POST':
        f = request.files['file']
        # Delete files from New folder
        if f and file_utility.allowed_file(f.filename):
            file_utility.remove_files(NEW_UPLOAD_FOLDER)
            filename = secure_filename(f.filename)
            f.save(os.path.join(NEW_UPLOAD_FOLDER, filename))

            resp = jsonify(file_msg)
            resp.headers.add('Access-Control-Allow-Origin', 'https://xoro.ai')
            return resp
        else:
            resp = jsonify(file_err_msg)
            resp.headers.add('Access-Control-Allow-Origin', 'https://xoro.ai')
            return resp
    else:
        resp = jsonify(curl_msg)
        resp.headers.add('Access-Control-Allow-Origin', 'https://xoro.ai')
        return resp


@application.route('/download_excel', methods=['GET'])
def download_excel():
    """Route for downloading completed questionnaire-excel"""
    if request.method == 'GET':
        if not file_utility.isempty(PREV_UPLOAD_FOLDER):
            if not file_utility.isempty(NEW_UPLOAD_FOLDER):
                # Data extraction from answered questionnaires
                excel_qa_obj = excel_extractor.ExcelData(PREV_UPLOAD_FOLDER)
                qa_dict, q_list = excel_qa_obj.get_qa()

                # Model training
                model_obj.train_similarity(q_list)

                # Data extraction from new questionnaire
                excel_q_obj = excel_extractor.ExcelData(NEW_UPLOAD_FOLDER)
                new_q_list = excel_q_obj.get_q()

                # Get answers from previous questionnaires with max similarity score
                answered_list = model_obj.excel_response(qa_dict, q_list, new_q_list, model_obj)

                # Delete files from Download folder
                file_utility.remove_files(DOWNLOAD_FOLDER)

                # Write new answers to excel file
                excelwriter = excel_writer.Excelwrite(DOWNLOAD_FOLDER, answered_list)
                excelwriter.writedata()

                for filepath in glob.glob(DOWNLOAD_FOLDER + '*.xlsx'):
                    return send_file(filepath, as_attachment=True)
            else:
                resp = jsonify(empty_dir_msg)
                resp.headers.add('Access-Control-Allow-Origin', 'https://xoro.ai')
                return resp
        else:
            resp = jsonify(empty_dir_msg)
            resp.headers.add('Access-Control-Allow-Origin', 'https://xoro.ai')
            return resp
    else:
        resp = jsonify(curl_msg)
        resp.headers.add('Access-Control-Allow-Origin', 'https://xoro.ai')
        return resp


@application.route('/upload_previous_json', methods=['POST'])
def upload_prev_json():
    """Route for uploading previous questionnaires-json"""
    if request.method == 'POST':
        if request.json:
            json_data = request.json
            json_file = os.path.join(PREV_UPLOAD_FOLDER, 'old_q_data.json')
            # Delete files from previous folder
            file_utility.remove_files(PREV_UPLOAD_FOLDER)

            # Saving incoming json data to .json file
            with open(json_file, 'w') as outfile:
                json.dump(json_data, outfile)

            resp = jsonify(json_post_msg)
            resp.headers.add('Access-Control-Allow-Origin', '*')
            return resp
        else:
            resp = jsonify(json_error)
            resp.headers.add('Access-Control-Allow-Origin', '*')
            return resp
    else:
        resp = jsonify(curl_msg)
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp


@application.route('/upload_new_json', methods=['POST'])
def upload_new_json():
    """Route for uploading new questionnaires-json"""
    if request.method == 'POST':
        if request.json:
            json_data = request.json
            json_file = os.path.join(NEW_UPLOAD_FOLDER, 'new_q_data.json')
            # Delete files from new folder
            file_utility.remove_files(NEW_UPLOAD_FOLDER)

            # Saving incoming json data to .json file
            with open(json_file, 'w') as outfile:
                json.dump(json_data, outfile)

            resp = jsonify(json_post_msg)
            resp.headers.add('Access-Control-Allow-Origin', '*')
            return resp
        else:
            resp = jsonify(json_error)
            resp.headers.add('Access-Control-Allow-Origin', '*')
            return resp
    else:
        resp = jsonify(curl_msg)
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp


@application.route('/download_json', methods=['GET'])
def download_json():
    """Route for downloading completed questionnaire-json"""
    if request.method == 'GET':
        if not file_utility.isempty(PREV_UPLOAD_FOLDER):
            if not file_utility.isempty(NEW_UPLOAD_FOLDER):
                # Data extraction from answered questionnaires
                with open(glob.glob(os.path.join(PREV_UPLOAD_FOLDER, '*.json'))[0]) as jsonfile:
                    data = json.load(jsonfile)
                qa_dict = data["metadata"]
                q_list = [*(data['metadata']).keys()]

                # Model training
                model_obj.train_similarity(q_list)

                # Data extraction from new questionnaire
                with open(glob.glob(os.path.join(NEW_UPLOAD_FOLDER, '*.json'))[0]) as jsonfile:
                    data = json.load(jsonfile)
                new_q_list = data["metadata"]

                # Get answers from previous questionnaires with max similarity score
                answered_dict = model_obj.json_response(qa_dict, q_list, new_q_list, model_obj)

                # Delete files from Download folder
                file_utility.remove_files(DOWNLOAD_FOLDER)

                completed_json = {"type": "download_questionnaire", "metadata": answered_dict}
                resp = jsonify(completed_json)
                resp.headers.add('Access-Control-Allow-Origin', '*')
                return resp

            else:
                resp = jsonify(empty_dir_msg)
                resp.headers.add('Access-Control-Allow-Origin', '*')
                return resp
        else:
            resp = jsonify(empty_dir_msg)
            resp.headers.add('Access-Control-Allow-Origin', '*')
            return resp
    else:
        resp = jsonify(curl_msg)
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
