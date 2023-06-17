# Flask App for virtual quran assistant

from flask import Flask, jsonify, render_template, request
from detect_word import predict_word
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/predict_word', methods=['POST'])
def predict_word_api():
    print("inside predict_word_api")
    # Check if audio file was sent and not empty
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return jsonify({'error': 'No audio file provided'}), 400
    
    save_path = os.path.join(os.path.dirname(__file__), 'temp.wav')
    audio_file.save(save_path)  # save the file 
    print("Starting prediction")
    predicted_word, confidence_score = predict_word(save_path)  
    predicted_word = str(predicted_word)
    confidence_score = round(float(confidence_score), 4)
    os.remove(save_path)  # delete temp file
    print("Prediction completed")
    print(f"Predicted keyword: {predicted_word}, confidence score: {confidence_score}")

    return jsonify({'predicted_keyword': predicted_word, 'confidence_score': confidence_score}), 200

    

if __name__ == "__main__":
    app.run(debug=True)