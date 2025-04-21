import time
import whisper
import pykakasi

kks = pykakasi.kakasi()
model = whisper.load_model("tiny")
while True:
 result = model.transcribe("recording_chunk.wav")

 transcripted_text = result["text"]

#conversion_result = kks.convert(transcripted_text)

#romaji = " ".join([item['hepburn'] for item in conversion_result])

# Print the original text and its romaji
 print(f"Transcription: {transcripted_text}")
 time.sleep(1.8)
#print(f"Romaji: {romaji}")



