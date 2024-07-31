from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import io
import logging
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up Azure OpenAI API credentials
openai.api_type = "azure"
openai.api_base = "https://nw-tech-wu.openai.azure.com/"
openai.api_version = "2024-02-01"
openai.api_key = "fce9b34907b848a6902e5c37ddfc8512"


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    transcript = data['transcript']
    question = data['question']

    # Combine transcript and question into a single prompt
    prompt = f"Transcript:\n{transcript}\n\nQuestion: {question}\nAnswer:"

    # Prepare messages for Azure OpenAI
    messages = [{"role": "system", "content": prompt}]

    # Query Azure OpenAI GPT-4
    response = openai.ChatCompletion.create(
        deployment_id="gpt-4o",  # Replace with your actual deployment ID
        messages=messages,
    )

    answer = response.choices[0].message['content'].strip()
    return jsonify({'answer': answer})

    
if __name__ == '__main__':
    app.run(debug=True)
