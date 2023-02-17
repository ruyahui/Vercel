from flask import Flask, Response,render_template
#import pyaudio
import wave
import os

app = Flask(__name__)


#FORMAT = pyaudio.paInt16
#CHANNELS = 2
#RATE = 44100
#CHUNK = 1024
#RECORD_SECONDS = 5

 
#audio1 = pyaudio.PyAudio()

def genHeader(sampleRate, bitsPerSample, channels):
	datasize = 2000*10**6
	o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
	o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
	o += bytes("WAVE",'ascii')                                              # (4byte) File type
	o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
	o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
	o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
	o += (channels).to_bytes(2,'little')                                    # (2byte)
	o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
	o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
	o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
	o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
	o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
	o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
	return o

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/audio')
def audio():
	# start Recording
	'''
    def sound():

        CHUNK = 1024
        sampleRate = 44100
        bitsPerSample = 16
        channels = 2
        wav_header = genHeader(sampleRate, bitsPerSample, channels)

        stream = audio1.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,input_device_index=1,
                        frames_per_buffer=CHUNK)
        print("recording...")
        #frames = []
        first_run = True
        while True:
           if first_run:
               data = wav_header + stream.read(CHUNK)
               first_run = False
           else:
               data = stream.read(CHUNK)
           yield(data)
	'''
	def play_sound():
		CHUNK = 65536
		sampleRate = 44100
		bitsPerSample = 16
		channels = 2
		wav_header = genHeader(sampleRate, bitsPerSample, channels)

		with wave.open("api/audio_tmp.wav", "rb") as wf:
			params = wf.getparams()
			nchannels, sampwidth, framerate, nframes = params[:4]
			print(nchannels, sampwidth, framerate, nframes)
			wav_header = genHeader(framerate, sampwidth*8, nchannels)
			first_run =True
			data = wav_header + wf.readframes(nframes)
			'''
			while True:
				if first_run:
					data = wav_header + wf.readframes(CHUNK)
					first_run = False
				else:
					data = wf.readframes(CHUNK)
				if data == b'':
					break
				yield(data)
				'''
			return data
	return Response(play_sound())

@app.route('/')
def index():
	folder = "toeic"
	files=os.listdir(folder)
	return render_template('index.html', files=files, folder = folder)

      
if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, threaded=True,port=5000)

