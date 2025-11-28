# senitment_analysis

Documents Tree
```bash
./practice_project
./practice_project/server.py
./practice_project/LICENSE
./practice_project/SentimentAnalysis
./practice_project/SentimentAnalysis/sentiment_analysis.py
./practice_project/SentimentAnalysis/__pycache__
./practice_project/SentimentAnalysis/__pycache__/sentiment_analysis.cpython-311.pyc
./practice_project/SentimentAnalysis/__pycache__/__init__.cpython-311.pyc
./practice_project/SentimentAnalysis/__init__.py
./practice_project/.gitignore
./practice_project/__pycache__
./practice_project/__pycache__/sentiment_analysis.cpython-311.pyc
./practice_project/test_sentiment_analysis.py
./practice_project/static
./practice_project/static/mywebscript.js
./practice_project/templates
./practice_project/templates/index.html
./practice_project/README.md
```

SentimentAnalysis/sentiment_analysis.py
```python
mport json

import requests

def sentiment_analyzer(text_to_analyse):
    """
    Analyzes the sentiment of a given text using an external Watson NLP service.

    This function sends a POST request to a specific IBM Watson NLP endpoint,
    passing the text to be analyzed. It expects to receive a sentiment prediction
    (e.g., 'positive', 'negative', 'neutral') along with confidence scores,
    returned as a JSON string within the response text.

    :param text_to_analyse: The string of text whose sentiment needs to be analyzed.
    :type text_to_analyse: str
    :raises requests.exceptions.RequestException: If an error occurs during the HTTP request.
    :returns: The raw response text from the service, which is typically a JSON string
              containing the sentiment analysis results.
    :rtype: str
    """
    url = (
        'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/'
        'NlpService/SentimentPredict'
    )
    headers = {"grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"}
    myobj = { "raw_document": { "text": text_to_analyse } }

    label = None
    score = None

    try:
        response = requests.post(url, json = myobj, headers=headers, timeout=5)
        formatted_response = json.loads(response.text)

        if response.status_code == 200:
            label = formatted_response['documentSentiment']['label']
            score = formatted_response['documentSentiment']['score']

    except requests.exceptions.RequestException:
        print("Error: A request exception occurred (connection or timeout).")

    return {'label': label, 'score': score}

```

practice_project/server.py
```python
"""
A simple Flask application to serve the sentiment analyzer module.

This application runs on localhost:5000, providing a web interface
to submit text and display the sentiment analysis results from the
backend module.
"""
from flask import Flask, render_template, request
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

app = Flask("Sentiment Analyzer")

@app.route("/sentimentAnalyzer")
def sent_analyzer():
    ''' This code receives the text from the HTML interface and 
        runs sentiment analysis over it using sentiment_analysis()
        function. The output returned shows the label and its confidence 
        score for the provided text.
    '''
    text_to_analyze = request.args.get('textToAnalyze')
    response = sentiment_analyzer(text_to_analyze)
    label = response['label']
    score = response['score']

    if label is None:
        return "Invalid input! Try again."

    result_message = (
        f"The given text has been identified as {label.split('_')[1]} "
        f"with a score of {score}."
    )
    return result_message

@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

```
