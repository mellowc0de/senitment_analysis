"""
A module for performing sentiment analysis on text data using an external
IBM Watson NLP service.

This module contains the `sentiment_analyzer` function which handles the
communication and data formatting required to send a text string to the
remote sentiment prediction endpoint and retrieve the raw results.

The primary goal is to provide a simple interface for determining the
emotional tone (e.g., positive, negative, neutral) of a given piece of text.
"""
import json

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
