from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Maximum file size (5MB)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Save the uploaded file temporarily
        temp_path = 'temp_audio'
        file.save(temp_path)
        
        # Open and transcribe the audio file
        with open(temp_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )
        
        # Clean up the temporary file
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'transcript': transcript['text']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
