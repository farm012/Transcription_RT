import pyaudiowpatch as pyaudio
import wave

p = pyaudio.PyAudio()

device_info = p.get_default_wasapi_loopback()
device_index = device_info['index']

device_info = p.get_device_info_by_index(device_index)
sample_rate = 48000
chunk = 1024
record_seconds = 3
channels = 2

stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=sample_rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=1024)

output_file = wave.open("desktop_audio_recording.wav", 'wb')
output_file.setnchannels(2)  # Stereo
output_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
output_file.setframerate(sample_rate)


# Record audio TOOK 3 days to get this shi working
count = 1
try:
    while True:
        frames = []

        for _ in range(int(sample_rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)

        with wave.open("recording_chunk.wav", 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

        #print(f"Chunk recorded (2s): {count}")
        #count += 1 #Testing

except KeyboardInterrupt:
    print("Recording stopped.")

# Clean up gosh
stream.stop_stream()
stream.close()
p.terminate()