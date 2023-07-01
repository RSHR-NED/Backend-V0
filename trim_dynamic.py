from detect_word import predict_word
import librosa
import soundfile as sf
import os

def trim(audio_file_path):
    audio_chunks = []  # Initialize array to store all the chunks of audio data
    audio, sample_rate = librosa.load(audio_file_path, sr=None)  

    stride_len = 0.01  # stride used while chunking each word
    start_index = 0
    chunk_length_samples = 0

    word_length_stats = {'001/001/001': {'min': 0.242, 'max': 0.699, 'avg': 0.45785714285714285}, '001/001/002': {'min': 0.367, 'max': 0.859, 'avg': 
0.5751071428571429}, '001/001/003': {'min': 0.7, 'max': 1.406, 'avg': 1.0892499999999998}, '001/001/004': {'min': 0.937, 'max': 2.567, 'avg': 1.6800714285714287}, '001/002/005': {'min': 0.5, 'max': 1.091, 'avg': 0.7868571428571431}, '001/002/006': {'min': 0.615, 'max': 1.111, 'avg': 0.83425}, '001/002/007': {'min': 0.4, 'max': 0.912, 'avg': 0.68875}, '001/002/008': {'min': 1.161, 'max': 2.709, 'avg': 1.9520357142857143}, '001/003/009': {'min': 0.862, 'max': 1.459, 'avg': 1.167892857142857}, '001/003/010': {'min': 0.67, 'max': 2.73, 'avg': 1.8099642857142861}, '001/004/011': {'min': 0.554, 'max': 1.0, 'avg': 0.7934642857142858}, '001/004/012': {'min': 0.461, 'max': 1.032, 'avg': 0.6912142857142856}, '001/004/013': {'min': 0.8, 'max': 2.46, 'avg': 1.4113928571428571}, '001/005/014': {'min': 0.634, 'max': 1.096, 'avg': 0.9189642857142858}, '001/005/015': {'min': 0.7, 'max': 1.046, 'avg': 0.8418214285714285}, '001/005/016': {'min': 0.974, 'max': 1.485, 'avg': 1.2133928571428574}, '001/005/017': {'min': 1.2, 'max': 2.759, 'avg': 1.8921428571428573}, '001/006/018': {'min': 0.453, 'max': 1.017, 'avg': 0.6553571428571429}, '001/006/019': {'min': 0.592, 'max': 1.36, 'avg': 0.9681785714285714}, '001/006/020': {'min': 1.203, 'max': 3.066, 'avg': 2.1166428571428577}, '001/007/021': {'min': 0.648, 'max': 1.286, 'avg': 0.8096071428571426}, '001/007/022': {'min': 0.7, 'max': 1.382, 'avg': 1.044107142857143}, '001/007/023': {'min': 0.7, 'max': 1.292, 'avg': 1.0179285714285713}, '001/007/024': {'min': 0.751, 'max': 1.326, 'avg': 1.0681071428571431}, '001/008/025': {'min': 0.459, 'max': 1.04, 'avg': 0.7361785714285712}, '001/008/026': {'min': 0.7, 'max': 1.53, 'avg': 1.157857142857143}, '001/008/027': {'min': 0.775, 'max': 1.511, 'avg': 1.0293571428571429}, '001/008/028': {'min': 3.191, 'max': 6.874, 'avg': 4.930428571428572}}
    ayat_words = ['001/002/005', '001/002/006', '001/002/007', '001/002/008']

    predictions = []
    os.makedirs("./audios/temp_trim_chunks", exist_ok=True)
    for word in ayat_words:

        print(f"Processing word: {word}")
        min_len = word_length_stats[word]['min']
        max_len = word_length_stats[word]['max']

        current_stride = 0
        end_index = start_index + int((min_len + current_stride) * sample_rate)
        while (end_index <= (start_index + int(max_len * sample_rate))) and (end_index <= len(audio)):
            chunk = audio[start_index : end_index]
            sf.write("./audios/temp_chunk.wav", chunk, sample_rate)
            predicted_word, confidence, pred_index = predict_word("./audios/temp_chunk.wav")
            if confidence > 0.88:
                break
            current_stride += stride_len
            end_index = start_index + int((word_length_stats[word]['min'] + current_stride) * sample_rate)

        predictions.append((predicted_word, confidence, pred_index))
        print(f"predicted word: {predicted_word}, confidence: {confidence}, 'label': {pred_index}")
        chunk_length_samples += int((word_length_stats[word]['min'] + current_stride) * sample_rate)
        start_index = chunk_length_samples
        sf.write(f"./audios/temp_trim_chunks/{word.split('/')[-1]}.wav", chunk, sample_rate)
        audio_chunks.append(chunk)
    
    print()
    for prediction in predictions:
        print(prediction)
        
    return predictions
    


# example usage
if __name__ == "__main__":
    file_path = "./audios/014_TqE4rW4Q.wav"
    # file_path = "./audios/001002 - Abdurrahmaan As-Sudais.mp3"
    trim(file_path)

