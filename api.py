# api.py
from flask import Flask, request, jsonify
from app.main import TextSummarizerApp
import os

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    mode = data.get('mode', 'hybrid')
    num_sentences = data.get('num_sentences', 3)
    
    summarizer = TextSummarizerApp(mode=mode)
    report = summarizer.generate_report(data['text'], num_sentences)
    
    return jsonify(report)

@app.route('/summarize-file', methods=['POST'])
def summarize_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    mode = request.form.get('mode', 'hybrid')
    num_sentences = int(request.form.get('num_sentences', 3))
    
    # Save temporarily
    temp_path = os.path.join('/tmp', file.filename)
    file.save(temp_path)
    
    summarizer = TextSummarizerApp(mode=mode)
    try:
        report = summarizer.process_file(temp_path, num_sentences)
        os.remove(temp_path)
        return jsonify(report)
    except Exception as e:
        os.remove(temp_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)