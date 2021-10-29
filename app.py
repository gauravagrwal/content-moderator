from flask import Flask, render_template, request
import requests, os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    path = '/contentmoderator/moderate/v1.0/ProcessText/Screen'

    headers = {
        # Request headers
        'Content-Type': 'text/plain',
        'Ocp-Apim-Subscription-Key': os.environ['KEY'],
    }

    params = {
        # Request parameters
        'autocorrect': 'True',
        'PII': 'True',
        'classify': 'True',
    }

    # Create the full URL
    url = os.environ['ENDPOINT'] + path

    # Fetch the content from the form
    original_text = request.form['text']

    # Create the body of the request with the text to be screened
    body = [{'text': original_text}]

    # Make the call using post
    cm_request = requests.post(
        url=url, params=params, headers=headers, json=body)

    # Retrieve the JSON response
    cm_response = cm_request.json()

    text = cm_response['OriginalText']
    normalized_text = cm_response['NormalizedText']
    autocorrected_text = cm_response['AutoCorrectedText']
    lang = cm_response['Language']
    result = cm_response

    # Call render template, passing the result of the screening
    return render_template(
        'results.html',
        text=text,
        normalized_text=normalized_text,
        autocorrected_text=autocorrected_text,
        lang=lang,
        result=result
    )