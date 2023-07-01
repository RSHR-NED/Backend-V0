# Flask App for virtual quran assistant

from flask import Flask, jsonify, render_template, request, make_response
from trim_dynamic import *
# from detect_word import predict_word
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/predict_word', methods=['POST'])
def predict_word_api():

    '''for comparison'''
    Al_Fatiha = [
    "Bis'mi",
    "Al-lahi",
    "Al-rahmaani",
    "Al-raheemi",
    "Alhamdu",
    "lillaahi",
    "Rabbil",
    "aalameen",
    "Ar-Rahmaan",
    "Ar-Raheem",
    "Maaliki",
    "Yumid",
    "Diin",
    "Iyyaka",
    "Na'abudu",
    "Iyyaka",
    "Nasta'een",
    "Ihdinas",
    "Siraatal",
    "Mustaqeem",
    "Siraatal",
    "Ladheena",
    "An'amta",
    "Alaihim",
    "Ghayril",
    "Maghdubi",
    "Alaihim",
    "Wala al-dalina"
    ]
    # user input Ayat number
    ayat_no = 1
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
    # predicted_word, confidence_score = predict_word(save_path)  
    # predicted_word = str(predicted_word)
    # confidence_score = round(float(confidence_score), 4)

    x = trim(save_path)
    print(x,'predictions')
    '''compare with Al-Fatiha'''
    # The code block you provided is creating a dictionary called `pred` and populating it with
    # predictions for each word in the input audio file.
    pred = {}
    ayat_1_index = [0,1,2,3]
    for i in range(len(x)):
        if ayat_no == 1:
            if x[i][2] == ayat_1_index[i]:
                pred[f'pred_word_{ayat_1_index[i]}'] = {'word':x[i][0],'confidence':str(x[i][1]),'correct':True}
            else:
                pred[f'pred_word_{ayat_1_index[i]}'] = {'word':Al_Fatiha[ayat_1_index[i]],'confidence':str(x[i][1]),'correct':False}

    print(pred,'predictions')
        ## similary for all Ayats
    os.remove(save_path)  # delete temp file
    print("Prediction completed")
    res = make_response(jsonify(pred))
    return res
    # return jsonify({'predicted_keyword': predicted_word, 'confidence_score': confidence_score}), 200

    

if __name__ == "__main__":
    app.run(debug=True)