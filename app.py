# Flask App for virtual quran assistant

from flask import Flask, jsonify, render_template, request
from detect_word import predict_word
import os
from helpers import get_ayat_words_accuracy, mark_correctness_levels


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/predict_word', methods=['POST'])
def predict_word_api():
    
    # Check if audio file was sent and not empty
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return jsonify({'error': 'No audio file provided'}), 400
    
    save_path = os.path.join(os.path.dirname(__file__), 'tmp_for_word_prediction.wav')
    audio_file.save(save_path)  # save the file 
    print("Starting prediction")
    predicted_word, confidence_score = predict_word(save_path)  
    predicted_word = str(predicted_word)
    confidence_score = round(float(confidence_score), 4)
    os.remove(save_path)  # delete temp file
    print("Prediction completed")
    print(f"Predicted keyword: {predicted_word}, confidence score: {confidence_score}")

    return jsonify({'predicted_keyword': predicted_word, 'confidence_score': confidence_score}), 200

    
@app.route('/api/ayat_accuracy', methods=['POST'])
def ayat_accuracy():

    # Check if audio file was sent and not empty
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return jsonify({'error': 'No audio file provided'}), 400
    
    surah_number = request.form['surah_number']
    ayat_number = request.form['ayat_number']

    save_path = os.path.join(os.path.dirname(__file__), 'tmp_for_word_prediction.wav')
    audio_file.save(save_path)  # save the file 

    predictions = get_ayat_words_accuracy(save_path, surah_number, ayat_number)
    predictions = [(predicted_word, float(confidence)) for predicted_word, confidence in predictions]
    print(predictions, "PREDICTIONS HERE")
    correctness_levels, ayat_words = mark_correctness_levels(surah_number, ayat_number, predictions)
    os.remove(save_path)  # delete temp file

    return jsonify({'predictions': predictions, 'correctness_levels': correctness_levels, 'ayat_words': ayat_words}), 200


if __name__ == "__main__":
    app.run(debug=True)