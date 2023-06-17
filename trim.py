import librosa
import soundfile as sf
# Load the audio file
d={'001/002/005': 0.8868571428571431, '001/002/006': 0.93425, '001/002/007': 0.78875, '001/002/008': 1.9520357142857143}
audio_file_path = 'test4.wav'
start_index = 0
count = 0

y, sr = librosa.load(audio_file_path, sr=None)
# print(y)
# Calculate the length of each chunk in samples
audio_chunks = []
chunk_length_samples = 0
for i in d:
    chunk_length_samples += int(d[i] * sr)
    # print("start_index",start_index,"chunk_length_samples",chunk_length_samples,"i",i,"d[i]",d[i])
    chunk = y[start_index:chunk_length_samples]
    audio_chunks.append(chunk)
    start_index = chunk_length_samples


# audio_chunks = [y[start_index:chunk_length_samples]]
# start_index = chunk_length_samples
# audio_chunks = [y[i:i+chunk_length_samples] for i in range(0, len(y), chunk_length_samples)]
print(audio_chunks,"audio_chunks")
    # Save each chunk to a separate file
for i, chunk in enumerate(audio_chunks):
    chunk_file_path = f'audio_{i}.wav'
    sf.write(chunk_file_path, chunk, sr)
